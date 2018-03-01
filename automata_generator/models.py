from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Automata(models.Model):
    name = models.CharField(
        _('Nombre'),
        blank=False, 
        null=False,
        max_length=255,
        help_text='Ingrese el nombre de la automata.'
        )
    description = models.TextField(
        _('Descripción'),
        blank=False,
        null=False,
        help_text='Brinde una breve explicación acerca de la automata'
        )
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Automata'
        verbose_name_plural = 'Automatas'


class AutomataState(models.Model):
    automata = models.ForeignKey(
        Automata,
        verbose_name='Automata',
        blank=False,
        null=False,
        help_text='Seleccione la automata asociada a este estado.',
        on_delete=models.CASCADE,
        )
    label = models.CharField(
        _('Etiqueta'),
        blank=False,
        null=False,
        max_length=2,
        help_text='Ingrese la etiqueta del estado. Ej: q0'
        )
    start_state = models.BooleanField(
         _('Es estado inicio?'),
        blank=False,
        default=True
        )
    final_state = models.BooleanField(
        _('Es estado final?'),
        blank=False,
        default=False
        )
    
    def clean(self):
        states = AutomataState.objects.filter(automata=self.automata)
        for item in states:
            if item.start_state == True and self.start_state == True:
                raise ValidationError('Ya hay un estado incial.')

    def __str__(self):
        return str(self.label)
    
    class Meta:
        verbose_name = 'Estado de Automata'
        verbose_name_plural = 'Estados de Automata'
        

class AutomataLanguage(models.Model):
    automata = models.ForeignKey(
        Automata,
        verbose_name='Automata',
        blank=False,
        null=False,
        help_text='Seleccione la automata asociada a este estado.',
        on_delete=models.CASCADE,
        )
    symbol = models.CharField(
        _('Caracter'),
        blank=False,
        null=False,
        max_length=1,
        help_text='Ingrese el carácter aceptado por esta automata'
        )
    
    def __str__(self):
        return str(self.symbol)

    class Meta:
        verbose_name = 'Caracter Aceptado por Automata'
        verbose_name_plural = 'Caracteres Aceptados por Automata'


class AutomataTransition(models.Model):
    automata = models.ForeignKey(
        Automata,
        verbose_name='Automata',
        blank=False,
        null=False,
        help_text='Seleccione la automata asociada a este estado.',
        on_delete=models.CASCADE,
        )
    transitionfrom = models.ForeignKey(
        AutomataState,
        blank=False,
        null=False,
        related_name='transition_from',
        help_text='Seleccione el estado donde comienza la transición.',
        on_delete=models.CASCADE,
        )
    value = models.ForeignKey(
        AutomataLanguage,
        blank=False,
        null=False,
        help_text='Seleccion el valor de la transición',
        on_delete=models.CASCADE,
        )
    transitionto = models.ForeignKey(
        AutomataState,
        blank=False,
        null=False,
        related_name='transition_to',
        help_text='Seleccione el estado donde comienza la transición.',
        on_delete=models.CASCADE,
        )
    
    def __str__(self):
        return '%s| desde: %s , hasta: %s , con:%s'  %(
            self.automata,
            self.transitionfrom,
            self.transitionto,
            self.value)
    
    class Meta:
        verbose_name = 'Transición de Automata'
        verbose_name_plural = 'Transiciones de Automatas'

class AutomataTest(models.Model):
    automata = models.ForeignKey(
        Automata,
        verbose_name='Automata',
        blank=False,
        null=False,
        help_text='Seleccione la automata asociada a este estado.',
        on_delete=models.CASCADE,
        )
    test = models.TextField(
        _('Cadenas de Prueba'),
        blank=True,
        help_text='Ingrese cadenas de prueba separadas por una "," '
    )

    def __str__(self):
        return '%s / %s' %(self.automata, self.test)
    
    class Meta:
        verbose_name = 'Prueba de Automata'
        verbose_name_plural = 'Pruebas de Automata'
