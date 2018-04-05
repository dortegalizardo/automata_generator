from django.contrib import admin

# Model Imports
from cfg.models import (
    CFG,
    Terminal,
    NonTerminal,
    Production
)

admin.site.register(CFG)
admin.site.register(Terminal)
admin.site.register(NonTerminal)
admin.site.register(Production)
