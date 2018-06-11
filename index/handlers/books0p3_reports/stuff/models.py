#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import sys
import os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship


Base = declarative_base()
if sys.version_info >= (3,):
    class aStr():
        def __str__(self):
            return self.__unicode__()
else:
    class aStr():
        def __str__(self):
            return self.__unicode__().encode('utf-8')


String = String(length=255)


class Dir(Base, aStr):                          # rev. 20150711
    __tablename__ = 'dirs'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name      = Column(String)                  # Имя директории
    location  = Column(String)                  # Имя компьютера
#   status    = Column(Integer)                 # Состояние

#   def __init__(self, **kargs):
#       kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
#       Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Директория '{0}' ({1})>".format(self.name, self.id)


class File(Base, aStr):                         # rev. 20150711
    __tablename__ = 'files'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _dirs_id = Column(Integer, ForeignKey('dirs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _dir = relationship(Dir, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя файла
    size      = Column(Integer)                 # Размер
    mtime     = Column(Integer)                 # Время модификации
#   status    = Column(Integer)                 # Состояние

#   def __init__(self, **kargs):
#       kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
#       Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Файл '{0}' ({1})>".format(self.name, self.id)


class Handler(Base, aStr):                      # rev. 20150608
    __tablename__ = 'handlers'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name      = Column(String)                  # Имя обработчика
    rev       = Column(Integer)                 # Ревизия
    hash      = Column(String)                  # Hash
    disabled  = Column(Integer)                 # Состояние
    created   = Column(Integer, default=datetime.utcnow)   # Время создания
    updated   = Column(Integer, onupdate=datetime.utcnow)  # Время обновления
    extras    = Column(PickleType)              # Параметры

#   def __init__(self, **kargs):
#       kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
#       Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Обработчик '{0}' ({1})>".format(self.name, self.id)


class FileProcessing(Base, aStr):               # rev. 20130924
    __tablename__ = 'fileprocessings'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate='CASCADE', ondelete='CASCADE'))
    _file = relationship(File, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _handlers_id = Column(Integer, ForeignKey('handlers.id', onupdate='CASCADE', ondelete='CASCADE'))
    _handler = relationship(Handler, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    size      = Column(Integer)                 # Размер файла при обработке
    mtime     = Column(Integer)                 # Время модификации при обработке
    status    = Column(Integer)                 # Состояние

#   def __init__(self, **kargs):
#       kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
#       Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Обработка файла '{0}' обработчиком '{1}' ({2})>".format(self._file.name, self._handler.name, self.id)


class Sheet(Base, aStr):                        # rev. 20120924
    __tablename__ = 'sheets'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate="CASCADE", ondelete="CASCADE"))
    _file = relationship(File, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _fileprocessings_id = Column(Integer, ForeignKey('fileprocessings.id', onupdate="CASCADE", ondelete="CASCADE"))
    _fileprocessing = relationship(FileProcessing, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя листа
    seq       = Column(Integer)                 # Номер листа в файле
    ncols     = Column(Integer)                 # Кол-во колонок в листе
    nrows     = Column(Integer)                 # Кол-во строк в листе
    visible   = Column(Integer)                 # Видимость листа

#   def __init__(self, **kargs):
#       kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
#       Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Таблица '{0}' ({1})>".format(self.name, self.id)


class Doc(Base, aStr):                          # rev. 20150715
    __tablename__ = 'docs'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate="CASCADE", ondelete="CASCADE"))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Номер документа
    doc_pre   = Column(String)                  # Префикс
    doc_seq   = Column(Integer)                 # Номер
    doc_sign  = Column(String)                  # Суффикс
    kind      = Column(String)                  # Форма документа
    type      = Column(String)                  # Тип документа
    date      = Column(Integer)                 # Дата
    date_str  = Column(String)                  # Дата (строка)

    def __init__(self, **kargs):
        kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
        Base.__init__(self, **kargs_reg)

        if 'doc' in kargs:
            self.name = kargs['doc']

        if not self.name:
            name_list = filter(lambda x: x, [self.doc_pre, self.doc_seq, self.doc_sign])
            name_list = map(unicode, name_list)
            self.name = " ".join(name_list)

    def __unicode__(self):
        return "<Документ '{0}' ({1})>".format(self.name, self.id)


