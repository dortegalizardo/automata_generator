import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from automata_generator.models import Automata, AutomataState, AutomataTransition, AutomataTest, AutomataLanguage
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class HomeAutomata(ListView):
    model = Automata
    template_name = 'home.html'

class AutomataDetail(DetailView):
    model = Automata
    template_name = 'automata_detail.html'

def ajax_get_states(request, pk):
    current = get_object_or_404(Automata, pk=pk) 
    states =  AutomataState.objects.filter(automata=current)
    states = serializers.serialize('json', states)
    contex_dict = {}
    contex_dict = {
        'status': 'OK',
        'states':states
    }
    return HttpResponse(json.dumps(contex_dict), content_type='application/json')

def ajax_get_transitions(request, pk):
    current = get_object_or_404(Automata, pk=pk)
    transitions = AutomataTransition.objects.filter(automata=current)
    contex_dict = {}
    data_list = []
    for item in transitions:
        data_list.append({
            'id': str(item.id),
            'from': str(item.transitionfrom.id),
            'to': str(item.transitionto.id),
            'value': str(item.value.symbol)
        })
    contex_dict = {
        'status': 'OK',
        'transitions': data_list
    }
    return HttpResponse(json.dumps(contex_dict), content_type='application/json')


def check_automata(automata):
    transitions = AutomataTransition.objects.filter(automata=automata)
    symbols = AutomataLanguage.objects.filter(automata=automata)
    states = AutomataState.objects.filter(automata=automata)
    is_nfa = False
    for state in states:
        for symbol in symbols:
            transitions = AutomataTransition.objects.filter(automata=automata, transitionfrom=state, value=symbol)
            if transitions.count() > 1:
                is_nfa = True
    return is_nfa

# TO DO > validar vacío en initial
def create_language(new_automata, symbols):
    for item in symbols:
        new_symbol = AutomataLanguage(automata=new_automata, symbol = item.symbol)
        new_symbol.save()

def create_label(automata, symbol, current_states):
    transitions_list = []
    new_label = ''
    for item in current_states:
        try:
            state = AutomataState.objects.get(automata=automata,label=item)
            current_transitions = AutomataTransition.objects.filter(automata=automata, transitionfrom=state, value__symbol=symbol.symbol)
            if current_transitions.count() != 0:
                for transition in current_transitions:
                    transitions_list.append(transition.transitionto.label)
        except ObjectDoesNotExist:
            new_label = str(item)

    if len(transitions_list)>0:
        new_label_list = []
        for label in transitions_list:
            if label not in new_label_list:
                new_label_list.append(label)
        new_label_list.sort()
        new_label = ",".join(new_label_list)
    elif new_label == '':
        new_label = ''
    else:
        new_label = new_label       
    return new_label

def create_new_state(new_automata, new_label):
    test_states = AutomataState.objects.filter(automata=new_automata, label=new_label)
    if test_states.count()== 0:
        new_state = AutomataState(automata=new_automata, label=new_label)
        new_state.save()
        return new_state
    else:
        return test_states[0]

def create_transition(new_automata, new_state, current_state, symbol):
    symbol = AutomataLanguage.objects.get(automata=new_automata, symbol=symbol)
    new_transition = AutomataTransition(automata=new_automata, transitionfrom=current_state, value=symbol, transitionto=new_state)
    new_transition.save()

def assign_final_state(new_automata,initial_final_states):
    original_final_states = []
    for state in initial_final_states:
        original_final_states.append(state.label)
    
    new_automta_states = AutomataState.objects.filter(automata=new_automata)
    
    for state in new_automta_states:
        current_labels = state.label.split(',')
        for label in current_labels:
            if label in original_final_states:
                state.final_state = True
                state.save()

def assign_tests(new_automata, automata):
    tests = AutomataTest.objects.filter(automata=automata)
    for test in tests:
        new_test = AutomataTest(automata=new_automata, test=test.test)
        new_test.save() 
    
    

def create_nfa(automata):
    transitions = AutomataTransition.objects.filter(automata=automata).order_by('-transitionfrom__start_state')
    symbols = AutomataLanguage.objects.filter(automata=automata)
    states = AutomataState.objects.filter(automata=automata).order_by('-start_state')
    initial_state = states.filter(start_state=True)[0]
    final_states = states.filter(final_state=True)
    new_automata = Automata(name=(automata.name + '-DFA_NEW'), description=('Creación de DFA del NFA - '+automata.name))
    new_automata.save()
    create_language(new_automata, symbols)
    symbols = AutomataLanguage.objects.filter(automata=new_automata)
    new_string = ''
    new_automata_states = []
    new_initial_state = AutomataState(automata = new_automata, label=initial_state.label, start_state=True)
    new_initial_state.save()
    new_automata_states.append(new_initial_state)
    for state in new_automata_states:
        for symbol in symbols:
            # Convert lable into list
            current_states = state.label.split(',')
            # Create new Label
            new_label = create_label(automata, symbol, current_states)
            if new_label != '':
                new_state = create_new_state(new_automata, new_label)
                if new_state not in new_automata_states:
                    new_automata_states.append(new_state)
                create_transition(new_automata,new_state,state, symbol)
            else:
                new_state = AutomataState(automata=new_automata, label=(str(current_states[0])+'1'))
                new_state.save()
                if new_state not in new_automata_states:
                    new_automata_states.append(new_state)
                create_transition(new_automata,new_state,state, symbol)
    assign_final_state(new_automata,final_states)
    assign_tests(new_automata,automata)
    automata.dfa_associated = new_automata
    automata.save()
    automata.is_nfa = True
    automata.save()
    return new_automata.id

def ajax_test_automata(request, pk):
    contex_dict = {}
    test = get_object_or_404(AutomataTest, pk=pk)
    strings = test.test.split(',')
    automata = test.automata
    nfa = check_automata(test.automata)
    if nfa:
        # Revisa si ya se creó un DFA equivalente
        if automata.is_nfa == False:
            # Crea DFA
            new_automata = create_nfa(automata)
            contex_dict = {
                'status': 'DFA',
                'id': str(new_automata)
                }
    else:
        # Not NFA
        states = AutomataState.objects.filter(automata=automata)
        initial_state = states.filter(start_state=True)[0]
        final_states = states.filter(final_state=True)
        current_state = initial_state
        transitions = AutomataTransition.objects.filter(automata=automata)
        results = []
        for string in strings:
            current_state = initial_state
            for char in string.strip():
                inner_transitions = AutomataTransition.objects.filter(automata=automata, transitionfrom = current_state, value__symbol=char)
                if inner_transitions:
                    current_state = inner_transitions[0].transitionto
                else:
                    current_state = None
            if current_state in final_states:
                results.append({
                    'string': str(string),
                    'result': 'OK'
                })
            else:
                results.append({
                    'string': str(string),
                    'result': 'Error'
                })
        contex_dict = {
            'status': 'OK',
            'tests': results
        }       
        
    return HttpResponse(json.dumps(contex_dict), content_type='application/json')