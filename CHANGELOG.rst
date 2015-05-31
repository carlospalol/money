

1.3
===

1.3.0
-----

2015-05-31

+ Dropped support for Python 3.3
+ Comparison operators ``<``, ``<=``, ``>``, ``>=`` now throw ``InvalidOperandType`` (TypeError) if the operand is not a Money object. Code that relies on this should be updated to access the amount value explicitly (see example below). 

.. code:: python

	>>> m = Money(2, 'USD')
	
	# old code
	>>> m > 0
	(raises InvalidOperandType)
	
	# 1.3.x
	>>> m.amount > 0
	True


1.2
===

1.2.1
-----

2014-06-15

+ Fixed bug in `__rsub__()` (fix by zedlander)

1.2.0
-----

2014-04-30

+ **Multiplication between a Money object and a float does not implicitly convert the float to a Decimal anymore.** (reported by spookylukey)


1.1
===

1.1.1
-----

2014-06-15

+ Fixed bug in `__rsub__()` (fix by zedlander)

1.1.0
-----

2014-04-01

+ Added tox testing (requested by kvesteri)
+ Compatible with Python 2.7, 3.3, 3.4 (requested by kvesteri)


1.0
===

1.0.2
-----

2013-11-25

+ Initial stable version
+ Compatible with Python 3.3

