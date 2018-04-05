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
admin.site.register(PDATransition)
admin.site.register(TransitionMove)
