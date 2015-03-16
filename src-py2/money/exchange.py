# -*- coding: utf-8 -*-
"""
Money exchange related classes and ``xrates`` API entry point.
"""
import abc
import decimal
import importlib

from .exceptions import ExchangeBackendNotInstalled


class BackendBase():
    """Abstract base class API for exchange backends"""
    __metaclass__ = abc.ABCMeta

    @property
    @abc.abstractmethod
    def base(self):
        """Return the base currency"""
        return

    @abc.abstractmethod
    def rate(self, currency):
        """Return quotation between the base and another currency"""
        return None

    @abc.abstractmethod
    def quotation(self, origin, target):
        """Return quotation between two currencies (origin, target)"""
        a = self.rate(origin)
        b = self.rate(target)
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
            raise Warning("set the base first: xrates.base = currency")
        self._rates[currency] = rate

    def rate(self, currency):
        if currency == self.base:
            return decimal.Decimal(1)
        return self._rates.get(currency, None)

    def quotation(self, origin, target):
        return super(SimpleBackend, self).quotation(origin, target)


class ExchangeRates(object):
    def __init__(self):
        self._backend = None

    def __nonzero__(self):
        return bool(self._backend)

    def install(self, backend='money.exchange.SimpleBackend'):
        """Install an exchange rates backend using a python path string"""
        if isinstance(backend, basestring):
            path, name = backend.rsplit('.', 1)
            module = importlib.import_module(path)
            backend = getattr(module, name)()
        elif isinstance(backend, type):
            backend = backend()
        if not isinstance(backend, BackendBase):
            raise TypeError("backend '{}' is not a subclass of "
                            "money.xrates.BackendBase".format(backend))
        self._backend = backend

    def uninstall(self):
        """Uninstall any exchange rates backend"""
        self._backend = None

    @property
    def backend_name(self):
        """Return the class name of the currently installed backend or None"""
        if not self._backend:
            return None
        return self._backend.__class__.__name__

    @property
    def base(self):
        """Return the base currency"""
        if not self._backend:
            raise ExchangeBackendNotInstalled()
        return self._backend.base

    def rate(self, currency):
        """Return quotation between the base and another currency"""
        if not self._backend:
            raise ExchangeBackendNotInstalled()
        return self._backend.rate(currency)

    def quotation(self, origin, target):
        """Return quotation between two currencies (origin, target)"""
        if not self._backend:
            raise ExchangeBackendNotInstalled()
        return self._backend.quotation(origin, target)

    def __getattr__(self, name):
        if self._backend is None:
            raise ExchangeBackendNotInstalled()
        return getattr(self._backend, name)

    def __setattr__(self, name, value):
        if name == '_backend':
            self.__dict__[name] = value
        elif self._backend is None:
            raise ExchangeBackendNotInstalled()
        else:
            setattr(self._backend, name, value)


xrates = ExchangeRates()




