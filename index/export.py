#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, importlib, logging

from lib.data_funcs import get_list
from models         import Base
from models.db      import initDb
from models.links   import initlinks, foreign_keys, foreign_keys_c
from reg            import set_object
from reg.result     import reg_error, reg_exception


def ProceedInit(sources, options={}, tree_widget=None, status=None):
    root_dict = dict(name="Root")
    ROOT = set_object(root_dict, tree_widget, brief=options)
    ROOT.tree_item.setSelected(True)

    dbconfig = options.get('db', {})
    try:
        session = initDb(dbconfig, base=Base)
        initlinks(Base)
        ROOT.tree_item.appendBrief([session, foreign_keys, foreign_keys_c])
    except Exception as e:
        reg_exception(ROOT, e)
        return

    if isinstance(status, dict):
        status['dirs']  = 0
        status['files'] = 0

    Proceed(sources, options, session, ROOT, status)


def Proceed(sources, options={}, session=None, ROOT=None, status=None):
    ver = options.get('ver', 1)
    proceed_name = "proceed{0}".format(ver)

    try:
        proceed_module = importlib.import_module(proceed_name)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    if not hasattr(proceed_module, 'proceed'):
        reg_error(ROOT, "No 'proceed' function in module '{0}'".format(proceed_name))
        return

    sources = get_list(sources)
    for source in sources:
        proceed_module.proceed(source, options, session, ROOT, status)

    try:
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)



def main(args):
    if args.files:
        ProceedInit(args.files, method=args.method)
    else:
        logging.warning("Файлы не заданы!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import argparse
    from lib.argparse_funcs import readable_file_or_dir_list

    parser = argparse.ArgumentParser(description="Indexing files and directories.")
    parser.add_argument('files', action=readable_file_or_dir_list, nargs='*',
                        help="files and directories to proceed")

    if sys.version_info >= (3,):
        argv = sys.argv
    else:
        fse = sys.getfilesystemencoding()
        argv = [i.decode(fse) for i in sys.argv]

    args = parser.parse_args(argv[1:])

    sys.exit(main(args))
