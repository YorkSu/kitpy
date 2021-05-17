# -*- coding: utf-8 -*-
import os
import sys


abs = os.path.abspath
basename = os.path.basename
commonpath = os.path.commonpath
commonprefix = os.path.commonprefix
curdir = os.path.curdir
cwd = os.getcwd
dir = os.path.dirname
dirname = os.path.dirname
exists = os.path.exists
expanduser = os.path.expanduser
expandvars = os.path.expandvars
getatime = os.path.getatime
getctime = os.path.getctime
getmtime = os.path.getmtime
getsize = os.path.getsize
isabs = os.path.isabs
isdir = os.path.isdir
isfile = os.path.isfile
islink = os.path.islink
ismount = os.path.ismount
join = os.path.join
listdir = os.listdir
normcase = os.path.normcase
normpath = os.path.normpath
remove = os.remove
realpath = os.path.realpath
relpath = os.path.relpath
split = os.path.split


def crf():
    return sys.argv[0]


def cd():
    return os.path.dirname(sys.argv[0])


def fd(filename):
    return os.path.dirname(os.path.abspath(filename))


def mkdir(path, mode=511, dir_fd=None):
    if not os.path.exists(path):
        os.mkdir(path, mode=mode, dir_fd=dir_fd)


def fix(path: str, filename: str) -> str:
    if isabs(filename):
        return filename
    return join(path, filename)
