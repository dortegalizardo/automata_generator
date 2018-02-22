from django.contrib import admin
from automata_generator.models import (
    Automata,
    AutomataState,
    AutomataLanguage,
    AutomataTransition,
    AutomataTest
)

# Register your models here.

admin.site.register(Automata)
admin.site.register(AutomataState)
admin.site.register(AutomataLanguage)
admin.site.register(AutomataTransition)
admin.site.register(AutomataTest)
