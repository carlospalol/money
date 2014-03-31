"""
Money doctests as unittest Suite
"""
import doctest


FILES = (
    '../../../README.rst',
)

def load_tests(loader, tests, pattern):
    return doctest.DocFileSuite(*FILES)