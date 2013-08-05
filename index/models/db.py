#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, shutil, logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def initDb(db_uri=None, session=None, base=None):
    if not db_uri:
        db_uri = getDefaultDb()
    if not session:
        session = scoped_session(sessionmaker())

    engine = create_engine(db_uri)

    if engine.name == 'sqlite':
        filename = engine.url.database
        if filename:
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            if not os.path.isdir(dirname):
                logging.error("Невозможно создать директорию '{0}'".format(dirname))
                return

    session.configure(bind=engine)
    if base:
        base.metadata.create_all(engine)

    return session


def getDefaultDb():
    dbname = "index"
    home = os.path.expanduser("~")
    db_path = os.path.join(os.path.expanduser("~"), "{0}.sqlite".format(dbname))
    db_uri = 'sqlite:///{0}'.format(db_path)
#   db_uri = 'mysql+oursql://root:54321@localhost/{0}'.format(dbname)

    return db_uri


def cleanDb(engine):
    pass


def archiveDb(engine):
    if engine.name == 'sqlite':
        filename = engine.url.database
        archivefile(filename)
    else:
        logging.warning("Для данного типа БД архивирование не предусмотрено: {0}, пропускаем архивирование!".format(engine.name))


def archiveFile(filename):
    if os.path.isfile(filename):
        timestamp = int(os.path.getmtime(filename))

        dirname   = os.path.dirname(filename)
        basename  = os.path.basename(filename)
        root, ext = os.path.splitext(basename)

        basename_new = "{0}_{1}{2}".format(root, timestamp, ext)
        dirname_new  = os.path.join(dirname, "backup")
        if not os.path.exists(dirname_new):
            os.makedirs(dirname_new)
        filename_new = os.path.join(dirname_new, basename_new)
        shutil.copy(filename, filename_new)
