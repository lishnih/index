#!/usr/bin/env python
# coding=utf-8
# Stan 2013-02-23

from __future__ import (division, absolute_import,
                        print_function, unicode_literals)

import os
import argparse


class readable_file(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isfile(values):
            raise argparse.ArgumentTypeError("[FILE] '{0}' is not valid path".format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError("[FILE] '{0}' is not readable file".format(values))


class readable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == '~':
            setattr(namespace, self.dest, values)
            return

        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError("[DIR] '{0}' is not valid path".format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError("[DIR] '{0}' is not readable dir".format(values))


class readable_file_or_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values[0] == '~':
            setattr(namespace, self.dest, values)
            return

        if not os.path.exists(values):
            raise argparse.ArgumentTypeError("[DIR/FILE] '{0}' is not valid path".format(values))
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError("[DIR/FILE] '{0}' is not readable dir".format(values))


class readable_file_or_dir_list(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            if value[0] == '~':
                setattr(namespace, self.dest, values)
                continue

            if not os.path.exists(value):
                raise argparse.ArgumentTypeError("[DIR/FILE] '{0}' is not valid path".format(value))
            if os.access(value, os.R_OK):
                self.append_file(namespace, value)
            else:
                raise argparse.ArgumentTypeError("[DIR/FILE] '{0}' is not readable dir".format(value))

    def append_file(self, namespace, value):
        files_list = getattr(namespace, self.dest)
        if not files_list:
            files_list = []
        files_list.append(value)
        setattr(namespace, self.dest, files_list)
