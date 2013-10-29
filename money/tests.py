import collections
from decimal import Decimal

import unittest

from money import Money


class TestClass(unittest.TestCase):
    def setUp(self):
        self.m = Money('2.22', 'EUR')
    
    def test_new_instance_int_amount(self):
        self.assertIsInstance(Money(0, 'EUR'), Money)
        self.assertIsInstance(Money(12345, 'EUR'), Money)
    
    def test_new_instance_decimal_amount(self):
        self.assertIsInstance(Money(Decimal(12345), 'EUR'), Money)
    
    def test_new_instance_float_amount(self):
        self.assertIsInstance(Money(12345.12345, 'EUR'), Money)
    
    def test_new_instance_str_amount(self):
        self.assertIsInstance(Money('0', 'EUR'), Money)
        self.assertIsInstance(Money('12345.12345', 'EUR'), Money)
    
    def test_invalid_currency_none(self):
        with self.assertRaises(ValueError):
            money = Money('2.22', None)
    
    def test_invalid_currency_false(self):
        with self.assertRaises(ValueError):
            money = Money('2.22', False)
    
    def test_repr(self):
        self.assertEqual(repr(self.m), 'EUR 2.22')
    
    def test_str(self):
        self.assertEqual(str(self.m), 'EUR 2.22')
    
    def test_not_hashable(self):
        self.assertFalse(isinstance(self.m, collections.Hashable))


class TestNumericOperations(unittest.TestCase):
    def test_lt(self):
        self.assertTrue(Money('2.219', 'EUR') < Money('2.22', 'EUR'))
        self.assertTrue(Money('-2.22', 'EUR') < Money('2.22', 'EUR'))
    
    def test_le(self):
        self.assertTrue(Money('2.219', 'EUR') <= Money('2.22', 'EUR'))
        self.assertTrue(Money('-2.22', 'EUR') <= Money('2.22', 'EUR'))
        self.assertTrue(Money('2.220', 'EUR') <= Money('2.22', 'EUR'))
    
    def test_eq(self):
        self.assertTrue(Money('2.220', 'EUR') == Money('2.22', 'EUR'))
    
    def test_nq(self):
        self.assertTrue(Money('2.219', 'EUR') != Money('2.22', 'EUR'))
    
    def test_gt(self):
        self.assertTrue(Money('2.22', 'EUR') > Money('2.219', 'EUR'))
        self.assertTrue(Money('2.22', 'EUR') > Money('-2.22', 'EUR'))
    
    def test_ge(self):
        self.assertTrue(Money('2.22', 'EUR') > Money('2.219', 'EUR'))
        self.assertTrue(Money('2.22', 'EUR') > Money('-2.22', 'EUR'))
        self.assertTrue(Money('2.220', 'EUR') == Money('2.22', 'EUR'))
    
    def test_bool(self):
        self.assertTrue(Money('2.22', 'EUR'))
        self.assertFalse(Money('0', 'EUR'))
    
    def test_add(self):
        result = Money('2', 'EUR') + Money('2', 'EUR')
        self.assertEqual(result, Money('4', 'EUR'))
    
    def test_sub(self):
        result = Money('2', 'EUR') - Money('2', 'EUR')
        self.assertEqual(result, Money('0', 'EUR'))
    
    def test_mul_number(self):
        result = Money('2', 'EUR') * 2
        self.assertEqual(result, Money('4', 'EUR'))
    
    def test_mul_money(self):
        with self.assertRaises(TypeError):
            Money('2', 'EUR') * Money('2', 'EUR')
    
    def test_truediv_number(self):
        result = Money('2.22', 'EUR') / 2
        self.assertEqual(result, Money('1.11', 'EUR'))
    
    def test_truediv_money(self):
        result = Money('2', 'EUR') / Money('2', 'EUR')
        self.assertEqual(result, Decimal('1'))
    
    def test_floordiv_number(self):
        result = Money('2.22', 'EUR') // 2
        self.assertEqual(result, Money('1', 'EUR'))
    
    def test_floordiv_money(self):
        result = Money('2.22', 'EUR') // Money('2', 'EUR')
        self.assertEqual(result, Decimal('1'))
    
    def test_mod_number(self):
        result = Money('2.22', 'EUR') % 2
        self.assertEqual(result, Money('0.22', 'EUR'))
    
    def test_mod_money(self):
        with self.assertRaises(TypeError):
            Money('2.22', 'EUR') % Money('2', 'EUR')
    
    def test_divmod_number(self):
        whole, remainder = divmod(Money('2.22', 'EUR'), 2)
        self.assertEqual(whole, Money('1', 'EUR'))
        self.assertEqual(remainder, Money('0.22', 'EUR'))
    
    def test_divmod_money(self):
        whole, remainder = divmod(Money('2.22', 'EUR'), Money('2', 'EUR'))
        self.assertEqual(whole, Decimal('1'))
        self.assertEqual(remainder, Decimal('0.22'))
    
    def test_pow_number(self):
        result = Money('3', 'EUR') ** 2
        self.assertEqual(result, Money('9', 'EUR'))
    
    def test_pow_money(self):
        with self.assertRaises(TypeError):
            Money('3', 'EUR') ** Money('2', 'EUR')
    
    def test_neg(self):
        result = -Money('2.22', 'EUR')
        self.assertEqual(result, Money('-2.22', 'EUR'))
    
    def test_pos(self):
        result = +Money('2.22', 'EUR')
        self.assertEqual(result, Money('2.22', 'EUR'))
    
    def test_abs(self):
        result = abs(Money('-2.22', 'EUR'))
        self.assertEqual(result, Money('2.22', 'EUR'))
    
    def test_int(self):
        self.assertEqual(int(Money('-2.22', 'EUR')), -2)
        self.assertEqual(int(Money('2.22', 'EUR')), 2)
    
    def test_float(self):
        self.assertEqual(float(Money('-2.22', 'EUR')), -2.22)
        self.assertEqual(float(Money('2.22', 'EUR')), 2.22)
    
    def test_round(self):
        self.assertEqual(round(Money('-1.49', 'EUR')), Money('-1', 'EUR'))
        self.assertEqual(round(Money('1.50', 'EUR')), Money('2', 'EUR'))
    



if __name__ == '__main__':
    unittest.main()


