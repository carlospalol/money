import abc
from decimal import Decimal
import unittest

from money import Money, XMoney, xrates
from money.exceptions import CurrencyExchangeUnavailable
from money.exceptions import CurrencyExchangeFailed


class TestExchangeRatesSetup(unittest.TestCase):
    def setUp(self):
        xrates.unregister_backend()
    
    def test_register(self):
        self.assertFalse(xrates)
        self.assertIsNone(xrates.backend_name)
        xrates.register_backend('money.exchange.SimpleBackend')
        self.assertEqual(xrates.backend_name, 'SimpleBackend')
    
    def test_unregister(self):
        xrates.register_backend('money.exchange.SimpleBackend')
        self.assertEqual(xrates.backend_name, 'SimpleBackend')
        xrates.unregister_backend()
        self.assertFalse(xrates)
        self.assertIsNone(xrates.backend_name)
    
    def test_no_backend_name(self):
        self.assertIsNone(xrates.backend_name)
    
    def test_no_backend_base(self):
        with self.assertRaises(CurrencyExchangeUnavailable):
            xrates.base
    
    def test_no_backend_get_rate(self):
        with self.assertRaises(CurrencyExchangeUnavailable):
            xrates.rate('XXX')
    
    def test_no_backend_get_quotation(self):
        with self.assertRaises(CurrencyExchangeUnavailable):
            xrates.quotation('XXX', 'YYY')


class BackendTestBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def test_base_property(self):
        pass
    
    @abc.abstractmethod
    def test_rate(self):
        pass
    
    @abc.abstractmethod
    def test_quotation(self):
        pass
    
    @abc.abstractmethod
    def test_unavailable_rate_returns_none(self):
        pass
    
    @abc.abstractmethod
    def test_unavailable_quotation_returns_none(self):
        pass
    
    @abc.abstractmethod
    def test_money_conversion(self):
        pass


class TestSimpleBackend(BackendTestBase, unittest.TestCase):
    def setUp(self):
        xrates.register_backend('money.exchange.SimpleBackend')
    
    def load_testing_data(self):
        xrates.base = 'XXX'
        xrates.setrate('AAA', Decimal('2'))
        xrates.setrate('BBB', Decimal('8'))
    
    def test_base_property(self):
        self.load_testing_data()
        self.assertEqual(xrates.base, 'XXX')
    
    def test_rate(self):
        self.load_testing_data()
        self.assertEqual(xrates.rate('XXX'), Decimal('1'))
        self.assertEqual(xrates.rate('AAA'), Decimal('2'))
        self.assertEqual(xrates.rate('BBB'), Decimal('8'))
    
    def test_quotation(self):
        self.load_testing_data()
        self.assertEqual(xrates.quotation('XXX', 'XXX'), Decimal('1'))
        self.assertEqual(xrates.quotation('XXX', 'AAA'), Decimal('2'))
        self.assertEqual(xrates.quotation('XXX', 'BBB'), Decimal('8'))
        self.assertEqual(xrates.quotation('AAA', 'XXX'), Decimal('0.5'))
        self.assertEqual(xrates.quotation('AAA', 'AAA'), Decimal('1'))
        self.assertEqual(xrates.quotation('AAA', 'BBB'), Decimal('4'))
        self.assertEqual(xrates.quotation('BBB', 'XXX'), Decimal('0.125'))
        self.assertEqual(xrates.quotation('BBB', 'AAA'), Decimal('0.25'))
        self.assertEqual(xrates.quotation('BBB', 'BBB'), Decimal('1'))
    
    def test_unavailable_rate_returns_none(self):
        self.load_testing_data()
        self.assertIsNone(xrates.rate('ZZZ'))
    
    def test_unavailable_quotation_returns_none(self):
        self.load_testing_data()
        self.assertIsNone(xrates.quotation('YYY', 'ZZZ'))
    
    def test_money_conversion(self):
        self.load_testing_data()
        self.assertEqual(Money('10', 'AAA').to('BBB'), Money('40', 'BBB'))
        self.assertEqual(Money('10', 'BBB').to('AAA'), Money('2.5', 'AAA'))
    
    def test_base_not_set_warning(self):
        with self.assertRaises(Warning):
            xrates.setrate('AAA', Decimal('2'))


class ConversionMixin(object):
    def test_unavailable_backend_conversion_error(self):
        xrates.unregister_backend()
        with self.assertRaises(CurrencyExchangeUnavailable):
            self.MoneyClass('2', 'AAA').to('BBB')
    
    def test_unavailable_rate_conversion_error(self):
        xrates.register_backend('money.exchange.SimpleBackend')
        with self.assertRaises(CurrencyExchangeFailed):
            self.MoneyClass('2', 'AAA').to('BBB')


class TestMoneyConversion(ConversionMixin, unittest.TestCase):
    MoneyClass = Money

class TestXMoneyConversion(ConversionMixin, unittest.TestCase):
    MoneyClass = XMoney







