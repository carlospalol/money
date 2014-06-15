# -*- coding: utf-8 -*-
"""
Python money class with optional CLDR-backed locale-aware formatting
and an extensible currency exchange solution.
"""
from .money import Money, XMoney
from .exchange import xrates


__version__ = '1.2.1'
