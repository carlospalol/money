import unittest

from money import Money
from money.money import BABEL_AVAILABLE
from .mixins import *


class TestMoneyClass(ClassMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyRepresentations(RepresentationsMixin, unittest.TestCase):
    MoneyClass = Money

@unittest.skipUnless(BABEL_AVAILABLE, "requires Babel")
class TestMoneyFormatting(FormattingMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyParser(ParserMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyNumericOperations(NumericOperationsMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyUnaryOperationsReturnNew(UnaryOperationsReturnNewMixin, unittest.TestCase):
    MoneyClass = Money


