import sys
from distutils.core import setup


DESCRIPTION = """
Python money class with optional CLDR-backed locale-aware formatting 
and an extensible currency exchange solution.
"""

SOURCE_ROOT = 'src'

# Python 2 backwards compatibility
if sys.version_info[0] == 2:
    SOURCE_ROOT = 'src-py2'


setup(
    name='money',
    description='Python Money Class',
    # long_description=DESCRIPTION,
    version='1.2.1',
    author='Carlos Palol',
    author_email='carlos.palol@awarepixel.com',
    url='https://github.com/carlospalol/money',
    license='MIT',
    package_dir={'': SOURCE_ROOT},
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
        'Topic :: Software Development :: Libraries',
    ]
)
