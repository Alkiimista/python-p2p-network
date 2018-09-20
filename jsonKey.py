# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = key_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class KeyClass:
    origin_id: str
    public_key: str

    def __init__(self, origin_id: str, public_key: str) -> None:
        self.origin_id = origin_id
        self.public_key = public_key

    @staticmethod
    def from_dict(obj: Any) -> 'KeyClass':
        assert isinstance(obj, dict)
        origin_id = from_str(obj.get("originID"))
        public_key = from_str(obj.get("publicKey"))
        return KeyClass(origin_id, public_key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["originID"] = from_str(self.origin_id)
        result["publicKey"] = from_str(self.public_key)
        return result


class Key:
    event: str
    key: KeyClass

    def __init__(self, event: str, key: KeyClass) -> None:
        self.event = event
        self.key = key

    @staticmethod
    def from_dict(obj: Any) -> 'Key':
        assert isinstance(obj, dict)
        event = from_str(obj.get("event"))
        key = KeyClass.from_dict(obj.get("key"))
        return Key(event, key)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = from_str(self.event)
        result["key"] = to_class(KeyClass, self.key)
        return result


def key_from_dict(s: Any) -> Key:
    return Key.from_dict(s)


def key_to_dict(x: Key) -> Any:
    return to_class(Key, x)
