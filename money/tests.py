import unittest
import collections
from decimal import Decimal
from money.money import Money, BABEL_AVAILABLE


class TestClass(unittest.TestCase):
    def test_new_instance_int_amount(self):
        self.assertIsInstance(Money(0, 'XXX'), Money)
        self.assertIsInstance(Money(12345, 'XXX'), Money)
    
    def test_new_instance_decimal_amount(self):
        self.assertIsInstance(Money(Decimal(12345), 'XXX'), Money)
    
    def test_new_instance_float_amount(self):
        self.assertIsInstance(Money(12345.12345, 'XXX'), Money)
    
    def test_new_instance_str_amount(self):
        self.assertIsInstance(Money('0', 'XXX'), Money)
        self.assertIsInstance(Money('12345.12345', 'XXX'), Money)
    
    def test_invalid_currency_none(self):
        with self.assertRaises(ValueError):
            money = Money('2.22', None)
    
    def test_invalid_currency_false(self):
        with self.assertRaises(ValueError):
            money = Money('2.22', False)
    
    def test_invalid_currency_empty(self):
        with self.assertRaises(ValueError):
            money = Money('2.22', '')
    
    def test_invalid_currency_code(self):
        with self.assertRaises(ValueError):
            money = Money('2.22', 'XX')
        with self.assertRaises(ValueError):
            money = Money('2.22', '123')
        with self.assertRaises(ValueError):
            money = Money('2.22', 'xxx')
        with self.assertRaises(ValueError):
            money = Money('2.22', '$')
        with self.assertRaises(ValueError):
            money = Money('2.22', 'US$')
    
    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            money = Money('twenty', 'XXX')
    
    def test_not_hashable(self):
        money = Money('2.22', 'XXX')
        self.assertFalse(isinstance(money, collections.Hashable))


class TestMoneyRepresentations(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(Money('1234.567', 'XXX')), 'XXX 1234.567')
    
    def test_str(self):
        self.assertEqual(str(Money('1234.567', 'XXX')), 'XXX 1,234.57')


@unittest.skipUnless(BABEL_AVAILABLE, "requires Babel")
class TestMoneyFormatting(unittest.TestCase):
    def setUp(self):
        self.money = Money('-1234.567', 'USD')
    
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


class TestMoneyParser(unittest.TestCase):
    def test_loads_valid(self):
        self.assertEqual(Money.loads('XXX 2.22'), Money('2.22', 'XXX'))
    
    def test_loads_missing_currency(self):
        with self.assertRaises(ValueError):
            money = Money.loads('2.22')
    
    def test_loads_reversed_order(self):
        with self.assertRaises(ValueError):
            money = Money.loads('2.22 XXX')
    
    def test_loads_empty(self):
        with self.assertRaises(ValueError):
            money = Money.loads('')


