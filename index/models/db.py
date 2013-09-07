#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, shutil, logging
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def initDb(config=None, session=None, base=None):
    db_uri = getDbUri(config)
    engine = create_engine(db_uri)

    if engine.name == "sqlite":
        filename = engine.url.database
        if filename:
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            if not os.path.isdir(dirname):
                logging.error("Невозможно создать директорию '{0}'".format(dirname))
                return

    if not session:
        session = scoped_session(sessionmaker())
    session.configure(bind=engine)

    if base:
        base.metadata.create_all(engine)

    return session


def getDbUri(config={}):
    db_uri = config.get("db_uri")
    if not db_uri:
        dbtype = config.get("dbtype", "sqlite")
    
        if dbtype == "sqlite":
            dbname = config.get("dbname", os.path.expanduser("~/default.sqlite"))
            db_uri = "{0}:///{1}".format(dbtype, dbname)
    
        elif dbtype == "mysql":
            dbtype = config.get("dbtype", "mysql")
            dbname = config.get("dbname", "default")
            host   = config.get("host",   "localhost")
            user   = config.get("user",   "root")
            passwd = config.get("passwd", "54321")
            db_uri = "{0}://{1}:{2}@{3}/{4}".format(dbtype, user, passwd, host, dbname)

    return db_uri


def cleanDb(engine):
    pass


def archiveDb(engine):
    if engine.name == "sqlite":
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
