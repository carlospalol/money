
============
Python Money
============

Money class with optional CLDR-backed locale-aware formatting and an extensible currency exchange solution.

.. RADAR: version

**This is version 1.4.0-dev**.

:Development: https://github.com/carlospalol/money
:Latest release: https://pypi.python.org/pypi/money/

This package is compatible with Python 2.7, 3.4, 3.5, but there are important `Differences between Python versions`_. All code examples use Python 3.5.

**Contents**

.. contents::
    :local:
    :backlinks: none


Installation
============

Install the latest release with:

::

    pip install money

For locale-aware formatting, also install the latest version of `Babel <https://pypi.python.org/pypi/Babel>`_ (2.2 or 2.3 required):

::

    pip install babel


Usage
=====

.. code:: python

    >>> from money import Money
    >>> m = Money(amount='2.22', currency='EUR')
    >>> m
    EUR 2.22

*amount* can be any valid value in ``decimal.Decimal(value)`` and *currency* should be a three-letter currency code. Money objects are immutable by convention and hashable. Once created, you can use read-only properties ``amount`` (decimal.Decimal) and ``currency`` (str) to access its internal components:

.. code:: python

    >>> m = Money(2, 'USD')
    >>> m.amount
    Decimal('2')
    >>> m.currency
    'USD'

Money emulates a numeric type and you can apply most arithmetic and comparison operators between money objects, as well as addition, subtraction, and division with integers (int) and decimal numbers (decimal.Decimal):

.. code:: python

    >>> m = Money('2.22', 'EUR')
    >>> m / 2
    EUR 1.11
    >>> m + Money('7.77', 'EUR')
    EUR 9.99

More formally, with *AAA* and *BBB* being different currencies:

+-----------+---------------+-----------+-----------+-----------------+
|           | Operator      | Money AAA | Money BBB | int, Decimal    |
+===========+===============+===========+===========+=================+
| **Money   | ``+``, ``-``  | Money     | N/A       | Money           |
+ AAA**     +---------------+-----------+-----------+-----------------+
|           | ``*``         | N/A       | N/A       | Money           |
+           +---------------+-----------+-----------+-----------------+
|           | ``/``, ``//`` | Decimal   | N/A       | Money           |
+           +---------------+-----------+-----------+-----------------+
|           | ``>``, ``>=`` | Compares  | N/A       | N/A             |
|           | ``<``, ``<=`` | amount.   |           |                 |
+           +---------------+           +-----------+-----------------+
|           | ``==``        |           | False     | False           |
|           |               |           |           |                 |
+-----------+---------------+-----------+-----------+-----------------+

Arithmetic operations with floats are not directly supported. If you need to operate with floats, you must first convert the float to a Decimal, or the Money object to a float (i.e. float(m)). Please be aware of the `issues and limitations of floating point arithmetics <https://docs.python.org/3/tutorial/floatingpoint.html>`_.


Currency presets
----------------

If you use fixed currencies in your code, you may find convenient to create currency-preset Money subclasses:

.. code:: python

    class EUR(Money):
        def __init__(self, amount='0'):
            super().__init__(amount=amount, currency='EUR')
    
    price = EUR('9.99')


Formatting
==========

Money objects are printed by default with en_US formatting and the currency code.

.. code:: python

    >>> m = Money('1234.567', 'EUR')
    >>> str(m)
    'EUR 1,234.57'

Use ``format(locale=LC_NUMERIC, pattern=None, currency_digits=True, format_type='standard')`` for locale-aware formatting with currency expansion. ``format()`` relies on ``babel.numbers.format_currency()``, and **requires Babel** 2.2 or higher to be installed.

.. code:: python

    >>> m = Money('1234.567', 'USD')
    >>> m.format('en_US')
    '$1,234.57'
    >>> m.format('es_ES')
    '1.234,57\xa0$'

The character ``\xa0`` is an unicode non-breaking space. If no locale is passed, Babel will use your system's locale. You can also provide a specific pattern to format():

.. code:: python

    >>> m = Money('-1234.567', 'USD')
    >>> # Regular US format:
    >>> m.format('en_US', '¤#,##0.00') 
    '-$1,234.57'
    >>> # Custom negative format:
    >>> m.format('en_US', '¤#,##0.00;<¤#,##0.00>')
    '<$1,234.57>'
    >>> # Spanish format, full currency name:
    >>> m.format('es_ES', '#,##0.00 ¤¤¤')
    '-1.234,57 dólares estadounidenses'
    >>> # Same as above, but rounding (overriding currency natural format):
    >>> m.format('es_ES', '#0 ¤¤¤', currency_digits=False)
    '-1235 dólares estadounidenses'

