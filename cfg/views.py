import json

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cfg.models import CFG, NonTerminal, Terminal, Production
from automata_generator.models import PDA, PDAState, PDASymbolStack, PDASymbolInput, PDATransition, TransitionMove


class HomeCFG(ListView):
    model = CFG
    template_name = 'cfg_home.html'

class CFGDetail(DetailView):
    model = CFG
    template_name = 'cfg_detail.html'

def ajax_create_pda(request, pk):
    current = get_object_or_404(CFG, pk=pk)
    terminals = Terminal.objects.filter(cfg=current)
    nonterminals = NonTerminal.objects.filter(cfg=current)
    productions = Production.objects.filter(cfg=current)
    # Create PDA
    pda = PDA(name=(current.name + '-PDA_NEW'), description=('Creación de PDA de -> '+current.name))
    pda.save()
    # Create 3 States: Estado de incio para meter $, Estado intermedio para las transicciones y Estado de Aceptación
    state1 = PDAState(pda=pda, label='q0', start_state=True, final_state=False)
    state1.save()
    state2 = PDAState(pda=pda, label='q1', start_state=False, final_state=False)
    state2.save()
    state3 = PDAState(pda=pda, label='q2', start_state=False, final_state=True)
    state3.save()
    # Create Input Symbols first EPSILON
    input_epsi = PDASymbolInput(pda=pda, value='EPSI')
    input_epsi.save()
    inputs_dollar = PDASymbolStack(pda=pda, value='$')
    inputs_dollar.save()
    input_epsi_stack = PDASymbolStack(pda=pda, value='EPSI')
    input_epsi_stack.save()
    move = TransitionMove(state=state1, production=inputs_dollar.value)
    move.save()
    # Create Transitions
    transition = PDATransition(pda=pda, state=state1, pda_input=input_epsi, pda_stack=input_epsi_stack, move=move)
    transition.save()
    
    for production in productions:
        # Create stackSymbol
        value = production.non_terminal.value
        check_count = PDASymbolStack.objects.filter(value = value)
        # Check if NonTerminal exists in the Stack already
        if check_count.count() == 0:
            input_stack = PDASymbolStack(pda=pda, value=value)
            input_stack.save()
        else:
            input_stack = check_count.first()
        list_productions = production.value.split('|')
        # Create Moves
        for item in list_productions:
            move = TransitionMove(state=state2, production=item.strip())
            move.save()
            # Create Transition
            transition = PDATransition(pda=pda, state=state2, pda_input=input_epsi, pda_stack=input_stack, move=move)
            transition.save()
    # End of Non Terminals PDA Transitions

    for item in terminals:
        # Check Input
        current_value = item.value
        check_input = PDASymbolInput.objects.filter(pda=pda, value=current_value)
        if check_input.count() == 0:
            new_input = PDASymbolInput(pda=pda, value=current_value)
            new_input.save()
        else:
            new_input = check_input.first()
        # Check Stack
        check_stack = PDASymbolStack.objects.filter(pda=pda, value=current_value)
        if check_stack.count() == 0:
            new_stack_symbol = PDASymbolStack(pda=pda, value=current_value)
            new_stack_symbol.save()
        else:
            new_stack_symbol = check_stack.first()
        
        # Check Move
        check_move = TransitionMove.objects.filter(state=state2, production=input_epsi.value)
        if check_move.count() == 0:
            move = TransitionMove(state=state2, production=input_epsi.value)
            move.save()
        else:
            move = check_move.first()
        
        # Create Transition
        transition = PDATransition(pda=pda, state=state2, pda_input=new_input, pda_stack=new_stack_symbol, move=move)
        transition.save()

    # Final State Transition
    move = TransitionMove(state=state3, production=inputs_dollar.value)
    move.save()
    transition = PDATransition(pda=pda, state=state3, pda_input=input_epsi, pda_stack=inputs_dollar, move=move)
    transition.save()
    contex_dict = {
        'status': 'OK',
        }  
    return HttpResponse(json.dumps(contex_dict), content_type='application/json')
    
    

