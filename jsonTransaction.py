# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = transaction_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast
from jsonBlock import Transaction as BlockTransaction


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TransactionClass:
    to: str
    transaction_from: str
    amount: int

    def __init__(self, to: str, transaction_from: str, amount: int) -> None:
        self.to = to
        self.transaction_from = transaction_from
        self.amount = amount

    @staticmethod
    def from_dict(obj: Any) -> 'TransactionClass':
        assert isinstance(obj, dict)
        to = from_str(obj.get("to"))
        transaction_from = from_str(obj.get("from"))
        amount = from_int(obj.get("amount"))
        return TransactionClass(to, transaction_from, amount)

    def to_dict(self) -> dict:
        result: dict = {}
        result["to"] = from_str(self.to)
        result["from"] = from_str(self.transaction_from)
        result["amount"] = from_int(self.amount)
        return result

    def to_block_transaction(self) -> BlockTransaction:
        return BlockTransaction(self.to, self.transaction_from, self.amount)


class Transaction:
    event: str
    transaction: TransactionClass

    def __init__(self, event: str, transaction: TransactionClass) -> None:
        self.event = event
        self.transaction = transaction

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        event = from_str(obj.get("event"))
        transaction = TransactionClass.from_dict(obj.get("transaction"))
        return Transaction(event, transaction)

    def to_dict(self) -> dict:
        result: dict = {}
        result["event"] = from_str(self.event)
        result["transaction"] = to_class(TransactionClass, self.transaction)
        return result


def transaction_from_dict(s: Any) -> Transaction:
    return Transaction.from_dict(s)


def transaction_to_dict(x: Transaction) -> Any:
    return to_class(Transaction, x)
