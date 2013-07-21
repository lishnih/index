import os
import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]

PY3 = py_version[0] == 3

if PY3:
    if py_version < (3, 3):
        raise RuntimeError('On Python 3, Index requires Python 3.2 or better')
else:
    if py_version < (2, 6):
        raise RuntimeError('On Python 2, Index requires Python 2.6 or better')

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires=[
    'setuptools',
     ]


if __name__ == '__main__':
    setup(
        name='index',
        version='0.2',
        url='http://github.com/lishnih/index',
        license='MIT',
        author='Stan',
        author_email='lishnih@gmail.com',
        description=('Document Index'),
        long_description=__doc__,
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires = install_requires,
        platforms='any',
        keywords='PySide indexing reports documents',
        classifiers=[
            'Environment :: Web Environment',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
        ],
    )
