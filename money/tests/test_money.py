# -*- coding: utf-8 -*-
"""
Money class unittests
"""
import unittest

from money import Money
from . import mixins
from money.exceptions import CurrencyMismatch


class TestMoneyInstantiation(mixins.InstantiationMixin, unittest.TestCase):
    def setUp(self):
        self.MoneyClass = Money


class TestMoneyClass(mixins.ClassMixin, unittest.TestCase):
    def setUp(self):
        self.money = Money('2.99', 'XXX')


class TestMoneyRepresentations(mixins.RepresentationsMixin, unittest.TestCase):
    def setUp(self):
        self.money = Money('1234.567', 'XXX')


class TestMoneyFormatting(mixins.FormattingMixin, unittest.TestCase):
    def setUp(self):
        self.money = Money('-1234.567', 'USD')


class TestMoneyParser(mixins.ParserMixin, unittest.TestCase):
    def setUp(self):
        self.MoneyClass = Money


class TestMoneyNumericOperations(mixins.NumericOperationsMixin, unittest.TestCase):
    def setUp(self):
        self.MoneyClass = Money
        
    def test_lt_money_different_currency(self):
        with self.assertRaises(CurrencyMismatch):
            self.MoneyClass(2, 'AAA') < self.MoneyClass(2, 'BBB')
    
    def test_le_money_different_currency(self):
        with self.assertRaises(CurrencyMismatch):
            self.MoneyClass(2, 'AAA') <= self.MoneyClass(2, 'BBB')

    def test_gt_money_different_currency(self):
        with self.assertRaises(CurrencyMismatch):
            self.MoneyClass(2, 'AAA') > self.MoneyClass(2, 'BBB')
            
    def test_ge_money_different_currency(self):
        with self.assertRaises(CurrencyMismatch):
            self.MoneyClass(2, 'AAA') >= self.MoneyClass(2, 'BBB')
    

class TestMoneyUnaryOperationsReturnNew(mixins.UnaryOperationsReturnNewMixin, unittest.TestCase):
    def setUp(self):
        self.money = Money('2.99', 'XXX')


class TestMoneyLeftmostTypePrevails(mixins.LeftmostTypePrevailsMixin, unittest.TestCase):
    def setUp(self):
        self.MoneyClass = Money
        self.money = self.MoneyClass('2.99', 'XXX')
        self.MoneySubclass = type('MoneySubclass', (self.MoneyClass,), {})
        self.other_money = self.MoneySubclass('2.99', 'XXX')


