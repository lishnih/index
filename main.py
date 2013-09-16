#!/usr/bin/env python
# coding=utf-8
# Stan 2013-09-15

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, argparse, logging

from index.main import main
from index.lib.argparse_funcs import readable_file_or_dir_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

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