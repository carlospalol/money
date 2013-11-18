
============
Python Money
============

Money class with optional CLDR-backed locale-aware formatting and an extensible currency exchange solution.


Installation
============

*money* requires python 3.3

::

    pip install --pre money

For locale-aware formatting, also install `Babel <https://pypi.python.org/pypi/Babel>`_:

::

    pip install babel


Basic usage
===========

.. code:: python

    >>> from money import Money
    >>> m = Money(amount='2.22', currency='EUR')
    >>> m
    EUR 2.22

*amount* can be any valid value for decimal.Decimal(value) and *currency* should be a three-letter currency code. You can perform most arithmetic operations between money objects and/or numbers (int, float, Decimal).

.. code:: python

    >>> from money import Money
    >>> m = Money('2.22', 'EUR')
    >>> m / 2
    EUR 1.11
    >>> m + Money('7.77', 'EUR')
    EUR 9.99


Formatting
==========

Money objects are printed by default with en_US formatting and the currency code.

.. code:: python

    >>> m = Money('1234.567', 'EUR')
    >>> str(m)
    'EUR 1,234.57'

Use ``format(locale=DEFAULT_LC_NUMERIC, pattern=None)`` for locale-aware formatting with currency expansion. ``format()`` emulates ``babel.numbers.format_currency()``, and **requires Babel** to be installed:

.. code:: python

    >>> m = Money('1234.567', 'USD')
    >>> m.format('en_US')
    '$1,234.57'
    >>> m.format('es_ES')
    '1.234,57\xa0US$'

The character ``\xa0`` is an unicode non-breaking space. If no locale is passed, Babel will use your system's locale. You can also provide a specific pattern to format():

.. code:: python

    >>> m = Money('-1234.567', 'USD')
    >>> # Regular US format:
    >>> m.format('en_US', '¤#,##0.00') 
    '-$1,234.57'
    >>> # Custom negative format:
    >>> m.format('en_US', '¤#,##0.00;<¤#,##0.00>')
    '<$1,234.57>'
    >>> # Round, Spanish format, full currency name:
    >>> m.format('es_ES', '0 ¤¤¤')
    '-1235 dólares estadounidenses'


`Learn more about the formatting syntaxis <http://www.unicode.org/reports/tr35/tr35-numbers.html#Number_Format_Patterns>`_.


Currency exchange
=================

Currency exchange works by "installing" a **backend** class that implements the abstract base class (`abc <http://docs.python.org/3.3/library/abc.html>`_) ``money.exchange.BackendBase``. Its API is exposed through ``money.xrates``, along with setup functions ``xrates.install(pythonpath)``, ``xrates.uninstall()``, and ``xrates.backend_name``.

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

You can use a subclass of Money, **XMoney** if you prefer automatic conversion between different currencies on binary operations. The currency of the leftmost object has priority.

.. code:: python

    from money import XMoney
    
    # Register backend and rates as above...
    
    a = XMoney(1, 'AAA')
    b = XMoney(1, 'BBB')

    assert a + b == XMoney('1.25', 'AAA')


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


License
=======

money is released under the **MIT license**, which can be found in the file ``LICENSE``.




