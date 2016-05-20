#!/usr/bin/env python
# coding=utf-8
# Stan 2012-04-08

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os

from ...reg import reg_object, set_object
from ...reg.result import reg_debug, reg_warning, reg_exception
from .process import proceed


def reg_file_processing(filename, runtime, DIR=None, HANDLER=None):
    model = runtime.get('m_module')
    session = runtime.get('session')

    basename = os.path.basename(filename)
    statinfo = os.stat(filename)
    size  = statinfo.st_size
    mtime = statinfo.st_mtime

    # Проверяем, обрабатывался ли файл данным обработчиком
    FILE = None
    PROCESSING = None

    file_dict = dict(_dir=DIR, name=basename)
    rows = session.query(model.File).filter_by(**file_dict).all()
    if rows:
        l = len(rows)
        if l > 1:
            reg_warning(DIR, "Найдено несколько одинаковых файлов ({0})!".format(l))
    
        for i in rows:
            FILE = set_object(i, DIR)

            processing_dict = dict(_file=FILE, _handler=HANDLER, size=size, mtime=mtime)
            rows2 = session.query(model.FileProcessing).filter_by(**processing_dict).all()
            if rows2:
                l2 = len(rows2)
                if l2 > 1:
                    reg_warning(FILE, "Найдено несколько одинаковых обработок файла ({0})!".format(l2))
            
                for i in rows2:
                    PROCESSING = set_object(i, FILE)

    if not FILE:
        FILE = reg_object(session, model.File, file_dict, DIR)

    # Обновляем время модификации и размер файла
    FILE.size = size
    FILE.mtime = mtime

    if not PROCESSING:
        processing_dict = dict(_file=FILE, _handler=HANDLER, size=size, mtime=mtime)
        PROCESSING = reg_object(session, model.FileProcessing, processing_dict, FILE)

    return FILE, PROCESSING


def proceed_file(filename, runtime, DIR=None, HANDLER=None):
    FILE, PROCESSING = reg_file_processing(filename, runtime, DIR, HANDLER)

    if PROCESSING.status > 0:
        reg_debug(FILE, "Файл уже обработам, пропускаем!")
        if hasattr(FILE, 'tree_item'):
            FILE.tree_item.set_quiet()
        return

    try:
        # Параметр 3: FILE или PROCESSING
        proceed(filename, runtime, PROCESSING)
        PROCESSING.status = 1
    except Exception as e:
        reg_exception(FILE, e)
        PROCESSING.status = -1
        return
