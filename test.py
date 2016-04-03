#!/usr/bin/env python

import sys
import os
import unittest


def main():
    source_dir = 'src'
    # Python 2 backwards compatibility
    if sys.version_info[0] == 2:
        source_dir = 'src-py2'
    
    path_base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path_base, source_dir)
    tests = unittest.defaultTestLoader.discover(path)
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)

if __name__ == '__main__':
    main()