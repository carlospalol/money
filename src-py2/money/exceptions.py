# -*- coding: utf-8 -*-
"""
Money exceptions
"""


class CurrencyMismatch(Exception):
    """Invalid operation between money objects of different currencies"""
    def __init__(self, a, b, operation):
        msg = ("unsupported operation between money in '{}' and '{}': '{}'. "
               "Use XMoney for automatic currency conversion."
               ).format(a, b, operation)
        super().__init__(msg)


class ExchangeError(Exception):
    """Generic exception related to exchange rates"""
    pass

class ExchangeBackendNotInstalled(ExchangeError):
    """No backend installed yet"""
    def __init__(self):
        msg = "use e.g. money.xrates.install('money.exchange.SimpleBackend')"
        super().__init__(msg)


class ExchangeRateNotFound(ExchangeError):
    """A rate/quotation was not returned by the backend"""
    def __init__(self, backend, a, b):
        msg = ("rate not found in backend '{}': {}/{}".format(backend, a, b))
        super().__init__(msg)


