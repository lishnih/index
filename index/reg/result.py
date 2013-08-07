#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging, traceback


def reg_debug(OBJ, msg=None):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.appendBrief(msg, once=True)
    else:
        logging.debug(msg)


def reg_ok(OBJ, msg=None):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setOk(msg)
    else:
        logging.info(msg)


def reg_warning(OBJ, msg=None):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setWarning(msg)
    else:
        logging.warning(msg)


def reg_error(OBJ, msg=None, *args, **kargs):
    msg = """(((((((
Ошибка '{0}'!
Были переданый следующие параметры:
args: {1!r}
kargs: {2!r}
)))))))\n""".format(msg, args, kargs)

    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setError(msg)
    else:
        logging.error(msg)


def reg_exception(OBJ, e, *args, **kargs):
    tb_msg = traceback.format_exc()

    msg = """(((((((
Ошибка '{0}'!
Были переданый следующие параметры:
args: {1!r}
kargs: {2!r}
===\n""".format(e, args, kargs)
    try:    msg += tb_msg
    except: msg += repr(tb_msg)
    msg += ")))))))\n"

    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.setError(msg)
    else:
        logging.exception(msg)


def set_bold(OBJ):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.set_bold()


def set_italic(OBJ):
    if OBJ and hasattr(OBJ, 'tree_item'):
        OBJ.tree_item.set_italic()
