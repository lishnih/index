#!/usr/bin/env python
# coding=utf-8
# Stan 2015-06-03

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

from ..lib.backwardcompat import *
from ..lib.items import DirItem, FileItem


def view_conf(tree_widget, settings):
    table_item = DirItem(tree_widget, "Settings", brief=settings.settings)
    table_item = DirItem(tree_widget, "System", brief=settings.system)

#   for key, value in settings:
#       table_item = FileItem(tree_widget, key, brief=value)

    table_item.setExpanded(True)
