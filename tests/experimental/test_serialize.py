import json
from typing import Any, Callable, Sequence, Union

from kitpy.experimental import serialize as srl


class People(srl.Serializable):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __encode__(self) -> Union[dict, list]:
        return {
            'name': self.name,
            'age': self.age
        }

    @classmethod
    def __decode__(cls, obj: Union[dict, list]) -> 'srl.Serializable':
        return cls(**obj)

    def __repr__(self) -> str:
        return f'People(name={self.name}, age={self.age})'


class TestSerialize:
    def test_raw_encoder(self):
        people = People('Bob', 18)
        encoded = srl.PureEncoder().encode(people)
        assert encoded == '{"name": "Bob", "age": 18}'

    def test_raw_encoder_nested(self):
        data = {
            'peoples': [
                People('Bob', 18),
                People('Mike', 19)
            ]
        }
        encoded = srl.PureEncoder().encode(data)
        assert encoded == '{"peoples": [{"name": "Bob", "age": 18}, ' \
                          '{"name": "Mike", "age": 19}]}'

    def test_advanced_encoder(self):
        people = People('Bob', 18)
        encoded = srl.AdvancedEncoder().encode(people)
        assert encoded == '{"__class__": "People", ' \
                          '"__data__": {"name": "Bob", "age": 18}}'

    def test_raw_decoder(self):
        data = {
            'name': 'Bob',
            'age': 18
        }
        encoded = srl.PureEncoder().encode(People(**data))
        assert json.loads(encoded) == data

    def test_advanced_decoder(self):
        data = {
            'name': 'Bob',
            'age': 18
        }
        encoded = srl.AdvancedEncoder().encode(People(**data))
        decoded = json.loads(encoded, object_hook=srl.AdvancedDecoder([People]))
        assert isinstance(decoded, People)

    def test_advanced_decoder_nested(self):
        data = {
            'peoples': [
                People('Bob', 18),
                People('Mike', 19)
            ]
        }
        encoded = srl.AdvancedEncoder().encode(data)
        decoded = json.loads(encoded, object_hook=srl.AdvancedDecoder([People]))
        assert isinstance(decoded, dict)
        assert 'peoples' in decoded
        for people in decoded['peoples']:
            assert isinstance(people, People)

    def test_encode_raw(self):
        people = People('Bob', 18)
        encoded = srl.encode(people, srl.PureEncoder)
        assert encoded == '{"name": "Bob", "age": 18}'

    def test_encode_default(self):
        people = People('Bob', 18)
        encoded = srl.encode(people)
        assert encoded == '{"__class__": "People", ' \
                          '"__data__": {"name": "Bob", "age": 18}}'

    def test_decode(self):
        data = {
            'peoples': [
                People('Bob', 18),
                People('Mike', 19)
            ]
        }
        encoded = srl.encode(data)
        decoded = srl.decode(encoded, People)
        assert isinstance(decoded, dict)
        assert 'peoples' in decoded
        for people in decoded['peoples']:
            assert isinstance(people, People)
