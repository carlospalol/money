"""
Python money class with optional CLDR-backed locale-aware formatting
and an extensible currency exchange solution.
"""
from .money import Money, XMoney
from .exchange import xrates


# RADAR: version
__version__ = '1.3.0'
