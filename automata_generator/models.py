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
    is_nfa_eps = models.BooleanField(
        _('Es NFA EPS?'),
        default=False,
        help_text='Seleccione si el automata es NFA'
    )
    is_nfa = models.BooleanField(
        _('Es NFA?'),
        default=False,
        help_text='Seleccione si el automata es NFA'
    )
    dfa_associated = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        help_text='Seleccione si tiene una sección padre, sino por favor deje el campo en blanco',
        on_delete = models.CASCADE,
        related_name='DFA')
    
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
        max_length=10,
        help_text='Ingrese la etiqueta del estado. Ej: q0'
        )
    start_state = models.BooleanField(
         _('Es estado inicio?'),
        blank=False,
        default=False
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
        return '%s | desde: %s , hasta: %s , con: %s'  %(
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


class PDA(models.Model):
    name = models.CharField(
        _('Nombre'),
        max_length=50,
        help_text='Nombre del PDA')
    description = models.TextField(
        _('Descripción'),
        help_text='Descripción del PDA')

    def __str__(self):
        return str(self.name)


class PDAState(models.Model):
    pda = models.ForeignKey(
        PDA,
        verbose_name='PDA',
        on_delete=models.CASCADE,
        help_text='Seleccione el PDA.')
    label = models.CharField(
        _('Etiqueta'),
        max_length=2,
        help_text='Ingrese la etiqueta')
    start_state = models.BooleanField(
         _('Es estado inicio?'),
        blank=False,
        default=False
        )
    final_state = models.BooleanField(
        _('Es estado final?'),
        blank=False,
        default=False
        )

    def __str__(self):
        return '%s - %s' % (self.pda, self.label)


class PDASymbolStack(models.Model):
    pda = models.ForeignKey(PDA, verbose_name='PDA', on_delete=models.CASCADE, help_text='Seleccione el PDA.')
    value = models.CharField(_('Valor'), max_length=255, help_text='Ingrese la etiqueta')
    start_symbol = models.BooleanField(
        _('Es símbolo incial?'),
        blank=False,
        default=False
        )

    def __str__(self):
         return '%s - %s' % (self.pda, self.value)


class PDASymbolInput(models.Model):
    pda = models.ForeignKey(PDA, verbose_name='PDA', on_delete=models.CASCADE, help_text='Seleccione el PDA.')
    value = models.CharField(_('Valor'), max_length=255, help_text='Ingrese la etiqueta')
    
    def __str__(self):
         return '%s - %s' % (self.pda, self.value)


class TransitionMove(models.Model):
    state = models.ForeignKey(PDAState, on_delete=models.CASCADE, verbose_name='Estado')
    production = models.TextField(_('Producción'))

    def __str__(self):
        return '(%s , %s)' % (self.state, self.production)

class PDATransition(models.Model):
    pda = models.ForeignKey(PDA, verbose_name='PDA', on_delete=models.CASCADE, help_text='Seleccione el PDA.')
    state = models.ForeignKey(PDAState, on_delete=models.CASCADE, verbose_name='Estado')
    pda_input = models.ForeignKey(PDASymbolInput, on_delete=models.CASCADE)
    pda_stack = models.ForeignKey(PDASymbolStack, on_delete=models.CASCADE)
    move = models.ForeignKey(TransitionMove, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
