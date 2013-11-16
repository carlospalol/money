

class CurrencyMismatch(Exception):
    def __init__(self, a, b, operation):
        msg = ("unsupported operation between money in '{}' and '{}': '{}'. "
               "Use XMoney for automatic currency conversion."
               ).format(a, b, operation)
        super().__init__(msg)


class ExchangeError(Exception):
    pass

class ExchangeBackendNotInstalled(ExchangeError):
    def __init__(self):
        msg = "use e.g. money.xrates.install('money.exchange.SimpleBackend')"
        super().__init__(msg)


class ExchangeRateNotFound(ExchangeError):
    def __init__(self, backend, a, b):
        msg = ("rate not found in backend '{}': {}/{}".format(backend, a, b))
        super().__init__(msg)


