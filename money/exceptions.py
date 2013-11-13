

class CurrencyMismatch(Exception):
    def __init__(self, a, b, operation):
        message = ("unsupported operation between money in '{}' "
                   "and '{}': '{}'. Use XMoney for automatic "
                   "currency conversion.").format(a, b, operation)
        super().__init__(message)


class ExchangeRatesUnavailable(Exception):
    def __init__(self):
        super().__init__("there is no backend registered")



