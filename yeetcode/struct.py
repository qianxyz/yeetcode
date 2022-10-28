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

    def _has_cycle(self) -> bool:
        slow = fast = self
        while slow and fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def __eq__(self, other) -> bool:
        """
        When checking solutions, two linked lists are never compared directly;
        They are serialized to plain lists and compared. To prevent accidental
        usage in production, this raises error.
        """
        raise NotImplementedError

    @staticmethod
    def _serialize(node: Optional["ListNode"]) -> list:
        if node is None:
            return []
        if not isinstance(node, ListNode):
            raise SerdeError("object is not linked list")
        if node._has_cycle():
            raise SerdeError("linked list has cycle")
        ret = []
        while node is not None:
            ret.append(node.val)
            node = node.next
        return ret

    @staticmethod
    def _deserialize(lst: list) -> Optional["ListNode"]:
        if not isinstance(lst, list):
            raise SerdeError("cannot deserialize non-list to linked list")
        head = None
        while lst:
            head = ListNode(val=lst.pop(), next=head)
        return head
