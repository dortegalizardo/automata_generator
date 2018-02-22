# -*- coding: UTF-8 -*-
"""
Django settings for myproject project.
"""
from __future__ import unicode_literals

from .conf.dev import *



### See recipe "Local settings"
try:
    exec(open(os.path.join(os.path.dirname(__file__), "local_settings.py")).read())
except IOError:
    pass