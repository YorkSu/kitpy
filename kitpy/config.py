# -*- coding: utf-8 -*-
import abc
import os
import json

from ruamel.yaml import YAML


class Handler(abc.ABC):
    @abc.abstractmethod
    def load(self) -> dict: ...

    @abc.abstractmethod
    def dump(self, obj: dict) -> None: ...


class BaseHander(Handler):
    def __init__(self,
                 filename: str,
                 encoding='utf-8',
                 readonly=False):
        self.filename = filename
        self.encoding = encoding
        self.readonly = readonly

    def load(self) -> dict:
        if not self.exists:
            raise Exception(
                'file not exist',
                self.filename
            )
        return dict()

    def dump(self, obj: dict) -> None:
        if not isinstance(obj, dict):
            raise TypeError(
                "dump.obj except serializable object, got",
                type(obj)
            )
        if self.readonly:
            raise Exception('readonly')

    @property
    def exists(self) -> bool:
        return os.path.exists(self.filename)


class JsonHandler(BaseHander):
    def load(self) -> dict:
        super().load()
        with open(self.filename, 'r', encoding=self.encoding) as f:
            result = json.load(f)
        return result

    def dump(self, obj: dict, indent=2, ensure_ascii=False) -> None:
        super().dump(obj)
        with open(self.filename, 'w', encoding=self.encoding) as f:
            json.dump(
                obj,
                f,
                indent=indent,
                ensure_ascii=ensure_ascii
            )


class YamlHandler(BaseHander):
    def load(self) -> dict:
        super().load()
        with open(self.filename, 'r', encoding='utf-8') as f:
            result = YAML(typ='safe').load(f)
        if result is None:
            result = dict()
        return result

    def dump(self, obj: dict) -> None:
        super().dump(obj)
        with open(self.filename, 'w', encoding='utf-8') as f:
            YAML().dump(obj, f)


class ConfigHandler(BaseHander):
    def __init__(self,
                 filename: str,
                 encoding='utf-8',
                 readonly=False):
        super().__init__(filename, encoding, readonly)
        self._handler = self.create_handler()(filename, encoding, readonly)

    def create_handler(self) -> 'Handler':
        if self.filename.endswith('.yml'):
            return YamlHandler
        if self.filename.endswith('.yaml'):
            return YamlHandler
        if self.filename.endswith('.json'):
            return JsonHandler
        return BaseHander

    def load(self) -> dict:
        return self._handler.load()

    def dump(self, obj: dict, *args, **kwargs) -> None:
        self._handler.dump(obj, *args, **kwargs)


def load(filename: str) -> dict:
    return ConfigHandler(filename).load()


def dump(filename: str, obj: dict, *args, **kwargs) -> None:
    return ConfigHandler(filename).dump(obj, *args, **kwargs)
