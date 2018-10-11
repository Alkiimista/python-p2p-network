from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Node:
    ip: str
    port: int
    pubKey: str

    def __init__(self, ip: str, port: int, pubKey: str) -> None:
        self.ip = ip
        self.port = port
        self.pubKey = pubKey

    @staticmethod
    def from_dict(obj: Any) -> 'Node':
        assert isinstance(obj, dict)
        ip = from_str(obj.get("ip"))
        port = from_int(obj.get("port"))
        pubKey = from_str(obj.get("pubKey"))
        return Node(ip, port, pubKey)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ip"] = from_str(self.ip)
        result["port"] = from_int(self.port)
        result["pubKey"] = from_str(self.pubKey)
        return result


class Message:
    event: str
    nodes: List[Node]

    def __init__(self, event: str, nodes: List[Node]) -> None:
        self.event = event
        self.nodes = nodes

    @staticmethod
    def from_dict(obj: Any) -> 'Message':
        assert isinstance(obj, dict)
        event = from_str(obj.get("event"))
        nodes = from_list(Node.from_dict, obj.get("nodes"))
        return Message(event, nodes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = from_str(self.event)
        result["nodes"] = from_list(lambda x: to_class(Node, x), self.nodes)
        return result


def message_from_dict(s: Any) -> Message:
    return Message.from_dict(s)


def message_to_dict(x: Message) -> Any:
    return to_class(Message, x)