class Unit(Base, aStr):                         # rev. 20130924
    __tablename__ = 'units'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name      = Column(String)                  # Наименование изделия
    kind      = Column(String)                  # Форма изделия
    type      = Column(String)                  # Тип изделия
    extras    = Column(PickleType)              # Доп. данные

    def __init__(self, **kargs):
        kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
        Base.__init__(self, **kargs_reg)

        if 'unit' in kargs:
            self.name = kargs['unit']

    def __unicode__(self):
        return "<Изделие '{0}' ({1})>".format(self.name, self.id)


class Joint(Base, aStr):                        # rev. 20150715
    __tablename__ = 'joints'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)

    name        = Column(String)                # Номер стыка
    joint_pre1  = Column(String)                # Префикс 1
    joint_pre2  = Column(String)                # Префикс 2
    joint_seq   = Column(Integer)               # Номер
    joint_sign1 = Column(String)                # Суффикс 1
    joint_sign2 = Column(String)                # Суффикс 2
    diameter1   = Column(Float)                 # Диаметр 1го наименования
    diameter2   = Column(Float)                 # Диаметр 2го наименования
    thickness1  = Column(Float)                 # Толщина 1го наименования
    thickness2  = Column(Float)                 # Толщина 2го наименования
    welders     = Column(String)                # Сварщики
    extras      = Column(PickleType)            # Доп. данные

    def __init__(self, **kargs):
        kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
        Base.__init__(self, **kargs_reg)

        if 'joint' in kargs:
            self.name = kargs['joint']

        if not self.name:
            name_list = filter(lambda x: x, [self.joint_pre1, self.joint_pre2, self.joint_seq, self.joint_sign1, self.joint_sign2])
            name_list = map(unicode, name_list)
            self.name = " ".join(name_list)

    def __unicode__(self):
        return "<Стык '{0}' ({1})>".format(self.name, self.id)


class Entry(Base, aStr):                        # rev. 20160425 - Сабетта
    __tablename__ = 'entries'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _unites_id = Column(Integer, ForeignKey('units.id', onupdate='CASCADE', ondelete='CASCADE'))
    _unit = relationship(Unit, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate="CASCADE", ondelete="CASCADE"))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    y         = Column(Integer)                 # Строка
    extras    = Column(PickleType)              # Доп. данные

    dir       = Column(String)                  # Объект
    file      = Column(String)                  # Объект
    unit      = Column(String)                  # Объект
    thickness = Column(Integer)                 # Толщина
    joint1    = Column(String)                  # Стык 1
    joint2    = Column(String)                  # Стык 2
    joint3    = Column(String)                  # Стык 3
    joint4    = Column(String)                  # Стык 4
    lock1     = Column(String)                  # Замок 1
    lock2     = Column(String)                  # Замок 2
    patch     = Column(String)                  # Накладка
    date      = Column(String)                  # Дата
    remark1   = Column(String)                  # Примечание 1
    remark2   = Column(String)                  # Примечание 2
    remark3   = Column(String)                  # Примечание 3
    remark4   = Column(String)                  # Примечание 4
    remark5   = Column(String)                  # Примечание 5
    remark6   = Column(String)                  # Примечание 6
    remark7   = Column(String)                  # Примечание 7
    remark8   = Column(String)                  # Примечание 8
    remark9   = Column(String)                  # Примечание 9
    remark10  = Column(String)                  # Примечание 10

    def __init__(self, **kargs):
        kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
        Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Запись изделия '{0}' ({1})>".format(self._unit.name, self.id)


class Joint_entry(Base, aStr):                  # rev. 20160424
    __tablename__ = 'joint_entries'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _joints_id = Column(Integer, ForeignKey('joints.id', onupdate='CASCADE', ondelete='CASCADE'))
    _joint = relationship(Joint, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate="CASCADE", ondelete="CASCADE"))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    y         = Column(Integer)                 # Строка
    decision  = Column(String)                  # Заключение
    remarks   = Column(String)                  # Примечания
    extras    = Column(PickleType)              # Доп. данные

    def __init__(self, **kargs):
        kargs_reg = {key: value for key, value in kargs.items() if hasattr(self, key)}
        Base.__init__(self, **kargs_reg)

    def __unicode__(self):
        return "<Запись стыка '{0}' ({1})>".format(self._joint.name, self.id)
