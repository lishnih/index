#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-22

from __future__ import ( division, absolute_import,
                         print_function, unicode_literals )

import os, pickle, logging

try:
    from .lib.settings import Settings
except:
    from lib.settings import Settings

from presets import *


def save_entry(filename, entry):
    with open(filename, 'wb') as f:
        pickle.dump(entry, f)


def main():
    s = Settings()
    s.init_path("datadir", "~~~")
    datadir = s.get("datadir")

    if datadir:
        logging.info("Export to '{0}'".format(datadir))
    
        for key, value in globals().items():
            if isinstance(value, dict):
                description = value.get("description", "")
                logging.info("{0:20}: {1}".format(key, description))
                filename = os.path.join(datadir, "{0}.pickle".format(key))
                save_entry(filename, value)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()
