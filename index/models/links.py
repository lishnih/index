#!/usr/bin/env python
# coding=utf-8
# Stan 2012-10-13

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import logging


foreign_keys = {}
foreign_keys_c = {}


def initlinks(Base):
    global foreign_keys, foreign_keys_c

    for modelname, model in Base._decl_class_registry.items():
        for i in dir(model):
            if i[0:1] == '_' and i[0:2] != '__':
                attr = getattr(model, i)
                try:
                    pairs = attr.property.synchronize_pairs
                    if type(pairs) == list:
                        for primary_c, foreign_c in pairs:
                            primary_tablename = primary_c.table.name
                            foreign_tablename = foreign_c.table.name
                            if foreign_tablename not in foreign_keys:
                                foreign_keys[foreign_tablename] = {}
                                foreign_keys_c[model] = {}
                            foreign_keys[foreign_tablename][primary_tablename] = i
                            foreign_keys_c[model][primary_tablename] = i
                except:
                    pass


def link_objects(*args):
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
    from __init__ import Base
    from db import initDb

    db_uri = "sqlite://"
    initDb(db_uri, base=Base)
    initlinks(Base)

    logging.info(foreign_keys)
    logging.info(foreign_keys_c)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
