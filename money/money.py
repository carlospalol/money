"""
NOTES:
* binary operations try to convert currencies
* Division between two Money objects drops the currency
* Money objects are not hashable
* FIXME: bool() behaves just like Decimal. e.g. bool(Money(0, 'EUR')) --> False
"""
import locale
import logging
import decimal

logger = logging.getLogger(__name__)


class Money(object):
    __hash__ = None
    
    def __init__(self, amount="0", currency=None):
        try:
            self.amount = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            raise TypeError("'{}' could not be converted to Decimal".format(amount))
        
        if currency is None or currency is False:
            raise ValueError("'{}' is not a valid currency".format(currency))
        self.currency = currency
        
    def __repr__(self):
        return "{} {}".format(self.currency, self.amount)
    
    def __str__(self):
        try:
            amount = locale.currency(self.amount, symbol=False, grouping=True, international=False)
            return "{} {}".format(amount, self.currency)
        except ValueError:
            return self.__repr__()
    
    def __lt__(self, other):
        return self.amount.__lt__(self._import_amount(other))
    
    def __le__(self, other):
        return self.amount.__le__(self._import_amount(other))
    
    def __eq__(self, other):
        return self.amount.__eq__(self._import_amount(other))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        return self.amount.__gt__(self._import_amount(other))
    
    def __ge__(self, other):
        return self.amount.__ge__(self._import_amount(other))
    
    def __bool__(self):
        return bool(self.amount)
    
    def __add__(self, other):
        amount = self.amount.__add__(self._import_amount(other))
        return self.__class__(amount, self.currency)
    
    def __sub__(self, other):
        amount = self.amount.__sub__(self._import_amount(other))
        return self.__class__(amount, self.currency)
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("multiplication is unsupported between two '{}' objects".format(self.__class__.__name__))
        amount = self.amount.__mul__(other)
        return self.__class__(amount, self.currency)
    
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self.amount.__truediv__(other.convert_to(self.currency).amount)
        else:
            amount = self.amount.__truediv__(other)
            return self.__class__(amount, self.currency)
    
    def __floordiv__(self, other):
        if isinstance(other, self.__class__):
            return self.amount.__floordiv__(other.convert_to(self.currency).amount)
        else:
            amount = self.amount.__floordiv__(other)
            return self.__class__(amount, self.currency)
    
    def __mod__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("modulo is unsupported between two '{}' objects".format(self.__class__.__name__))
        amount = self.amount.__mod__(other)
        return self.__class__(amount, self.currency)
    
    def __divmod__(self, other):
        if isinstance(other, self.__class__):
            return divmod(self.amount, other.convert_to(self.currency).amount)
        whole, remainder = divmod(self.amount, other)
        return (self.__class__(whole, self.currency), self.__class__(remainder, self.currency))
    
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("power operator is unsupported between two '{}' objects".format(self.__class__.__name__))
        amount = self.amount.__pow__(other)
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





