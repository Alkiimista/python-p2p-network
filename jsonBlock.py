# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = block_from_dict(json.loads(json_string))

from typing import Any, List, TypeVar, Callable, Type, cast
import jsonTransaction

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


class Transaction:
    to: str
    transaction_from: str
    amount: int

    def __init__(self, to: str, transaction_from: str, amount: int) -> None:
        self.to = to
        self.transaction_from = transaction_from
        self.amount = amount

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        to = from_str(obj.get("to"))
        transaction_from = from_str(obj.get("from"))
        amount = from_int(obj.get("amount"))
        return Transaction(to, transaction_from, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["to"] = from_str(self.to)
        result["from"] = from_str(self.transaction_from)
        result["amount"] = from_int(self.amount)
        return result

    def to_other_transaction(self) -> 'jsonTransaction.Transaction':
        return jsonTransaction.Transaction("TRANSACTION", jsonTransaction.TransactionClass(self.to, self.transaction_from, self.amount))


class Block:
    event: str
    nonce: int
    previous_block: str
    transactions: List[Transaction]

    def __init__(self, event: str, nonce: int, previous_block: str, transactions: List[Transaction]) -> None:
        self.event = event
        self.nonce = nonce
        self.previous_block = previous_block
        self.transactions = transactions

    @staticmethod
    def from_dict(obj: Any) -> 'Block':
        assert isinstance(obj, dict)
        event = from_str(obj.get("event"))
        nonce = from_int(obj.get("nonce"))
        previous_block = from_str(obj.get("previous_block"))
        transactions = from_list(Transaction.from_dict, obj.get("transactions"))
        return Block(event, nonce, previous_block, transactions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = from_str(self.event)
        result["nonce"] = from_int(self.nonce)
        result["previous_block"] = from_str(self.previous_block)
        result["transactions"] = from_list(lambda x: to_class(Transaction, x), self.transactions)
        return result


def block_from_dict(s: Any) -> Block:
    return Block.from_dict(s)


def block_to_dict(x: Block) -> Any:
    return to_class(Block, x)
