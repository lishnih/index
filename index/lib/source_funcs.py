#!/usr/bin/env python
# coding=utf-8
# Stan 2015-06-07

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os


def get_source_data(name, s):
    sources = s.get('sources')
    default = None

    name = os.path.abspath(name)
    name = name.replace('\\', '/')

    for i in sources:
        if i[0] == name:
            default = i
            break
        if i[0] == '*':
            default = i

    if default:
        return [i if i else 'default' for i in default]
