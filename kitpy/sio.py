# -*- coding: utf-8 -*-
"""String File IO"""
import os
from typing import AnyStr, Iterable, Sequence, Union

from kitpy.path import delete


def write(path: AnyStr,
          content: Union[str, Iterable[str]],
          encoding='utf-8') -> None:
    with open(path, 'w', encoding=encoding) as f:
        if isinstance(content, Iterable):
            f.writelines(content)
        else:
            f.write(content)


def read(path: AnyStr, encoding='utf-8') -> Sequence[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, 'r', encoding=encoding) as f:
        return f.readlines()


def touch(path: AnyStr, mode=0o666, dir_fd=None, **kwargs) -> None:
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(path, flags=flags,
                           mode=mode, dir_fd=dir_fd)) as f:
        path = f.fileno() if os.utime in os.supports_fd else path
        dir_fd = None if os.supports_fd else dir_fd
        os.utime(path, dir_fd=dir_fd, **kwargs)
