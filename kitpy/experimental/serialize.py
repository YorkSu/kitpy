# -*- coding: utf-8 -*-
"""Serialization tools

Serialization & Deserialization

"""

import json
from typing import Any, Callable, Sequence, Union


class Serializable(object):
    def __encode__(self) -> Union[dict, list]:
        return NotImplemented

    @classmethod
    def __decode__(cls, obj: Union[dict, list]) -> 'Serializable':
        return NotImplemented


class AdvancedEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Serializable):
            return {
                '__class__': str(type(obj).__name__),
                '__data__': obj.__encode__()
            }
        return super().default(obj)


class PureEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Serializable):
            return obj.__encode__()
        return super().default(obj)


def AdvancedDecoder(clss: Sequence[Serializable]) -> Callable:
    decode_map = dict()

    if isinstance(clss, (tuple, list)):
        for cls in clss:
            if not issubclass(cls, Serializable):
                raise TypeError('Expect cls `Serializable`, got',
                                type(cls))
            decode_map[cls.__name__] = cls
    else:
        raise TypeError('Expect clss `[Serializable]`, got', clss)

    def object_hook(o: dict) -> Any:
        if '__class__' in o and o['__class__'] in decode_map:
            return decode_map[o['__class__']].__decode__(o['__data__'])
        return o

    return object_hook


def encode(o: Any, cls: json.JSONEncoder = None) -> str:
    if cls is not None:
        if not issubclass(cls, json.JSONEncoder):
            raise TypeError('Expect cls `json.JSONEncoder`, got', cls)
    else:
        cls = AdvancedEncoder
    return cls().encode(o)


def decode(s: str, clss: Union[Sequence[Serializable], Serializable] = None) -> Any:
    if clss is None:
        return json.loads(s)
    if isinstance(clss, (tuple, list)):
        return json.loads(s, object_hook=AdvancedDecoder(clss))
    if issubclass(clss, Serializable):
        return json.loads(s, object_hook=AdvancedDecoder([clss]))
    raise TypeError('Expect clss `[Serializable]` or None, got', type(clss))
