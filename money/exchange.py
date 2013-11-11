import abc
import decimal
import importlib


class BackendBase(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def base(self):
        """Return the base currency"""
        return
    
    @base.setter
    @abc.abstractmethod
    def base(self, currency):
        """Set the base currency"""
        pass
    
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
            raise Exception("you must set the base first: xrates.base = currency")
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
            raise TypeError("backend '{}' is not a subclass of BackendBase".format(backend))
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
            raise Exception("no exchange rates backend registered")
        return self._backend.base
    
    @base.setter
    def base(self, currency):
        if not self._backend:
            raise Exception("no exchange rates backend registered")
        self._backend.base = currency
    
    def rate(self, currency):
        if not self._backend:
            raise Exception("no exchange rates backend registered")
        return self._backend.rate(currency)
    
    def quotation(self, from_currency, to_currency):
        if not self._backend:
            raise Exception("no exchange rates backend registered")
        return self._backend.quotation(from_currency, to_currency)
    
    def __getattr__(self, name):
        if not self._backend:
            raise Exception("no exchange rates backend registered")
        return getattr(self._backend, name)


xrates = ExchangeRates()




