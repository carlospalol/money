# -*- coding: utf-8 -*-
"""
Money class unittests
"""
import unittest

from money import Money
from .mixins import *


class TestMoneyClass(ClassMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyRepresentations(RepresentationsMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyFormatting(FormattingMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyParser(ParserMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyNumericOperations(NumericOperationsMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyUnaryOperationsReturnNew(UnaryOperationsReturnNewMixin, unittest.TestCase):
    MoneyClass = Money

class TestMoneyLeftmostTypePrevails(LeftmostTypePrevailsMixin, unittest.TestCase):
    MoneyClass = Money
