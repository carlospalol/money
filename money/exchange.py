import abc
import decimal
import importlib

from .exceptions import ExchangeRatesUnavailable


__all__ = ['xrates']


class BackendBase(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def base(self):
        """Return the base currency"""
        return
    
    @abc.abstractmethod
    def rate(self, currency):
        """Return quotation between the base and a price currency"""
        return None
    
    def quotation(self, from_currency, to_currency):
        """Return quotation between two currencies"""
        a = self.rate(from_currency)
        b = self.rate(to_currency)
        if a and b:
            return b / a
        return None


class SimpleBackend(BackendBase):
    def __init__(self):
        self._base = None
        self._rates = {}
    
    @property
    def base(self):
        return self._base
    
    @base.setter
    def base(self, currency):
        self._base = currency
    
    def setrate(self, currency, rate):
        if not self.base:
            raise Exception("you must set the base first: "
                            "xrates.base = currency")
        self._rates[currency] = rate
    
    def rate(self, currency):
        if currency == self.base:
            return decimal.Decimal(1)
        return self._rates.get(currency, None)


class ExchangeRates(object):
    def __init__(self):
        self._backend = None
    
    def __bool__(self):
        return bool(self._backend)
    
    def register_backend(self, pythonpath='money.exchange.SimpleBackend'):
        path, name = pythonpath.rsplit('.', 1)
        module = importlib.import_module(path)
        backend = getattr(module, name)
        if not issubclass(backend, BackendBase):
            raise TypeError("backend '{}' is not a subclass of "
                            "BackendBase".format(backend))
        self._backend = backend()
    
    def unregister_backend(self):
        self._backend = None
    
    @property
    def backend_name(self):
        if not self._backend:
            return None
        return self._backend.__class__.__name__
    
    @property
    def base(self):
        if not self._backend:
            raise ExchangeRatesUnavailable()
        return self._backend.base
    
    def rate(self, currency):
        if not self._backend:
            raise ExchangeRatesUnavailable()
        return self._backend.rate(currency)
    
    def quotation(self, from_currency, to_currency):
        if not self._backend:
            raise ExchangeRatesUnavailable()
        return self._backend.quotation(from_currency, to_currency)
    
    def __getattr__(self, name):
        # Redirect other attribute retrievals to the backend
        if name == '_backend' or self._backend is None:
            raise ExchangeRatesUnavailable()
        return getattr(self._backend, name)
    
    def __setattr__(self, name, value):
        # Redirect all assignations to the backend
        if name == '_backend':
            self.__dict__[name] = value
        elif self._backend is None:
            raise ExchangeRatesUnavailable()
        else:
            setattr(self._backend, name, value)


xrates = ExchangeRates()




