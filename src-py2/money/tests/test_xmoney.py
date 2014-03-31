# -*- coding: utf-8 -*-
"""
XMoney class unittests
"""
from decimal import Decimal
import unittest

from money import XMoney, xrates
from money.money import BABEL_AVAILABLE
from .mixins import *


class TestXMoneyClass(ClassMixin, unittest.TestCase):
    MoneyClass = XMoney

class TestXMoneyRepresentations(RepresentationsMixin, unittest.TestCase):
    MoneyClass = XMoney

@unittest.skipUnless(BABEL_AVAILABLE, "requires Babel")
class TestXMoneyFormatting(FormattingMixin, unittest.TestCase):
    MoneyClass = XMoney

class TestXMoneyParser(ParserMixin, unittest.TestCase):
    MoneyClass = XMoney

class TestXMoneyNumericOperations(NumericOperationsMixin, unittest.TestCase):
    MoneyClass = XMoney

class TestXMoneyUnaryOperationsReturnNew(UnaryOperationsReturnNewMixin, unittest.TestCase):
    MoneyClass = XMoney

class TestXMoneyLeftmostTypePrevails(LeftmostTypePrevailsMixin, unittest.TestCase):
    MoneyClass = XMoney


class TestXMoneyAutoConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        xrates.install('money.exchange.SimpleBackend')
        xrates.base = 'XXX'
        xrates.setrate('AAA', Decimal('2'))
        xrates.setrate('BBB', Decimal('8'))
    
    @classmethod
    def tearDownClass(cls):
        xrates.uninstall()
    
    def setUp(self):
        self.x = XMoney('10', 'XXX')
        self.a = XMoney('10', 'AAA')
        self.b = XMoney('10', 'BBB')
        self.ax = XMoney('20', 'AAA')
        self.bx = XMoney('80', 'BBB')
    
    def test_lt(self):
        self.assertTrue(self.b < self.a)
        self.assertFalse(self.a < self.b)
        self.assertFalse(self.ax < self.bx)
    
    def test_le(self):
        self.assertTrue(self.b <= self.a)
        self.assertFalse(self.a <= self.b)
        self.assertTrue(self.ax <= self.bx)
        self.assertTrue(self.bx <= self.ax)
    
    def test_gt(self):
        self.assertTrue(self.a > self.b)
        self.assertFalse(self.b > self.a)
        self.assertFalse(self.ax > self.bx)
    
    def test_ge(self):
        self.assertTrue(self.a >= self.b)
        self.assertFalse(self.b >= self.a)
        self.assertTrue(self.ax >= self.bx)
        self.assertTrue(self.bx >= self.ax)
    
    def test_add(self):
        self.assertEqual(self.a + self.b, XMoney('12.5', 'AAA'))
        self.assertEqual(self.b + self.a, XMoney('50', 'BBB'))
    
    def test_sub(self):
        self.assertEqual(self.a - self.b, XMoney('7.5', 'AAA'))
        self.assertEqual(self.b - self.a, XMoney('-30', 'BBB'))
    
    def test_truediv(self):
        self.assertEqual(self.a / self.b, Decimal('4'))
        self.assertEqual(self.b / self.a, Decimal('0.25'))
    
    def test_floordiv(self):
        self.assertEqual(self.a // self.b, Decimal('4'))
        self.assertEqual(self.b // self.a, Decimal('0'))
    
    def test_divmod(self):
        whole, remainder = divmod(self.a, self.b)
        self.assertEqual(whole, Decimal('4'))
        self.assertEqual(remainder, Decimal('0'))
        whole, remainder = divmod(self.b, self.a)
        self.assertEqual(whole, Decimal('0'))
        self.assertEqual(remainder, Decimal('10'))



