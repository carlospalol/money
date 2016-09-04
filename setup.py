import sys
from distutils.core import setup


DESCRIPTION = """
Python money class with optional CLDR-backed locale-aware formatting 
and an extensible currency exchange solution.
"""


setup(
    name='money',
    description='Python Money Class',
    # long_description=DESCRIPTION,
    # RADAR: version
    version='1.4.0-dev',
    author='Carlos Palol',
    author_email='carlos.palol@awarepixel.com',
    url='https://github.com/carlospalol/money',
    license='MIT',
    packages=[
        'money',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ]
)
