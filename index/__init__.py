#!/usr/bin/env python
# coding=utf-8


__pkgname__ = __name__
__description__ = "Index System"
__version__ = "0.4"


if __pkgname__ == '__init__':
    import os
    __pkgname__ = os.path.basename(os.path.dirname(__file__))
