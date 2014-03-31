"""
Money unittests as mixins for Money and subclasses
"""
import abc
from decimal import Decimal
import collections
import unittest

from money import Money, XMoney


class ClassMixin(object):
    def test_new_instance_int_amount(self):
        self.assertIsInstance(self.MoneyClass(0, 'XXX'), self.MoneyClass)
        self.assertIsInstance(self.MoneyClass(12345, 'XXX'), self.MoneyClass)
    
    def test_new_instance_decimal_amount(self):
        self.assertIsInstance(self.MoneyClass(Decimal(12345), 'XXX'), self.MoneyClass)
    
    def test_new_instance_float_amount(self):
        self.assertIsInstance(self.MoneyClass(12345.12345, 'XXX'), self.MoneyClass)
    
    def test_new_instance_str_amount(self):
        self.assertIsInstance(self.MoneyClass('0', 'XXX'), self.MoneyClass)
        self.assertIsInstance(self.MoneyClass('12345.12345', 'XXX'), self.MoneyClass)
    
    def test_invalid_currency_none(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', None)
    
    def test_invalid_currency_false(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', False)
    
    def test_invalid_currency_empty(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', '')
    
    def test_invalid_currency_code(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', 'XX')
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', '123')
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', 'xxx')
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', '$')
        with self.assertRaises(ValueError):
            money = self.MoneyClass('2.22', 'US$')
    
    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass('twenty', 'XXX')
    
    def test_not_hashable(self):
        money = self.MoneyClass('2.22', 'XXX')
        self.assertFalse(isinstance(money, collections.Hashable))


class RepresentationsMixin(object):
    def test_repr(self):
        self.assertEqual(repr(self.MoneyClass('1234.567', 'XXX')), 'XXX 1234.567')
    
    def test_str(self):
        self.assertEqual(str(self.MoneyClass('1234.567', 'XXX')), 'XXX 1,234.57')


class FormattingMixin(object):
    def setUp(self):
        self.money = self.MoneyClass('-1234.567', 'USD')
    
    def test_custom_format_padding(self):
        self.assertEqual(self.money.format('en_US', '¤000000.00'), '-$001234.57')
    
    def test_custom_format_custom_negative(self):
        self.assertEqual(self.money.format('en_US', '¤#,##0.00;<¤#,##0.00>'), '<$1,234.57>')
    
    def test_custom_format_grouping(self):
        self.assertEqual(self.money.format('en_US', '¤#,##0.00'), '-$1,234.57')
        self.assertEqual(self.money.format('de_DE', '#,##0.00 ¤'), '-1.234,57 $')
        self.assertEqual(self.money.format('en_US', '¤0.00'), '-$1234.57')
        self.assertEqual(self.money.format('de_DE', '0.00 ¤'), '-1234,57 $')
    
    def test_custom_format_decimals(self):
        self.assertEqual(self.money.format('en_US', '¤0.000'), '-$1234.567')
        self.assertEqual(self.money.format('en_US', '¤0'), '-$1235')
    
    def test_auto_format_locales(self):
        self.assertEqual(self.money.format('en_US'), '($1,234.57)')
        self.assertEqual(self.money.format('de_DE'), '-1.234,57\xa0$')
        self.assertEqual(self.money.format('es_CO'), '-1.234,57\xa0US$')
    
    def test_auto_format_locales_alias(self):
        self.assertEqual(self.money.format('en'), self.money.format('en_US'))
        self.assertEqual(self.money.format('de'), self.money.format('de_DE'))


class ParserMixin(object):
    def test_loads_valid(self):
        self.assertEqual(self.MoneyClass.loads('XXX 2.22'), self.MoneyClass('2.22', 'XXX'))
    
    def test_loads_missing_currency(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass.loads('2.22')
    
    def test_loads_reversed_order(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass.loads('2.22 XXX')
    
    def test_loads_empty(self):
        with self.assertRaises(ValueError):
            money = self.MoneyClass.loads('')


class NumericOperationsMixin(object):
    def test_lt_number(self):
        self.assertTrue(self.MoneyClass('2.22', 'XXX') < 3)
        self.assertTrue(self.MoneyClass('2.22', 'XXX') < 3.0)
        self.assertTrue(self.MoneyClass('2.22', 'XXX') < Decimal(3))
    
    def test_lt_money(self):
        self.assertTrue(self.MoneyClass('2.219', 'XXX') < self.MoneyClass('2.22', 'XXX'))
        self.assertTrue(self.MoneyClass('-2.22', 'XXX') < self.MoneyClass('2.22', 'XXX'))
    
    def test_lt_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') < None
    
    def test_le_number(self):
        self.assertTrue(self.MoneyClass('2.219', 'XXX') <= 3)
        self.assertTrue(self.MoneyClass('2.219', 'XXX') <= 3.0)
        self.assertTrue(self.MoneyClass('-2.22', 'XXX') <= Decimal('3'))
    
    def test_le_money(self):
        self.assertTrue(self.MoneyClass('2.219', 'XXX') <= self.MoneyClass('2.22', 'XXX'))
        self.assertTrue(self.MoneyClass('-2.22', 'XXX') <= self.MoneyClass('2.22', 'XXX'))
        self.assertTrue(self.MoneyClass('2.220', 'XXX') <= self.MoneyClass('2.22', 'XXX'))
    
    def test_le_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') <= None
    
    def test_eq(self):
        self.assertEqual(self.MoneyClass('2', 'XXX'), self.MoneyClass('2', 'XXX'))
        self.assertEqual(self.MoneyClass('2.22000', 'XXX'), self.MoneyClass('2.22', 'XXX'))
    
    def test_ne(self):
        self.assertNotEqual(self.MoneyClass('0', 'XXX'), 0)
        self.assertNotEqual(self.MoneyClass('2', 'XXX'), 2)
        self.assertNotEqual(self.MoneyClass('2', 'XXX'), 'two')
    
    def test_ne_money(self):
        self.assertNotEqual(self.MoneyClass('2', 'XXX'), self.MoneyClass('3', 'XXX'))
        self.assertNotEqual(self.MoneyClass('2', 'XXX'), self.MoneyClass('2', 'YYY'))
    
    def test_ne_none(self):
        self.assertNotEqual(self.MoneyClass(0, 'XXX'), None)
    
    def test_gt_number(self):
        self.assertTrue(self.MoneyClass('2.22', 'XXX') > 2)
        self.assertTrue(self.MoneyClass('2.22', 'XXX') > Decimal('2'))
    
    def test_gt_money(self):
        self.assertTrue(self.MoneyClass('2.22', 'XXX') > self.MoneyClass('2.219', 'XXX'))
        self.assertTrue(self.MoneyClass('2.22', 'XXX') > self.MoneyClass('-2.22', 'XXX'))
    
    def test_gt_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') > None
    
    def test_ge_number(self):
        self.assertTrue(self.MoneyClass('2', 'XXX') >= 1)
        self.assertTrue(self.MoneyClass('2', 'XXX') >= 2)
        self.assertTrue(self.MoneyClass('2', 'XXX') >= Decimal('1'))
        self.assertTrue(self.MoneyClass('2', 'XXX') >= Decimal('2'))
    
    def test_ge_money(self):
        self.assertTrue(self.MoneyClass('2.22', 'XXX') >= self.MoneyClass('2.219', 'XXX'))
        self.assertTrue(self.MoneyClass('2.22', 'XXX') >= self.MoneyClass('-2.22', 'XXX'))
        self.assertTrue(self.MoneyClass('2.22', 'XXX') >= self.MoneyClass('2.22', 'XXX'))
    
    def test_ge_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') >= None
    
    def test_bool_true(self):
        self.assertTrue(self.MoneyClass('2.22', 'XXX'))
        self.assertTrue(self.MoneyClass('-1', 'XXX'))
    
    def test_bool_false(self):
        self.assertFalse(self.MoneyClass('0', 'XXX'))
    
    def test_add_int(self):
        result = self.MoneyClass('2', 'XXX') + 2
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_add_decimal(self):
        result = self.MoneyClass('2', 'XXX') + Decimal('2')
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_add_money(self):
        result = self.MoneyClass('2', 'XXX') + self.MoneyClass('2', 'XXX')
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_add_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') + None
    
    def test_radd_int(self):
        result = 2 + self.MoneyClass('2', 'XXX')
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_sub_int(self):
        result = self.MoneyClass('2', 'XXX') - 2
        self.assertEqual(result, self.MoneyClass('0', 'XXX'))
    
    def test_sub_decimal(self):
        result = self.MoneyClass('2', 'XXX') - Decimal(2)
        self.assertEqual(result, self.MoneyClass('0', 'XXX'))
    
    def test_sub_money(self):
        result = self.MoneyClass('2', 'XXX') - self.MoneyClass('2', 'XXX')
        self.assertEqual(result, self.MoneyClass('0', 'XXX'))
    
    def test_sub_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') - None
    
    def test_rsub_int(self):
        result = 2 - self.MoneyClass('2', 'XXX')
        self.assertEqual(result, self.MoneyClass('0', 'XXX'))
    
    def test_mul_int(self):
        result = self.MoneyClass('2', 'XXX') * 2
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_mul_float(self):
        result = self.MoneyClass('2', 'XXX') * 2.0
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_mul_decimal(self):
        result = self.MoneyClass('2', 'XXX') * Decimal(2)
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_mul_money(self):
        with self.assertRaises(TypeError):
            self.MoneyClass('2', 'XXX') * self.MoneyClass('2', 'XXX')
    
    def test_mul_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') * None
    
    def test_rmul_int(self):
        result = 2 * self.MoneyClass('2', 'XXX')
        self.assertEqual(result, self.MoneyClass('4', 'XXX'))
    
    def test_truediv_int(self):
        result = self.MoneyClass('2.22', 'XXX') / 2
        self.assertEqual(result, self.MoneyClass('1.11', 'XXX'))
    
    def test_truediv_decimal(self):
        result = self.MoneyClass('2.22', 'XXX') / Decimal(2)
        self.assertEqual(result, self.MoneyClass('1.11', 'XXX'))
    
    def test_truediv_money(self):
        result = self.MoneyClass('2', 'XXX') / self.MoneyClass('2', 'XXX')
        self.assertEqual(result, Decimal('1'))
    
    def test_truediv_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(2, 'XXX') / None
    
    def test_truediv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.MoneyClass(2, 'XXX') / 0
    
    def test_floordiv_number(self):
        result = self.MoneyClass('2.22', 'XXX') // 2
        self.assertEqual(result, self.MoneyClass('1', 'XXX'))
    
    def test_floordiv_money(self):
        result = self.MoneyClass('2.22', 'XXX') // self.MoneyClass('2', 'XXX')
        self.assertEqual(result, Decimal('1'))
    
    def test_floordiv_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(2, 'XXX') // None
    
    def test_floordiv_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.MoneyClass(2, 'XXX') // 0
    
    def test_mod_number(self):
        result = self.MoneyClass('2.22', 'XXX') % 2
        self.assertEqual(result, self.MoneyClass('0.22', 'XXX'))
    
    def test_mod_money(self):
        with self.assertRaises(TypeError):
            self.MoneyClass('2.22', 'XXX') % self.MoneyClass('2', 'XXX')
    
    def test_mod_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(2, 'XXX') % None
    
    def test_mod_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.MoneyClass(2, 'XXX') % 0
    
    def test_divmod_number(self):
        whole, remainder = divmod(self.MoneyClass('2.22', 'XXX'), 2)
        self.assertEqual(whole, self.MoneyClass('1', 'XXX'))
        self.assertEqual(remainder, self.MoneyClass('0.22', 'XXX'))
    
    def test_divmod_money(self):
        whole, remainder = divmod(self.MoneyClass('2.22', 'XXX'), self.MoneyClass('2', 'XXX'))
        self.assertEqual(whole, Decimal('1'))
        self.assertEqual(remainder, Decimal('0.22'))
    
    def test_divmod_none(self):
        with self.assertRaises(TypeError):
            divmod(self.MoneyClass(2, 'XXX'), None)
    
    def test_divmod_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divmod(self.MoneyClass(2, 'XXX'), 0)
    
    def test_pow_number(self):
        result = self.MoneyClass('3', 'XXX') ** 2
        self.assertEqual(result, self.MoneyClass('9', 'XXX'))
    
    def test_pow_money(self):
        with self.assertRaises(TypeError):
            self.MoneyClass('3', 'XXX') ** self.MoneyClass('2', 'XXX')
    
    def test_pow_none(self):
        with self.assertRaises(TypeError):
            self.MoneyClass(0, 'XXX') ** None
    
    def test_neg(self):
        result = -self.MoneyClass('2.22', 'XXX')
        self.assertEqual(result, self.MoneyClass('-2.22', 'XXX'))
    
    def test_pos(self):
        result = +self.MoneyClass('2.22', 'XXX')
        self.assertEqual(result, self.MoneyClass('2.22', 'XXX'))
    
    def test_abs(self):
        result = abs(self.MoneyClass('-2.22', 'XXX'))
        self.assertEqual(result, self.MoneyClass('2.22', 'XXX'))
    
    def test_int(self):
        self.assertEqual(int(self.MoneyClass('-2.22', 'XXX')), -2)
        self.assertEqual(int(self.MoneyClass('2.22', 'XXX')), 2)
    
    def test_float(self):
        self.assertEqual(float(self.MoneyClass('-2.22', 'XXX')), -2.22)
        self.assertEqual(float(self.MoneyClass('2.22', 'XXX')), 2.22)
    
    def test_round(self):
        self.assertEqual(round(self.MoneyClass('-1.49', 'XXX')), self.MoneyClass('-1', 'XXX'))
        self.assertEqual(round(self.MoneyClass('1.50', 'XXX')), self.MoneyClass('2', 'XXX'))
        self.assertEqual(round(self.MoneyClass('1.234', 'XXX'), 2), self.MoneyClass('1.23', 'XXX'))


class UnaryOperationsReturnNewMixin(object):
    def setUp(self):
        self.money = self.MoneyClass(2, 'XXX')
    
    def test_pos(self):
        self.assertIsNot(+self.money, self.money)
    
    def test_abs(self):
        self.assertIsNot(abs(self.money), self.money)
    
    def test_round(self):
        self.assertIsNot(round(self.money), self.money)


class LeftmostTypePrevailsMixin(object):
    def setUp(self):
        if self.MoneyClass.__name__ == 'Money':
            self.OtherClass = XMoney
        if self.MoneyClass.__name__ == 'XMoney':
            self.OtherClass = Money
        
        self.home = self.MoneyClass(2, 'XXX')
        self.visitor = self.OtherClass(2, 'XXX')
    
    def test_add(self):
        result = self.home + self.visitor
        self.assertEqual(result.__class__, self.MoneyClass)
    
    def test_add_other(self):
        result = self.visitor + self.home
        self.assertEqual(result.__class__, self.OtherClass)
    
    def test_sub(self):
        result = self.home - self.visitor
        self.assertEqual(result.__class__, self.MoneyClass)
    
    def test_sub_other(self):
        result = self.visitor - self.home
        self.assertEqual(result.__class__, self.OtherClass)
    







