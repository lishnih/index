#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, importlib, logging

from lib.data_funcs import get_list
from db             import initDb, initlinks, foreign_keys, foreign_keys_c
from reg            import set_object
from reg.result     import reg_error, reg_exception


def Proceed(sources, options={}, tree_widget=None, status=None):
    root_dict = dict(name="Root")
    ROOT = set_object(root_dict, tree_widget, brief=options)
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
        if hasattr(ROOT, 'tree_item'):
            ROOT.tree_item.appendBrief([session, foreign_keys, foreign_keys_c])
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

    # Завершаем транзакции
    try:
        session.commit()
    except Exception as e:
        reg_exception(ROOT, e)



def main(args):
    if args.files:
        Proceed(args.files)
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
