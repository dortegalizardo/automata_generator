from django.shortcuts import render
from django.views.generic import ListView, DetailView

from cfg.models import CFG


class HomeCFG(ListView):
    model = CFG
    template_name = 'cfg_home.html'

class CFGDetail(DetailView):
    model = CFG
    template_name = 'cfg_detail.html'