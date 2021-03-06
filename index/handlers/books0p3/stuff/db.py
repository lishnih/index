#!/usr/bin/env python
# coding=utf-8
# Stan 2012-03-10

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import shutil
import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, attributes


foreign_keys = {}
foreign_keys_c = {}


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


def getDbUri(config=None):
    if not config:
        config = {}

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


def utilDb(session, archive_db=None, clear_db=None, prefix=None):
    engine = session.bind

    if archive_db:
        archiveDb(engine)

    if clear_db:
        if prefix:
            clearDb(engine, prefix)
        else:
            logging.warning("prefix is missing, pass clearing...")


def clearDb(engine, prefix):
    metadata = MetaData(engine, reflect=True)
    for tablename in metadata.tables.keys():
        if tablename.startswith("{0}_".format(prefix)):
            mtable = metadata.tables.get(tablename)
            engine.execute(mtable.delete())


def archiveDb(engine):
    if engine.name == "sqlite":
        filename = engine.url.database
        logging.info('Archiving {0}'.format(filename))
        archiveFile(filename)
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


def initlinks(Base):
    global foreign_keys, foreign_keys_c

    for modelname, model in Base._decl_class_registry.items():
        for i in dir(model):
            if i[0:1] == '_' and i[0:2] != '__':
                attr = getattr(model, i)
                if isinstance(attr, attributes.InstrumentedAttribute):
                    if hasattr(attr.property, 'synchronize_pairs'):
                        pairs = attr.property.synchronize_pairs
                        if isinstance(pairs, list):
                            for primary_c, foreign_c in pairs:
                                primary_tablename = primary_c.table.name
                                foreign_tablename = foreign_c.table.name
                                if foreign_tablename not in foreign_keys:
                                    foreign_keys[foreign_tablename] = {}
                                    foreign_keys_c[model] = {}
                                foreign_keys[foreign_tablename][primary_tablename] = i
                                foreign_keys_c[model][primary_tablename] = i

#   logging.debug(foreign_keys)
#   logging.debug(foreign_keys_c)
    return foreign_keys, foreign_keys_c


def link_objects(*args):
    args = [i for i in args if i and hasattr(i, '_sa_class_manager')]

    if len(args) < 2:
        return

    classes = [i._sa_class_manager.class_ for i in args]
    tablenames = [i.__table__.name for i in args]

    im = 0
    for model in classes:
        if model in foreign_keys_c:
            for primary_tablename in foreign_keys_c[model]:
                if primary_tablename in tablenames:
                    obj = args[im]
                    ip = tablenames.index(primary_tablename)
                    pobj = args[ip]
                    foreign_key = foreign_keys_c[model][primary_tablename]
                    setattr(obj, foreign_key, pobj)
        im += 1


def main():
    from models import Base

    dbconfig = {'db_uri': "sqlite://"}
    initDb(dbconfig, base=Base)
    foreign_keys, foreign_keys_c = initlinks(Base)

    logging.info("foreign_keys:")
    for key, value in foreign_keys.items():
        logging.info(key, value)

    logging.info("foreign_keys_c:")
    for key, value in foreign_keys_c.items():
        logging.info(key, value)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    main()
