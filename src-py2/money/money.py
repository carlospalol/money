# -*- coding: utf-8 -*-
"""
Money classes
"""
import decimal
import re
from distutils.version import StrictVersion

from .exchange import xrates
from .exceptions import (CurrencyMismatch, ExchangeRateNotFound,
                         InvalidOperandType)


__all__ = ['Money', 'XMoney']

BABEL_AVAILABLE = False
BABEL_VERSION = None
REGEX_CURRENCY_CODE = re.compile("^[A-Z]{3}$")
LC_NUMERIC = None

try:
    import babel
    import babel.numbers
    BABEL_AVAILABLE = True
    BABEL_VERSION = StrictVersion(babel.__version__)
    LC_NUMERIC = babel.default_locale('LC_NUMERIC')
except ImportError:
    pass


class Money(object):
    """Money class with a decimal amount and a currency"""
    
    def __init__(self, amount="0", currency=None):
        try:
            self._amount = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            raise ValueError("amount value could not be converted to "
                             "Decimal(): '{}'".format(amount))
        if currency in [None, False, '']:
            raise ValueError("invalid currency value: '{}'".format(currency))
        if not REGEX_CURRENCY_CODE.match(currency):
            raise ValueError("currency not in ISO 4217 format: "
                             "'{}'".format(currency))
        self._currency = currency
    
    @property
    def amount(self):
        return self._amount
    
    @property
    def currency(self):
        return self._currency
    
    def __hash__(self):
        return hash((self._amount, self._currency))
    
    def __repr__(self):
        return "{} {}".format(self._currency, self._amount)
    
    def __str__(self):
        return self.__unicode__().encode('utf-8')
    
    def __unicode__(self):
        return u"{} {:,.2f}".format(self._currency, self._amount)
    
    def __lt__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '<')
        elif other.currency != self._currency:
            raise CurrencyMismatch(self._currency, other.currency, '<')
        else:
            return self._amount < other.amount
    
    def __le__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '<=')
        elif other.currency != self._currency:
            raise CurrencyMismatch(self._currency, other.currency, '<=')
        else:
            return self._amount <= other.amount
    
    def __eq__(self, other):
        if isinstance(other, Money):
            return ((self._amount == other.amount) and
                    (self._currency == other.currency))
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __gt__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '>')
        elif other.currency != self._currency:
            raise CurrencyMismatch(self._currency, other.currency, '>')
        else:
            return self._amount > other.amount
    
    def __ge__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandType(other, '>=')
        elif other.currency != self._currency:
            raise CurrencyMismatch(self._currency, other.currency, '>=')
        else:
            return self._amount >= other.amount
    
    def __nonzero__(self):
        """
        Considering Money a numeric type (on ``amount``):
        
        bool(Money(2, 'XXX')) --> True
        bool(Money(0, 'XXX')) --> False
        """
        return bool(self._amount)
    
    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency != self._currency:
                raise CurrencyMismatch(self._currency, other.currency, '+')
            other = other.amount
        amount = self._amount + other
        return self.__class__(amount, self._currency)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency != self._currency:
                raise CurrencyMismatch(self._currency, other.currency, '-')
            other = other.amount
        amount = self._amount - other
        return self.__class__(amount, self._currency)
    
    def __rsub__(self, other):
        return (-self).__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError("multiplication is unsupported between "
                            "two money objects")
        amount = self._amount * other
        return self.__class__(amount, self._currency)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __div__(self, other):
        return self.__truediv__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Money):
            if other.currency != self._currency:
                raise CurrencyMismatch(self._currency, other.currency, '/')
            elif other.amount == 0:
                raise ZeroDivisionError()
            return self._amount / other.amount
        else:
            if other == 0:
                raise ZeroDivisionError()
            amount = self._amount / other
            return self.__class__(amount, self._currency)
    
    def __floordiv__(self, other):
        if isinstance(other, Money):
            if other.currency != self._currency:
                raise CurrencyMismatch(self._currency, other.currency, '//')
            elif other.amount == 0:
                raise ZeroDivisionError()
            return self._amount // other.amount
        else:
            if other == 0:
                raise ZeroDivisionError()
            amount = self._amount // other
            return self.__class__(amount, self._currency)
    
    def __mod__(self, other):
        if isinstance(other, Money):
            raise TypeError("modulo is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        if other == 0:
            raise ZeroDivisionError()
        amount = self._amount % other
        return self.__class__(amount, self._currency)
    
    def __divmod__(self, other):
        if isinstance(other, Money):
            if other.currency != self._currency:
                raise CurrencyMismatch(self._currency, other.currency, 'divmod')
            elif other.amount == 0:
                raise ZeroDivisionError()
            return divmod(self._amount, other.amount)
        else:
            if other == 0:
                raise ZeroDivisionError()
            whole, remainder = divmod(self._amount, other)
            return (self.__class__(whole, self._currency),
                    self.__class__(remainder, self._currency))
    
    def __pow__(self, other):
        if isinstance(other, Money):
            raise TypeError("power operator is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        amount = self._amount ** other
        return self.__class__(amount, self._currency)
    
    def __neg__(self):
        return self.__class__(-self._amount, self._currency)
    
    def __pos__(self):
        return self.__class__(+self._amount, self._currency)
    
    def __abs__(self):
        return self.__class__(abs(self._amount), self._currency)
        
    def __int__(self):
        return int(self._amount)
    
    def __float__(self):
        return float(self._amount)
    
    def __round__(self, ndigits=0):
        return self.__class__(round(self._amount, ndigits), self._currency)
    
    def __composite_values__(self):
        return self._amount, self._currency
    
    def to(self, currency):
        """Return equivalent money object in another currency"""
        if currency == self._currency:
            return self
        rate = xrates.quotation(self._currency, currency)
        if rate is None:
            raise ExchangeRateNotFound(xrates.backend_name,
                                         self._currency, currency)
        amount = self._amount * rate
        return self.__class__(amount, currency)
    
    def format(self, locale=LC_NUMERIC, pattern=None, currency_digits=True,
               format_type='standard'):
        """
        Return a locale-aware, currency-formatted string.
        
        This method emulates babel.numbers.format_currency().
        
        A specific locale identifier (language[_territory]) can be passed,
        otherwise the system's default locale will be used. A custom
        formatting pattern of the form "¤#,##0.00;(¤#,##0.00)"
        (positive[;negative]) can also be passed, otherwise it will be
        determined from the locale and the CLDR (Unicode Common Locale Data
        Repository) included with Babel.
        
        >>> m = Money('1234.567', 'EUR')
        >>> m.format() # assuming the system's locale is 'en_US'
        €1,234.57
        >>> m.format('de_DE') # German formatting
        1.234,57 €
        >>> m.format('de', '#,##0 ¤') # German formatting (short), no cents
        1.235 €
        >>> m.format(pattern='#,##0.00 ¤¤¤') # Default locale, full name
        1,235.57 euro
        
        Learn more about this formatting syntaxis at:
        http://www.unicode.org/reports/tr35/tr35-numbers.html
        """
        if BABEL_AVAILABLE:
            if BABEL_VERSION < StrictVersion('2.2'):
                raise Exception('Babel {} is unsupported. '
                    'Please upgrade to 2.2 or higher.'.format(BABEL_VERSION))
            return babel.numbers.format_currency(
                self._amount, self._currency, format=pattern, locale=locale,
                currency_digits=currency_digits, format_type=format_type)
        else:
            raise NotImplementedError("formatting requires Babel "
                                      "(https://pypi.python.org/pypi/Babel)")
    
    @classmethod
    def loads(cls, s):
        """Parse from a string representation (repr)"""
        try:
            currency, amount = s.strip().split(' ')
            return cls(amount, currency)
        except ValueError as err:
            raise ValueError("failed to parse string '{}': "
                             "{}".format(s, err))


class XMoney(Money):
    """Money subclass with implicit currency conversion"""
    def __add__(self, other):
        if isinstance(other, Money):
            other = other.to(self._currency)
        return super(XMoney, self).__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            other = other.to(self._currency)
        return super(XMoney, self).__sub__(other)
    
    def __div__(self, other):
        return self.__truediv__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Money):
            other = other.to(self._currency)
        return super(XMoney, self).__truediv__(other)
    
    def __floordiv__(self, other):
        if isinstance(other, Money):
            other = other.to(self._currency)
        return super(XMoney, self).__floordiv__(other)
    
    def __divmod__(self, other):
        if isinstance(other, Money):
            other = other.to(self._currency)
        return super(XMoney, self).__divmod__(other)







