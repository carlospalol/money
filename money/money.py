import locale
import logging
import decimal
import re


logger = logging.getLogger(__name__)
BABEL_AVAILABLE = False
REGEX_CURRENCY_CODE = re.compile("^[A-Z]{3}$")

try:
    import babel
    import babel.numbers
    BABEL_AVAILABLE = True
except ImportError:
    pass


class Money(object):
    __hash__ = None
    
    def __init__(self, amount="0", currency=None):
        try:
            self.amount = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            raise ValueError("invalid amount value for Decimal(): '{}'".format(amount)) from None
        if currency in [None, False, '']:
            raise ValueError("invalid currency value: '{}'".format(currency))
        elif not REGEX_CURRENCY_CODE.match(currency):
            raise ValueError("currency not in ISO 4217 format: '{}'".format(currency))
        self.currency = currency
        
    def __repr__(self):
        return "{} {}".format(self.currency, self.amount)
    
    def __str__(self):
        return "{} {:,.2f}".format(self.currency, self.amount)
    
    def __lt__(self, other):
        return self.amount < self._import_amount(other)
    
    def __le__(self, other):
        return self.amount <= self._import_amount(other)
    
    def __eq__(self, other):
        return self.amount == self._import_amount(other)
    
    def __ne__(self, other):
        return not self == other
    
    def __gt__(self, other):
        return self.amount > self._import_amount(other)
    
    def __ge__(self, other):
        return self.amount >= self._import_amount(other)
    
    def __bool__(self):
        return True
    
    def __add__(self, other):
        amount = self.amount + self._import_amount(other)
        return self.__class__(amount, self.currency)
    
    def __sub__(self, other):
        amount = self.amount - self._import_amount(other)
        return self.__class__(amount, self.currency)
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("multiplication is unsupported between two '{}' objects".format(self.__class__.__name__))
        amount = self.amount * other
        return self.__class__(amount, self.currency)
    
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self.amount / other.convert_to(self.currency).amount
        else:
            amount = self.amount / other
            return self.__class__(amount, self.currency)
    
    def __floordiv__(self, other):
        if isinstance(other, self.__class__):
            return self.amount // other.convert_to(self.currency).amount
        else:
            amount = self.amount // other
            return self.__class__(amount, self.currency)
    
    def __mod__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("modulo is unsupported between two '{}' objects".format(self.__class__.__name__))
        amount = self.amount % other
        return self.__class__(amount, self.currency)
    
    def __divmod__(self, other):
        if isinstance(other, self.__class__):
            return divmod(self.amount, other.convert_to(self.currency).amount)
        whole, remainder = divmod(self.amount, other)
        return (self.__class__(whole, self.currency), self.__class__(remainder, self.currency))
    
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("power operator is unsupported between two '{}' objects".format(self.__class__.__name__))
        amount = self.amount ** other
        return self.__class__(amount, self.currency)
    
    def __neg__(self):
        return self.__class__(-self.amount, self.currency)
    
    def __pos__(self):
        return self.__class__(self.amount, self.currency)
    
    def __abs__(self):
        return self.__class__(abs(self.amount), self.currency)
        
    def __int__(self):
        return int(self.amount)
    
    def __float__(self):
        return float(self.amount)
    
    def __round__(self, ndigits=0):
        return self.__class__(round(self.amount, ndigits), self.currency)
    
    def _import_amount(self, other):
        """Return the converted amount of the other, if possible."""
        if isinstance(other, self.__class__):
            return other.convert_to(self.currency).amount
        else:
            return other
    
    def convert_to(self, currency):
        if currency == self.currency:
            return self
        else:
            raise NotImplementedError("money exchange not implemented yet")
    
    def format(self, locale=None, pattern=None):
        """
        Return a locale-aware, currency-formatted string.
        
        This method is a wrapper of Babel's babel.numbers.format_currency().
        
        A specific locale identifier (language[_territory]) can be passed,
        otherwise the system's default locale will be used. A custom formatting
        pattern of the form "¤#,##0.00;(¤#,##0.00)" (positive[;negative]) can
        also be passed, otherwise it will be determined from the locale and the
        CLDR (Unicode Common Locale Data Repository) included with Babel.
        
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
            raise NotImplementedError("Money formatting requires Babel (https://pypi.python.org/pypi/Babel)")
    
    @classmethod
    def loads(cls, s):
        """Parse and return a Money object from a string representation."""
        try:
            currency, amount = s.strip().split(' ')
            return cls(amount, currency)
        except ValueError as err:
            raise ValueError("failed to parse '{}' into Money: {}".format(s, err)) from None



