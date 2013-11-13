

class CurrencyMismatch(Exception):
    def __init__(self, a, b, operation):
        message = ("unsupported operation between money in '{}' "
                   "and '{}': '{}'. Use XMoney for automatic "
                   "currency conversion.").format(a, b, operation)
        super().__init__(message)


class CurrencyExchangeUnavailable(Exception):
    def __init__(self):
        message = ("there is no backend installed: use e.g. money.xrates."
                   "register_backend('money.exchange.SimpleBackend')")
        super().__init__(message)


class CurrencyExchangeFailed(Exception):
    def __init__(self, name, a, b):
        message = ("rate not found in backend '{}': {}/{}".format(name, a, b))
        super().__init__(message)
