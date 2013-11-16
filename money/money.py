"""
Money classes
"""
import decimal
import re

from .exchange import xrates
from .exceptions import CurrencyMismatch, ExchangeRateNotFound


__all__ = ['Money', 'XMoney']

BABEL_AVAILABLE = False
REGEX_CURRENCY_CODE = re.compile("^[A-Z]{3}$")

try:
    import babel
    import babel.numbers
    BABEL_AVAILABLE = True
except ImportError:
    pass


class Money(object):
    """Money class with a decimal amount and a currency"""
    def __init__(self, amount="0", currency=None):
        try:
            self.amount = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            raise ValueError("amount value could not be converted to "
                             "Decimal(): '{}'".format(amount)) from None
        if currency in [None, False, '']:
            raise ValueError("invalid currency value: '{}'".format(currency))
        if not REGEX_CURRENCY_CODE.match(currency):
            raise ValueError("currency not in ISO 4217 format: "
                             "'{}'".format(currency))
        self.currency = currency
    
    def __repr__(self):
        return "{} {}".format(self.currency, self.amount)
    
    def __str__(self):
        return "{} {:,.2f}".format(self.currency, self.amount)
    
    def __lt__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '<')
            other = other.amount
        return self.amount < other
    
    def __le__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '<=')
            other = other.amount
        return self.amount <= other
    
    def __eq__(self, other):
        if isinstance(other, Money):
            return ((self.amount == other.amount) and
                    (self.currency == other.currency))
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __gt__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '>')
            other = other.amount
        return self.amount > other
    
    def __ge__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '>=')
            other = other.amount
        return self.amount >= other
    
    def __bool__(self):
        """
        Considering Money a numeric type (on ``amount``):
        
        bool(Money(2, 'XXX')) --> True
        bool(Money(0, 'XXX')) --> False
        """
        return bool(self.amount)
    
    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '+')
            other = other.amount
        amount = self.amount + other
        return self.__class__(amount, self.currency)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '-')
            other = other.amount
        amount = self.amount - other
        return self.__class__(amount, self.currency)
    
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError("multiplication is unsupported between "
                            "two money objects")
        if isinstance(other, float):
            other = decimal.Decimal(other)
        amount = self.amount * other
        return self.__class__(amount, self.currency)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '/')
            elif other.amount == 0:
                raise ZeroDivisionError()
            return self.amount / other.amount
        else:
            if other == 0:
                raise ZeroDivisionError()
            amount = self.amount / other
            return self.__class__(amount, self.currency)
    
    def __floordiv__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '//')
            elif other.amount == 0:
                raise ZeroDivisionError()
            return self.amount // other.amount
        else:
            if other == 0:
                raise ZeroDivisionError()
            amount = self.amount // other
            return self.__class__(amount, self.currency)
    
    def __mod__(self, other):
        if isinstance(other, Money):
            raise TypeError("modulo is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        if other == 0:
            raise ZeroDivisionError()
        amount = self.amount % other
        return self.__class__(amount, self.currency)
    
    def __divmod__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, 'divmod')
            elif other.amount == 0:
                raise ZeroDivisionError()
            return divmod(self.amount, other.amount)
        else:
            if other == 0:
                raise ZeroDivisionError()
            whole, remainder = divmod(self.amount, other)
            return (self.__class__(whole, self.currency),
                    self.__class__(remainder, self.currency))
    
    def __pow__(self, other):
        if isinstance(other, Money):
            raise TypeError("power operator is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        amount = self.amount ** other
        return self.__class__(amount, self.currency)
    
    def __neg__(self):
        return self.__class__(-self.amount, self.currency)
    
    def __pos__(self):
        return self.__class__(+self.amount, self.currency)
    
    def __abs__(self):
        return self.__class__(abs(self.amount), self.currency)
        
    def __int__(self):
        return int(self.amount)
    
    def __float__(self):
        return float(self.amount)
    
    def __round__(self, ndigits=0):
        return self.__class__(round(self.amount, ndigits), self.currency)
    
    def to(self, currency):
        """Return equivalent money object in another currency"""
        if currency == self.currency:
            return self
        rate = xrates.quotation(self.currency, currency)
        if rate is None:
            raise ExchangeRateNotFound(xrates.backend_name,
                                         self.currency, currency)
        amount = self.amount * rate
        return self.__class__(amount, currency)
    
    def format(self, locale=None, pattern=None):
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
            if not locale:
                locale = babel.default_locale('LC_NUMERIC')
            locale = babel.Locale.parse(locale)
            if not pattern:
                pattern = locale.currency_formats.get(pattern)
            pattern = babel.numbers.parse_pattern(pattern)
            return pattern.apply(self.amount, locale, currency=self.currency)
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
                             "{}".format(s, err)) from None


class XMoney(Money):
    """Money subclass with implicit currency conversion"""
    def __lt__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__lt__(other)
    
    def __le__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__le__(other)
    
    def __gt__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__gt__(other)
    
    def __ge__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__ge__(other)
    
    def __add__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__add__(other)
    
    def __sub__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__sub__(other)
    
    def __truediv__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__truediv__(other)
    
    def __floordiv__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__floordiv__(other)
    
    def __divmod__(self, other):
        if isinstance(other, Money):
            other = other.to(self.currency)
        return super().__divmod__(other)







