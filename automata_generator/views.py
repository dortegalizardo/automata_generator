import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from automata_generator.models import Automata, AutomataState, AutomataTransition, AutomataTest, AutomataLanguage
from django.forms.models import model_to_dict
from django.core import serializers

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
            print(transitions)
            if transitions.count() > 1:
                is_nfa = True
    return is_nfa

def create_nfa(autoamta):
    transitions = AutomataTransition.objects.filter(automata=automata)
    symbols = AutomataLanguage.objects.filter(automata=automata)
    states = AutomataState.objects.filter(automata=automata)
    initial_state = states.filter(start_state=True)[0]

    return 0

def ajax_test_automata(request, pk):
    contex_dict = {}
    test = get_object_or_404(AutomataTest, pk=pk)
    strings = test.test.split(',')
    automata = test.automata
    nfa = check_automata(test.automata)
    if nfa:
        print('Create NFA')
    """
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
    """
    contex_dict = {
        'status': 'OK',
        'tests': ''
    }       
        
    return HttpResponse(json.dumps(contex_dict), content_type='application/json')