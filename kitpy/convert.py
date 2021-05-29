# -*- coding: utf-8 -*-
from typing import Optional


class AdvancedDict(dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __repr__(self):
        return f"ADict({', '.join([f'{k}={v}' for k, v in self.items()])})"

    @classmethod
    def from_dict(cls, _dict: dict) -> Optional['AdvancedDict']:
        if isinstance(_dict, dict):
            obj = cls()
            for k, v in _dict.items():
                obj[k] = cls.from_dict(v)
            return obj
        if isinstance(_dict, list):
            return list(map(cls.from_dict, _dict))
        return _dict


dict2ad = AdvancedDict.from_dict