For more details on formatting see `Babel docs on currency formatting <http://babel.pocoo.org/en/latest/api/numbers.html#babel.numbers.format_currency>`_. To learn more about the formatting pattern syntax check out `Unicode TR35 <http://www.unicode.org/reports/tr35/tr35-numbers.html#Number_Format_Patterns>`_.

Currency exchange
=================

Currency exchange works by "installing" a **backend** class that implements the abstract base class (`abc <https://docs.python.org/3/library/abc.html>`_) ``money.exchange.BackendBase``. Its API is exposed through ``money.xrates``, along with setup functions ``xrates.install(pythonpath)``, ``xrates.uninstall()``, and ``xrates.backend_name``.

A simple proof-of-concept backend ``money.exchange.SimpleBackend`` is included:

.. code:: python

    from decimal import Decimal
    from money import Money, xrates

    xrates.install('money.exchange.SimpleBackend')
    xrates.base = 'USD'
    xrates.setrate('AAA', Decimal('2'))
    xrates.setrate('BBB', Decimal('8'))
    
    a = Money(1, 'AAA')
    b = Money(1, 'BBB')
    
    assert a.to('BBB') == Money('4', 'BBB')
    assert b.to('AAA') == Money('0.25', 'AAA')
    assert a + b.to('AAA') == Money('1.25', 'AAA')



XMoney
======

You can use ``money.XMoney`` (a subclass of Money), for automatic currency conversion while adding, subtracting, and dividing money objects (+, +=, -, -=, /, //). This is useful when aggregating lots of money objects with heterogeneous currencies. The currency of the leftmost object has priority.

.. code:: python

    from money import XMoney
    
    # Register backend and rates as above...
    
    a = XMoney(1, 'AAA')
    b = XMoney(1, 'BBB')
    
    assert sum([a, b]) == XMoney('1.25', 'AAA')


Exceptions
==========

Found in ``money.exceptions``.

``MoneyException(Exception)``
    Base class for all exceptions.

``CurrencyMismatch(MoneyException, ValueError)``
    Thrown when mixing different currencies, e.g. ``Money(2, 'EUR') + Money(2, 'USD')``. Money objects must be converted first to the same currency, or XMoney could be used for automatic conversion.

``InvalidOperandType(MoneyException, TypeError)``
    Thrown when attempting invalid operations, e.g. multiplication between money objects.

``ExchangeError(MoneyException)``
    Base class for exchange exceptions.

``ExchangeBackendNotInstalled(ExchangeError)``
    Thrown if a conversion is attempted, but there is no backend available.

``ExchangeRateNotFound(ExchangeError)``
    The installed backend failed to provide a suitable exchange rate between the origin and target currencies.


Hierarchy
---------

* ``MoneyException``
    * ``CurrencyMismatch``
    * ``InvalidOperandType``
    * ``ExchangeError``
        * ``ExchangeBackendNotInstalled``
        * ``ExchangeRateNotFound``



.. _python-differences:

Differences between Python versions
===================================

.. list-table::
    :header-rows: 1
    :stub-columns: 1
    
    * - Expression
      - Python 2.x
      - Python 3.x
    
    * - ``round(Money('2.5', 'EUR'))``
      - Returns ``3.0``, a **float** rounded amount **away from zero**.
      - Returns ``EUR 2``, a **Money object** with rounded amount to the **nearest even**.
    
    * - ``Money('0', 'EUR').amount < '0'``
      - Returns ``True``. This is the weird but expected behaviour in Python 2.x when comparing Decimal objects with non-numerical objects (Note the '0' is a string). `See note in docs <https://docs.python.org/2/library/stdtypes.html#comparisons>`_.
      - TypeError: unorderable types: decimal.Decimal() > str()



Design decisions
================

There are several design decisions in *money* that differ from currently available money class implementations:

Localization
------------

Do not keep any kind of locale conventions database inside this package. Locale conventions are extensive and change over time; keeping track of them is a project of its own. There is already such a project and database (the Unicode Common Locale Data Repository), and an excellent python API for it: `Babel <https://pypi.python.org/pypi/Babel>`_.

Currency
--------

There is no need for a currency class. A currency is fully identified by its ISO 4217 code, and localization or exchange rates data are expected to be centralized as databases/services because of their changing nature.

Also:

+ **Modulo operator (%)**: do not override to mean "percentage".
+ **Numeric type**: you **can** mix numbers and money in binary operations, and objects evaluate to False if their amount is zero.
+ **Global default currency**: subclassing is a safer solution.


Contributions
=============

Contributions are welcome. You can use the `regular github mechanisms <https://help.github.com/>`_.

To test your changes you will need `tox <https://pypi.python.org/pypi/tox>`_ and python 2.7, 3.4, and 3.5. Simply cd to the package root (by setup.py) and run ``tox``.


License
=======

money is released under the **MIT license**, which can be found in the file ``LICENSE``.




