import typing
from typing import Optional


class SerdeError(Exception):
    pass


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, item):
        if not (item is None or isinstance(item, ListNode)):
            raise ValueError("next must be ListNode or None")
        self._next = item

    def _serialize(self) -> list | dict:
        """
        When the linked list has no cycles, return a list of vals.
        Otherwise, return a dict { "vals": list, "pos": int }.
        See Leetcode problem #141.
        """
        # NOTE: dict preserves insertion order since Python 3.7
        visited = {}
        pos = 0
        while self is not None:
            if self in visited:
                return {
                    "vals": [node.val for node in visited],
                    "pos": visited[self],
                }
            visited[self] = pos
            self = self.next
            pos += 1
        return [node.val for node in visited]

    @staticmethod
    def _deserialize(data: list | dict) -> Optional["ListNode"]:
        if isinstance(data, list):
            p = None
            while data:
                p = ListNode(val=data.pop(), next=p)
            return p

        elif isinstance(data, dict):
            vals = data["vals"]
            pos = data["pos"]
            p = end = loop_entrance = None
            while vals:
                p = ListNode(val=vals.pop(), next=p)
                if end is None:
                    end = p
                if len(vals) == pos:
                    loop_entrance = p
            if end is not None:
                end.next = loop_entrance
            return p

        else:
            raise SerdeError("unsupported type to deserialize to linked list")


# All types in Leetcode top 100 questions:
#
# int, float, str, bool, type(None)
# List[int], List[List[int]], List[str], List[List[str]], List[float]
# ListNode, Optional[ListNode], List[Optional[ListNode]]
# TreeNode, Optional[TreeNode]
#
# And generally I want to support more Optional thing.


def deserialize(origin, typ: typing.Type):
    pass


def serialize(data, typ: typing.Type):
    pass
