#!/usr/bin/env python
# coding=utf-8

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os
from setuptools import setup, find_packages

py_version = sys.version_info[:2]
PY3 = py_version[0] == 3
if PY3:
    if py_version < (3, 3):
        raise RuntimeError('On Python 3, Index requires Python 3.3 or better')
else:
    if py_version < (2, 6):
        raise RuntimeError('On Python 2, Index requires Python 2.6 or better')

here = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''


from index import __pkgname__, __description__, __version__


if __name__ == '__main__':
    setup(
        name = __pkgname__,
        description = __description__,
        version = __version__,
        long_description = README,

        author = 'Stan',
        author_email = 'lishnih@gmail.com',
        url = 'https://github.com/lishnih/index',
        platforms = ['any'],
        keywords = ['PySide', 'indexing', 'reporting', 'documents'],

        packages = find_packages(),
#       include_package_data=True,
#       zip_safe=False,

#       package_data = {__pkgname__: []},

        scripts = [
        ],

        install_requires = [
            'PySide',
            'sqlalchemy',
            'yaml',
        ],

        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Win32 (MS Windows)',
            'Environment :: X11 Applications :: Qt',
            'Intended Audience :: Manufacturing',
            'License :: OSI Approved :: MIT License',
            'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
            'Natural Language :: Russian',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Database',
            'Topic :: Utilities',
        ],
    )
