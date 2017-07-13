.. RADAR: version


1.4
===

+ Merged Python 2 and 3 sources.


1.3
===

1.3.0 (2016-04-17)
------------------

+ Migrated to Babel 2.2 or higher. New CLDR and new API for ``babel.numbers.format_currency()`` (reported by `chrisrossi <https://github.com/chrisrossi>`_).

+ Dropped support for Python 3.3

+ XMoney now only attempts automatic currency conversion in addition, substraction, and division.

  Before, XMoney would convert currencies in comparison, including >= and <=, with results that were inconsistent with ==.

+ Comparison operators ``<``, ``<=``, ``>``, ``>=`` now throw ``InvalidOperandType`` (TypeError) if the operand is not a Money object. Code that relies on this should be updated to access the amount value explicitly (see example below).

.. code:: python

    >>> m = Money(2, 'USD')
    
    # old code
    >>> m > 1
    (raises InvalidOperandType)
    
    # 1.3.x
    >>> m.amount > Money(1, 'USD')
    True

+ '0' is consider a valid money amount for math and comparison.


1.2
===

1.2.3 (2016-04-17)
------------------

+ Throw an exception if used with Babel 2.2 or higher (reported by `chrisrossi <https://github.com/chrisrossi>`_).


1.2.2 (2015-06-09)
------------------

+ Added support for SQLAlchemy composite columns (by `dahlia <https://github.com/dahlia>`_)


1.2.1 (2014-06-15)
------------------

+ Fixed bug in `__rsub__()` (fix by `zedlander <https://github.com/zedlander>`_)


1.2.0 (2014-04-30)
------------------

+ **Multiplication between a Money object and a float does not implicitly convert the float to a Decimal anymore.** (reported by `spookylukey <https://github.com/spookylukey>`_)


1.1
===

1.1.1 (2014-06-15)
------------------

+ Fixed bug in `__rsub__()` (fix by `zedlander <https://github.com/zedlander>`_)


1.1.0 (2014-04-01)
------------------

+ Added tox testing (requested by `kvesteri <https://github.com/kvesteri>`_)
+ Compatible with Python 2.7, 3.3, 3.4 (requested by `kvesteri <https://github.com/kvesteri>`_)


1.0
===

1.0.2 (2013-11-25)
------------------

+ Initial stable version
+ Compatible with Python 3.3


