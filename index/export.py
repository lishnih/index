#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, importlib, logging

from lib.settings import Settings
from lib.data_funcs import get_list
from db import initDb, initlinks, foreign_keys, foreign_keys_c
from reg import set_object
from reg.result import reg_error, reg_exception


def Proceed(sources, options={}, tree_widget=None, status=None):
    ROOT = set_object("/", tree_widget, brief=options)
    if hasattr(ROOT, 'tree_item'):
        ROOT.tree_item.setSelected(True)

    # Загружаем обработчик
    handler = options.get('handler', "proceed_default")
    handler_path = options.get('handler_path')

    # Добавляем handler_path в sys.path
    if handler_path:
        if not os.path.isdir(handler_path):
            reg_error(ROOT, "handler_path not exists: '{0}'".format(handler_path))
            return

        sys.path.append(handler_path)

    # Загружаем необходимые модули
    try:
        handler_module = importlib.import_module(handler)
        models_module  = importlib.import_module('.models', handler)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    # Извлекаем handler_path из sys.path
    if handler_path:
        sys.path.pop()

    if not hasattr(handler_module, 'proceed'):
        reg_error(ROOT, "No 'proceed' function in handler '{0}'".format(handler))
        return

    # Инициализируем БД
    dbconfig = options.get('db', {})
    try:
        session = initDb(dbconfig, base=models_module.Base)
        initlinks(models_module.Base)

        set_object("session", tree_widget, brief=session)
#       set_object("foreign_keys", tree_widget, brief=foreign_keys)
#       set_object("foreign_keys_c", tree_widget, brief=foreign_keys_c)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    if isinstance(status, dict):
        status['dirs']  = 0
        status['files'] = 0

    # Производим обработку
    sources = get_list(sources)
    for source in sources:
        handler_module.proceed(source, options, session, ROOT, status)

    if isinstance(status, dict) and 'break' in status:
        status.pop('break')

    # Завершаем транзакции
    try:
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)



def main(args):
    if args.files:
        if args.method:
            s = Settings()
            profiles = s.get_group('profiles')
            if profiles.contains(args.method, dict):
                options = profiles.get_group(args.method).get_dict()

            else:
                text = "Required method not exists: '{0}'!".format(args.method)
                logging.warning(text)
                return

        else:
            options = {}

        Proceed(args.files, options)

    else:
        logging.warning("Files not specified!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import argparse
    from lib.argparse_funcs import readable_file_or_dir_list

    parser = argparse.ArgumentParser(description="Indexing files and directories.")
    parser.add_argument('files', action=readable_file_or_dir_list, nargs='*',
                        help="files and directories to proceed")
    parser.add_argument('-m', '--method',
                        help='specify the method name')

    if sys.version_info >= (3,):
        argv = sys.argv
    else:
        fse = sys.getfilesystemencoding()
        argv = [i.decode(fse) for i in sys.argv]

    args = parser.parse_args(argv[1:])

    sys.exit(main(args))
