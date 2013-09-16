#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import sys, os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
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


class Dir(Base, aStr):                          # rev. 20130730
    __tablename__ = 'dirs'

    id = Column(Integer, primary_key=True)

    name      = Column(String)                  # Имя директории
    location  = Column(String)                  # Имя компьютера
    status    = Column(Integer)                 # Состояние

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __unicode__(self):
        return "<Директория '{0}' ({1})>".format(self.name, self.id)


class File(Base, aStr):                         # rev. 20130730
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    _dirs_id = Column(Integer, ForeignKey('dirs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _dir = relationship(Dir, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя файла
    size      = Column(Integer)                 # Размер
    mtime     = Column(Integer)                 # Время модификации
    status    = Column(Integer)                 # Состояние

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __unicode__(self):
        return "<Файл '{0}' ({1})>".format(self.name, self.id)
