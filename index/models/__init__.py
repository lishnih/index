#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship


Base = declarative_base()
class aStr():
    def __str__(self):
        return self.__unicode__()


class Handler(Base, aStr):                      # rev. 20130730
    __tablename__ = 'handlers'
    id = Column(Integer, primary_key=True)

    name      = Column(String)                  # Имя обработчика
    status    = Column(Integer)                 # Состояние
    created   = Column(Integer, default=datetime.utcnow)  # Время создания
    updated   = Column(Integer, onupdate=datetime.utcnow) # Время обновления
    options   = Column(String)                  # для пакета index

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __unicode__(self):
        return "<Обработчик '{0}' ({1})>".format(self.name, self.id)


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

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if os.path.isfile(self.name):
            statinfo   = os.stat(self.name)
            self.size  = statinfo.st_size
            self.mtime = statinfo.st_mtime

            if self._dir:
                self.name = os.path.basename(self.name)

    def __unicode__(self):
        return "<Файл '{0}' ({1})>".format(self.name, self.id)


class Sheet(Base, aStr):                        # rev. 20120913
    __tablename__ = 'sheets'
    id = Column(Integer, primary_key=True)
    _files_id = Column(Integer, ForeignKey('files.id', onupdate="CASCADE", ondelete="CASCADE"))
    _file = relationship(File, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name      = Column(String)                  # Имя листа
    seq       = Column(Integer)                 # Номер листа в файле
    ncols     = Column(Integer)                 # Кол-во колонок в листе
    nrows     = Column(Integer)                 # Кол-во строк в листе
    visible   = Column(Integer)                 # Видимость листа

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __unicode__(self):
        return "<Таблица '{0}' ({1})>".format(self.name, self.id)


class Doc(Base, aStr):                          # rev. 20130907
    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)
    _handlers_id = Column(Integer, ForeignKey('handlers.id', onupdate="CASCADE", ondelete="CASCADE"))
    _handler = relationship(Handler, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate="CASCADE", ondelete="CASCADE"))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name       = Column(String)                 # Номер документа
    doc_pre    = Column(String)
    doc_seq    = Column(Integer)
    doc_sign   = Column(String)
    type       = Column(String)
    date       = Column(Integer)                # Дата
    date_str   = Column(String)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.doc_pre, self.doc_seq])
            name_list = map(unicode, name_list)
            self.name = "/".join(name_list)
            if self.doc_sign:
                self.name += ' ' + format(self.doc_sign)

    def __unicode__(self):
        return "<Документ '{0}' ({1})>".format(self.name, self.id)


class Unit(Base, aStr):                         # rev. 20130907
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)

    name       = Column(String)                 # Наименование изделия
    extra      = Column(String)

#   def __init__(self, **kargs):
#       Base.__init__(self, **kargs)

    def __unicode__(self):
        return "<Изделие '{0}' ({1})>".format(self.name, self.id)


class Joint(Base, aStr):                        # rev. 20121015
    __tablename__ = 'joints'
    id = Column(Integer, primary_key=True)

    name        = Column(String)                # Номер стыка
#   joint_kind  = Column(String)
    joint_pre   = Column(String)
    joint_line  = Column(String)
    joint_seq   = Column(Integer)
#   joint_sign  = Column(String)
    diameter1   = Column(Integer)
    diameter2   = Column(Integer)
    thickness1  = Column(Float)
    thickness2  = Column(Float)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.joint_pre, self.joint_line, self.joint_seq])
            name_list = map(unicode, name_list)
            self.name = "-".join(name_list)
#             if self.joint_sign:
#                 self.name += ' ' + format(self.joint_sign)

    def __unicode__(self):
        return "<Стык '{0}' ({1})>".format(self.name, self.id)


class Entry(Base, aStr):                        # rev. 20130907
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _unites_id = Column(Integer, ForeignKey('units.id', onupdate='CASCADE', ondelete='CASCADE'))
    _unit = relationship(Unit, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name       = Column(String)                 # Наименование
    y          = Column(Integer)                # y

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            self.name = "{0} / {1} [{2}]".format(self._unit.name, self._doc.name, self.y)

    def __unicode__(self):
        return "<Запись в листе '{0}' ({1})>".format(self.name, self.id)


class Joint_entry(Base, aStr):                  # rev. 20130907
    __tablename__ = 'joint_entries'
    id = Column(Integer, primary_key=True)
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _joints_id = Column(Integer, ForeignKey('joints.id', onupdate='CASCADE', ondelete='CASCADE'))
    _joint = relationship(Joint, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name       = Column(String)                 # Наименование
    y          = Column(Integer)                # y

#     def __init__(self, **kargs):
#         Base.__init__(self, **kargs)
#         if not self.name:
#             self.name = "{0} / {1} [{2}]".format(self._joint.name, self._doc.name, self.y)

    def __unicode__(self):
        return "<Запись в листе '{0}' ({1})>".format(self.name, self.id)