class TestNumericOperations(unittest.TestCase):
    def test_lt_number(self):
        self.assertTrue(Money('2.22', 'XXX') < 3)
        self.assertTrue(Money('2.22', 'XXX') < 3.0)
        self.assertTrue(Money('2.22', 'XXX') < Decimal(3))
    
    def test_lt_money(self):
        self.assertTrue(Money('2.219', 'XXX') < Money('2.22', 'XXX'))
        self.assertTrue(Money('-2.22', 'XXX') < Money('2.22', 'XXX'))
    
    def test_lt_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') < None
    
    def test_le_number(self):
        self.assertTrue(Money('2.219', 'XXX') <= 3)
        self.assertTrue(Money('2.219', 'XXX') <= 3.0)
        self.assertTrue(Money('-2.22', 'XXX') <= Decimal('3'))
    
    def test_le_money(self):
        self.assertTrue(Money('2.219', 'XXX') <= Money('2.22', 'XXX'))
        self.assertTrue(Money('-2.22', 'XXX') <= Money('2.22', 'XXX'))
        self.assertTrue(Money('2.220', 'XXX') <= Money('2.22', 'XXX'))
    
    def test_le_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') <= None
    
    def test_eq_number(self):
        self.assertTrue(Money('2', 'XXX') == 2)
        self.assertTrue(Money('2', 'XXX') == Decimal(2))
    
    def test_eq_money(self):
        self.assertTrue(Money('2.220', 'XXX') == Money('2.22', 'XXX'))
    
    def test_nq_number(self):
        self.assertTrue(Money('2.219', 'XXX') != 3)
        self.assertTrue(Money('2.219', 'XXX') != Decimal('2.22'))
    
    def test_nq_money(self):
        self.assertTrue(Money('2.219', 'XXX') != Money('2.22', 'XXX'))
    
    def test_nq_none(self):
        self.assertNotEqual(Money(0, 'XXX'), None)
    
    def test_gt_number(self):
        self.assertTrue(Money('2.22', 'XXX') > 2)
        self.assertTrue(Money('2.22', 'XXX') > Decimal('2'))
    
    def test_gt_money(self):
        self.assertTrue(Money('2.22', 'XXX') > Money('2.219', 'XXX'))
        self.assertTrue(Money('2.22', 'XXX') > Money('-2.22', 'XXX'))
    
    def test_gt_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') > None
    
    def test_ge_number(self):
        self.assertTrue(Money('2', 'XXX') >= 1)
        self.assertTrue(Money('2', 'XXX') >= 2)
        self.assertTrue(Money('2', 'XXX') >= Decimal('1'))
        self.assertTrue(Money('2', 'XXX') >= Decimal('2'))
    
    def test_ge_money(self):
        self.assertTrue(Money('2.22', 'XXX') >= Money('2.219', 'XXX'))
        self.assertTrue(Money('2.22', 'XXX') >= Money('-2.22', 'XXX'))
        self.assertTrue(Money('2.22', 'XXX') >= Money('2.22', 'XXX'))
    
    def test_ge_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') >= None
    
    def test_bool_true(self):
        self.assertTrue(Money('2.22', 'XXX'))
        self.assertTrue(Money('-1', 'XXX'))
    
    def test_bool_false(self):
        self.assertFalse(Money('0', 'XXX'))
    
    def test_add_number(self):
        result = Money('2', 'XXX') + 2
        self.assertEqual(result, Money('4', 'XXX'))
        result = Money('2', 'XXX') + Decimal('2')
        self.assertEqual(result, Money('4', 'XXX'))
    
    def test_add_money(self):
        result = Money('2', 'XXX') + Money('2', 'XXX')
        self.assertEqual(result, Money('4', 'XXX'))
    
    def test_add_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') + None
    
    def test_sub_number(self):
        result = Money('2', 'XXX') - 2
        self.assertEqual(result, Money('0', 'XXX'))
        result = Money('2', 'XXX') - Decimal(2)
        self.assertEqual(result, Money('0', 'XXX'))
    
    def test_sub_money(self):
        result = Money('2', 'XXX') - Money('2', 'XXX')
        self.assertEqual(result, Money('0', 'XXX'))
    
    def test_sub_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') - None
    
    def test_mul_number(self):
        result = Money('2', 'XXX') * 2
        self.assertEqual(result, Money('4', 'XXX'))
    
    def test_mul_money(self):
        with self.assertRaises(TypeError):
            Money('2', 'XXX') * Money('2', 'XXX')
    
    def test_mul_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') * None
    
    def test_truediv_number(self):
        result = Money('2.22', 'XXX') / 2
        self.assertEqual(result, Money('1.11', 'XXX'))
    
    def test_truediv_money(self):
        result = Money('2', 'XXX') / Money('2', 'XXX')
        self.assertEqual(result, Decimal('1'))
    
    def test_truediv_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') / None
    
    def test_floordiv_number(self):
        result = Money('2.22', 'XXX') // 2
        self.assertEqual(result, Money('1', 'XXX'))
    
    def test_floordiv_money(self):
        result = Money('2.22', 'XXX') // Money('2', 'XXX')
        self.assertEqual(result, Decimal('1'))
    
    def test_floordiv_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') // None
    
    def test_mod_number(self):
        result = Money('2.22', 'XXX') % 2
        self.assertEqual(result, Money('0.22', 'XXX'))
    
    def test_mod_money(self):
        with self.assertRaises(TypeError):
            Money('2.22', 'XXX') % Money('2', 'XXX')
    
    def test_mod_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') % None
    
    def test_divmod_number(self):
        whole, remainder = divmod(Money('2.22', 'XXX'), 2)
        self.assertEqual(whole, Money('1', 'XXX'))
        self.assertEqual(remainder, Money('0.22', 'XXX'))
    
    def test_divmod_money(self):
        whole, remainder = divmod(Money('2.22', 'XXX'), Money('2', 'XXX'))
        self.assertEqual(whole, Decimal('1'))
        self.assertEqual(remainder, Decimal('0.22'))
    
    def test_divmod_none(self):
        with self.assertRaises(TypeError):
            divmod(Money(0, 'XXX'), None)
    
    def test_pow_number(self):
        result = Money('3', 'XXX') ** 2
        self.assertEqual(result, Money('9', 'XXX'))
    
    def test_pow_money(self):
        with self.assertRaises(TypeError):
            Money('3', 'XXX') ** Money('2', 'XXX')
    
    def test_pow_none(self):
        with self.assertRaises(TypeError):
            Money(0, 'XXX') ** None
    
    def test_neg(self):
        result = -Money('2.22', 'XXX')
        self.assertEqual(result, Money('-2.22', 'XXX'))
    
    def test_pos(self):
        result = +Money('2.22', 'XXX')
        self.assertEqual(result, Money('2.22', 'XXX'))
    
    def test_abs(self):
        result = abs(Money('-2.22', 'XXX'))
        self.assertEqual(result, Money('2.22', 'XXX'))
    
    def test_int(self):
        self.assertEqual(int(Money('-2.22', 'XXX')), -2)
        self.assertEqual(int(Money('2.22', 'XXX')), 2)
    
    def test_float(self):
        self.assertEqual(float(Money('-2.22', 'XXX')), -2.22)
        self.assertEqual(float(Money('2.22', 'XXX')), 2.22)
    
    def test_round(self):
        self.assertEqual(round(Money('-1.49', 'XXX')), Money('-1', 'XXX'))
        self.assertEqual(round(Money('1.50', 'XXX')), Money('2', 'XXX'))
        self.assertEqual(round(Money('1.234', 'XXX'), 2), Money('1.23', 'XXX'))


class TestUnaryOperationsReturnNewObject(unittest.TestCase):
    def setUp(self):
        self.money = Money(2, 'XXX')
    
    def test_pos(self):
        self.assertIsNot(+self.money, self.money)
    
    def test_abs(self):
        self.assertIsNot(abs(self.money), self.money)
    
    def test_round(self):
        self.assertIsNot(round(self.money), self.money)


if __name__ == '__main__':
    unittest.main()


