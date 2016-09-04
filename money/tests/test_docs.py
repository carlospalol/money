# -*- coding: utf-8 -*-
"""
Money doctests as unittest Suite
"""
# RADAR: Python2
from __future__ import absolute_import

import doctest
import unittest

# RADAR: Python2
import money.six

FILES = (
    '../../README.rst',
)

def load_tests(loader, tests, pattern):
    # RADAR Python 2.x
    if money.six.PY2:
        # Doc tests are Python 3.x
        return unittest.TestSuite()
    return doctest.DocFileSuite(*FILES)