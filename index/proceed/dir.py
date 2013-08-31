#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, re

from models import Dir
from reg import reg_object1


def proceed_dir(dirname, options, session, ROOT=None):
    dir_dict = dict(name=dirname)
    DIR = reg_object1(session, Dir, dir_dict, ROOT, style='B')

    return DIR
