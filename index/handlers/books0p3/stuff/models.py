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


class Sheet(Base, aStr):                        # rev. 20160424
    __tablename__ = 'sheets'
    __table_args__ = {'mysql_engine': 'MyISAM', 'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate="CASCADE", ondelete="CASCADE"))
    _file = relationship(File, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

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
