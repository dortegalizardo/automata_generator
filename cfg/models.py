from __future__ import unicode_literals

# Django Imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class CFG(models.Model):
    name = models.CharField(
        _('Nombre'),
        max_length=50,
        help_text='Ingrese el nombre de la grámatica Libre de Contexto')
    description = models.TextField(
        _('Descripción'),
        help_text='Ingrese alguna descripción acerca de la GLC.')
    
    def __str__(self):
        return str(self.name)


class Terminal(models.Model):
    cfg = models.ForeignKey(
        CFG,
        verbose_name='Gramática Libre de Contexto',
        on_delete = models.CASCADE,
        help_text='Seleccion la GLC')
    value = models.CharField(
        _('Valor'),
        max_length=150,
        help_text='Ingrese un valor para la terminal')

    def __str__(self):
        return '%s - %s' % (self.cfg, self.value)


class NonTerminal(models.Model):
    cfg = models.ForeignKey(
        CFG,
        verbose_name='Gramática Libre de Contexto',
        on_delete = models.CASCADE,
        help_text='Seleccion la GLC')
    value = models.CharField(
        _('Valor'),
        max_length=150,
        help_text='Ingrese un valor para la terminal')

    def __str__(self):
        return '%s - %s' % (self.cfg, self.value)
    

class Production(models.Model):
    cfg = models.ForeignKey(
        CFG,
        verbose_name='Gramática Libre de Contexto',
        on_delete = models.CASCADE,
        help_text='Seleccion la GLC')
    non_terminal =  models.ForeignKey(
        NonTerminal,
        verbose_name='No Terminal',
        on_delete = models.CASCADE,
        help_text='Seleccione un No Terminal para la producción.')
    value =  models.TextField(
        _('Valor'),
        help_text='Ingrese la producción o producciones divididas por | en caso de que haya multiples por No Terminal. Si \
        se necesita un Epsilon entonces usar la palabra reservada EPSI')
    
    def __str__(self):
        return '%s -> %s' % (self.non_terminal, self.value)
