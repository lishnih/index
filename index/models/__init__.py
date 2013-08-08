#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-01

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )
from lib.backwardcompat import *

import os
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship


DBSession = scoped_session(sessionmaker())
Base = declarative_base()


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
    sh        = Column(String)                  # Аттрибут для возможности передать переменную sh

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if self.sh:
            self.name  = self.sh.name
            self.ncols = self.sh.ncols
            self.nrows = self.sh.nrows
            self.visible = self.sh.visibility
            self.sh = None

    def __unicode__(self):
        return "<Таблица '{0}' ({1})>".format(self.name, self.id)


class Doc(Base, aStr):                          # rev. 20121020
    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)
    _handlers_id = Column(Integer, ForeignKey('handlers.id', onupdate="CASCADE", ondelete="CASCADE"))
    _handler = relationship(Handler, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

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


class Piece(Base, aStr):                        # rev. 20121020
    __tablename__ = 'pieces'
    id = Column(Integer, primary_key=True)

    name       = Column(String)                 # Наименование изделия
    piece_type = Column(String)
    piece_name = Column(String)
    piece_scheme = Column(String)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            name_list = filter(lambda x: x, [self.piece_type, self.piece_name, self.piece_scheme])
            name_list = map(unicode, name_list)
            self.name = " ".join(name_list)

    def __unicode__(self):
        return "<Изделие '{0}' ({1})>".format(self.name, self.id)


class Piece_entry(Base, aStr):                  # rev. 20121020
    __tablename__ = 'piece_entries'
    id = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate='CASCADE', ondelete='CASCADE'))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _pieces_id = Column(Integer, ForeignKey('pieces.id', onupdate='CASCADE', ondelete='CASCADE'))
    _piece = relationship(Piece, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name       = Column(String)                 # Наименование
    piece      = Column(String)
    object     = Column(String)                 # Объект
    scheme     = Column(String)                 # Схема
    mfr        = Column(String)                 # Производитель
    order      = Column(Integer)                # Заказ
    qnt        = Column(Float)                  # Кол-во
    meas       = Column(String)
    invoice    = Column(Integer)                # Т/н
    cert_type  = Column(String)                 # Сертификат
    cert       = Column(Integer)
    y          = Column(Integer)                # y

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            self.name = "{0} [{1}]".format(self.piece, self.y)

    def __unicode__(self):
        return "<Запись изделия '{0}' ({1})>".format(self.name, self.id)


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


class Joint_entry(Base, aStr):                  # rev. 20121020
    __tablename__ = 'joint_entries'

    id = Column(Integer, primary_key=True)
    _sheets_id = Column(Integer, ForeignKey('sheets.id', onupdate='CASCADE', ondelete='CASCADE'))
    _sheet = relationship(Sheet, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _docs_id = Column(Integer, ForeignKey('docs.id', onupdate='CASCADE', ondelete='CASCADE'))
    _doc = relationship(Doc, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))
    _joints_id = Column(Integer, ForeignKey('joints.id', onupdate='CASCADE', ondelete='CASCADE'))
    _joint = relationship(Joint, backref=backref(__tablename__, cascade='all, delete, delete-orphan'))

    name        = Column(String)                # Номер записи
    joint       = Column(String)
    welders     = Column(String(length=255))
    method      = Column(String(length=255))
    d_w_th      = Column(String(length=255))
    defects     = Column(String(length=255))
    report      = Column(String(length=255))
    date        = Column(Integer)
    date_str    = Column(String(length=255))
    decision    = Column(String(length=255))
    y           = Column(Integer)

    def __init__(self, **kargs):
        Base.__init__(self, **kargs)
        if not self.name:
            self.name = "{0} [{1}]".format(self.joint, self.y)

    def __unicode__(self):
        return "<Запись стыка '{0}' ({1})>".format(self.name, self.id)
