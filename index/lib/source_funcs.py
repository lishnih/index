#!/usr/bin/env python
# coding=utf-8
# Stan 2015-06-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, hashlib


def get_source_data(name, s):
    sources = s.get('sources', [])
    default = None

    for i in sources:
        if i[0] == name:
            default = i
            break
        if i[0] == '*':
            default = i

    if default:
        return [i if i else 'default' for i in default]


def get_sha256_module(module):
    filename = module.__file__

    if filename.endswith('.pyc'):
        filename = filename[:-1]

    if not os.path.exists(filename):
        print("File missed: '{0}'".format(filename))

    if filename.endswith('__init__.py'):
        sha256 = get_sha256_dir(os.path.dirname(filename))
    else:
        sha256 = get_sha256_file(filename)

    return sha256


def get_sha256_dir(root):
    sha256 = hashlib.sha256()
    for dirname, dirs, files in os.walk(root):
        for i in files:
            if os.path.splitext(i)[1] == '.py':
                filename = os.path.join(dirname, i)
                sha256.update(open(filename, 'rb').read())

    return sha256.hexdigest()


def get_sha256_file(filename):
    sha256 = hashlib.sha256()
    sha256.update(open(filename, 'rb').read())

    return sha256.hexdigest()
