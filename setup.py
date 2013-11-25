from distutils.core import setup


DESCRIPTION = """
Python money class with optional CLDR-backed locale-aware formatting and an extensible currency exchange solution.
"""

setup(
    name='money',
    description='Python Money Class',
    long_description=DESCRIPTION,
    version='1.0',
    author='Carlos Palol',
    author_email='carlos.palol@awarepixel.com',
    url='https://github.com/carlospalol/money',
    license='MIT',
    packages=[
        'money',
        'money.tests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries',
    ]
)
