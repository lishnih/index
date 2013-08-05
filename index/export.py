#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-12

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os, logging

from models             import DBSession, Base
from models.db          import initDb
from proceed.dir        import proceed_dir
from proceed.file       import proceed_file
from reg                import set_object
from reg.result         import reg_exception

from lib.settings       import Settings
from lib.data_funcs     import get_list, filter_match, filter_list
from lib.items          import DirItem
from lib.dump           import plain


tracing = []


def ProceedInit(sources, method=None, filename=None, tree_widget=None):
    # Получаем настройки метода
    options = {}
    if method:
        options = Settings(method)
    elif filename:
        options = Settings(filename=filename)

    if not method:
        method = "default"

    root_dict = dict(name="Root")
    ROOT = set_object(root_dict, tree_widget,
           brief = dict(sources=sources, method=method, filename=filename,
                   options=options))
    ROOT.tree_item.setSelected(True)

    dbpath = options.get('dbpath', '.')
    dbname = options.get('dbname', "{0}.sqlite".format(method))
    db_path = os.path.join(dbpath, dbname)
    db_uri_default = u'sqlite:///{0}'.format(db_path)
    db_uri = options.get('db_uri', db_uri_default)
    try:
        initDb(db_uri, DBSession, Base)
    except Exception as e:
        reg_exception(ROOT, e)
        return

    sources = get_list(sources)
    for source in sources:
        Proceed(source, options, ROOT)


def Proceed(source, options=None, ROOT=None):
    filename = os.path.abspath(source)
    filename = filename.replace('\\', '/')    # приводим к стилю Qt

    if os.path.isdir(filename):
        logging.info("Обработка директории '{0}'".format(filename))

        dirs_filter = options.get('dirs_filter')
        files_filter = options.get('files_filter')

        # Dir
        for root, dirs, files in os.walk(filename):
            tracing.append(root)
            DIR = proceed_dir(root, options, ROOT)

            for dirname in dirs:
                if filter_match(dirname, dirs_filter):
                    pass
                else:
                    dirs.remove(dirname)

            files_filtered = filter_list(files, files_filter)

            for filename in files:
                if filename in files_filtered:
                    tracing.append(filename)
    
                    # File
                    filename = os.path.join(root, filename)
                    proceed_file(filename, options, DIR)
                else:
                    set_object(filename, DIR, style='D', brief=u"Этот файл не индексируется!")

    elif os.path.isfile(filename):
        logging.info("Обработка файла '{0}'".format(filename))

        # Dir
        dirname = os.path.dirname(filename)
        DIR = proceed_dir(dirname, options, ROOT)

        # File
        proceed_file(filename, options, DIR)

    else:
        logging.warning("Не найден файл/директория '{0}'!".format(filename))

    try:
        DBSession.commit()
    except Exception as e:    # StatementError
        reg_exception(root, e)


def main(args):
    if args.files:
        ProceedInit(args.files, method=args.method)
    else:
        logging.warning("Файлы не заданы!")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    import argparse
    from lib.argparse_funcs import readable_file_or_dir_list

    parser = argparse.ArgumentParser(description='Indexing files and directories.')
    parser.add_argument('files', action=readable_file_or_dir_list, nargs='*',
                        help='files and directories to proceed')
    parser.add_argument('-m', '--method',
                        help='specify the method name')

    if sys.version_info >= (3,):
        argv = sys.argv
    else:
        fse = sys.getfilesystemencoding()
        argv = [i.decode(fse) for i in sys.argv]

    args = parser.parse_args(argv[1:])

    sys.exit(main(args))
