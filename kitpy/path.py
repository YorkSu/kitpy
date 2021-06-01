# -*- coding: utf-8 -*-
import os
import sys
import shutil
from typing import AnyStr, Sequence, Union, NoReturn


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
makedirs = os.makedirs
mkdir = os.mkdir
normcase = os.path.normcase
normpath = os.path.normpath
remove = os.remove
realpath = os.path.realpath
relpath = os.path.relpath
split = os.path.split


def cd() -> AnyStr:
    return os.path.dirname(sys.argv[0])


def crf() -> AnyStr:
    return sys.argv[0]


def delete(path: AnyStr, must_exist=False) -> NoReturn:
    """
    Removes a file or recursively removes a directory.
    If a path does not exist, raise Exception or do nothing.

    Args:
        path (AnyStr): the file path
        must_exist (bool): if True and path does not exist,
            raise Exception

    Raises:
        FileNotFoundError: path not exist and ``must_exist`` is True
        Exception: Unknown Error
    """
    if os.path.exists(path):
        if os.path.islink(path):
            os.unlink(path)
        elif os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise Exception('Unknown Error', path)
    elif must_exist:
        raise FileNotFoundError(path)


def ensure(path: Union[AnyStr, Sequence[AnyStr]], mode: int = 0o777) -> AnyStr:
    """
    Ensure that directory will exist.

    Args:
        path (Union[AnyStr, Sequence[AnyStr]]): dir to ensure
        mode (int): octal mode of directory

    Returns:
        AnyStr: the ensure directory
    """
    if isinstance(path, (tuple, list)):
        path = join(path)

    if not exists(path):
        os.makedirs(normpath(path), mode=mode, exist_ok=True)

    return path


def ensure_empty(path: Union[AnyStr, Sequence[AnyStr]], mode: int = 0o777) -> AnyStr:
    if isinstance(path, (tuple, list)):
        path = join(path)

    if exists(path):
        if os.listdir(path):
            delete(path)
    else:
        os.makedirs(normpath(path), mode=mode, exist_ok=True)

    return path


def fd(_file: AnyStr) -> AnyStr:
    return os.path.dirname(os.path.abspath(_file))


def fix(path: AnyStr, filename: AnyStr) -> AnyStr:
    if isabs(filename):
        return filename
    return join(path, filename)


def userhome(username=None) -> AnyStr:
    if username is None:
        if 'HOME' in os.environ:
            result = os.environ['HOME']
        else:
            if sys.platform.startswith('win32'):
                if 'USERPROFILE' in os.environ:
                    result = os.environ['USERPROFILE']
                elif 'HOMEPATH' in os.environ:
                    drive = os.environ.get('HOMEDRIVE', '')
                    result = join(drive, os.environ['HOMEPATH'])
                else:
                    raise OSError("Cannot determine the user's home directory")
            else:
                # unix os
                result = ''
    else:
        if sys.platform.startswith('win32'):
            c_users = dirname(userhome())
            userhome_dpath = join(c_users, username)
            if not exists(userhome_dpath):
                raise KeyError(f'Unknown user: {username}')
        else:
            # unix os
            result = ''
    return result
