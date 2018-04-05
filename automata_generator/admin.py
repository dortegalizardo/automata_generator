from django.contrib import admin
from automata_generator.models import *

# Register your models here.

admin.site.register(Automata)
admin.site.register(AutomataState)
admin.site.register(AutomataLanguage)
admin.site.register(AutomataTransition)
admin.site.register(AutomataTest)
admin.site.register(PDA)
admin.site.register(PDAState)
admin.site.register(PDASymbolInput)
admin.site.register(PDASymbolStack)
@admin.register(PDATransition)
class PDATransitionAdmin(admin.ModelAdmin):
    list_display = ('pda', 'state', 'pda_input', 'pda_stack', 'move')
    list_display_links = ['pda']

admin.site.register(TransitionMove)
