#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ..reg import reg_object, set_object
from ..reg.result import reg_debug, reg_warning, reg_exception
from .models import File, FileProcessing
from .process import proceed


def reg_file_processing(filename, options, session, DIR=None, HANDLER=None):
    basename = os.path.basename(filename)
    statinfo = os.stat(filename)
    size  = statinfo.st_size
    mtime = statinfo.st_mtime

    # Проверяем, обрабатывался ли файл данным обработчиком
    FILE = None
    PROCESSING = None

    file_dict = dict(_dir=DIR, name=basename)
    rows = session.query(File).filter_by(**file_dict).all()
    if rows:
        l = len(rows)
        if l > 1:
            reg_warning(DIR, "Найдено несколько одинаковых файлов ({0})!".format(l))
    
        for i in rows:
            FILE = set_object(i, DIR)
            setattr(FILE, '_records', l)

            processing_dict = dict(_file=FILE, _handler=HANDLER, size=size, mtime=mtime)
            rows2 = session.query(FileProcessing).filter_by(**processing_dict).all()
            if rows2:
                l2 = len(rows2)
                if l2 > 1:
                    reg_warning(FILE, "Найдено несколько одинаковых обработок файла ({0})!".format(l2))
            
                PROCESSING = set_object(rows2[0], FILE)
                setattr(PROCESSING, '_records', l2)
                break

    if not FILE:
        FILE = reg_object(session, File, file_dict, DIR)

    FILE.size = size
    FILE.mtime = mtime

    if not PROCESSING:
        processing_dict = dict(_file=FILE, _handler=HANDLER, size=size, mtime=mtime)
        PROCESSING = reg_object(session, FileProcessing, processing_dict, FILE)

    return FILE, PROCESSING


def proceed_file(filename, options, session, DIR=None, HANDLER=None):
    FILE, PROCESSING = reg_file_processing(filename, options, session, DIR, HANDLER)

    if hasattr(PROCESSING, '_records'):
        reg_debug(FILE, "Файл уже обработам, пропускаем!")
        if hasattr(FILE, 'tree_item'):
            FILE.tree_item.set_quiet()
        return

    try:
        # Параметр 4: FILE или PROCESSING
        proceed(filename, options, session, PROCESSING)
    except Exception as e:
        reg_exception(FILE, e)
        return
