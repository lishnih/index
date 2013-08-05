#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

import os, re

from reg import reg_object1
from models import Dir


def proceed_dir(dirname, options, ROOT=None):
    dir_dict = dict(name=dirname)
    DIR = reg_object1(Dir, dir_dict, ROOT, style='B')

    return DIR
