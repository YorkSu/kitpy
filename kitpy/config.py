# -*- coding: utf-8 -*-
import abc
import json
import typing

from ruamel.yaml import YAML

from kitpy import paths


class BaseHandler(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def load(filename: str, root='./') -> dict: ...

    @staticmethod
    @abc.abstractmethod
    def dump(obj: dict, filename: str, root='./') -> bool: ...


class YamlHandler(BaseHandler):
    @staticmethod
    def load(filename: str, root='./') -> dict:
        cfg = dict()
        filename = paths.fix(root, filename)
        if paths.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    cfg = YAML(typ='safe').load(f)
                if cfg is None:
                    cfg = dict()
            except Exception as e:
                print(e)
        return cfg

    @staticmethod
    def dump(obj: dict, filename: str, root='./') -> bool:
        assert isinstance(obj, dict)
        filename = paths.fix(root, filename)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                YAML().dump(obj, f)
        except Exception as e:
            print(e)
            return False
        return True


class JsonHandler(BaseHandler):
    @staticmethod
    def load(filename: str, root='./') -> dict:
        cfg = dict()
        filename = paths.fix(root, filename)
        if paths.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
            except Exception as e:
                print(e)
        return cfg

    @staticmethod
    def dump(obj: dict, filename: str, root='./', indent=2, ensure_ascii=False) -> bool:
        assert isinstance(obj, dict)
        filename = paths.fix(root, filename)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(
                    obj,
                    f,
                    indent=indent,
                    ensure_ascii=ensure_ascii
                )
        except Exception as e:
            print(e)
            return False
        return True


class ConfigHandler(BaseHandler):
    @staticmethod
    def load(filename: str, root='./') -> dict:
        cfg = dict()
        handler: typing.Optional['BaseHandler'] = None
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            handler = YamlHandler
        elif filename.endswith('.json'):
            handler = JsonHandler
        if handler:
            cfg = handler.load(filename, root)
        return cfg

    @staticmethod
    def dump(obj: dict, filename: str, root='./', **kwargs) -> bool:
        handler: typing.Optional['BaseHandler'] = None
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            handler = YamlHandler
        elif filename.endswith('.json'):
            handler = JsonHandler
        return handler.dump(obj, filename, root, **kwargs) if handler else False
