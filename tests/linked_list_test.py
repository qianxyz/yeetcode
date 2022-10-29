from typing import Optional
import pytest
from yeetcode.struct import ListNode, SerdeError


def normal_linked_list():
    return ListNode(1, ListNode(2, ListNode(3)))


def cycle_included():
    a = ListNode()
    b = ListNode()
    c = ListNode()
    a.next = b
    b.next = c
    c.next = b
    return a


def ouroboros():
    a = ListNode()
    a.next = a
    return a


def is_equal(p: Optional[ListNode], q: Optional[ListNode]) -> bool:
    while p and q and p.val == q.val:
        p = p.next
        q = q.next
    return p is q


def test_invalid_next():
    # when initializing
    with pytest.raises(ValueError):
        _ = ListNode(next=0)

    # modify after initialization
    a = ListNode()
    with pytest.raises(ValueError):
        a.next = 0


def test_cycle_detection():
    assert ouroboros()._has_cycle()
    assert cycle_included()._has_cycle()
    assert not normal_linked_list()._has_cycle()


def test_serialize():
    s = ListNode._serialize
    assert s(None) == []
    assert s(normal_linked_list()) == [1, 2, 3]
    with pytest.raises(SerdeError):
        s(1)
    with pytest.raises(SerdeError):
        s(ouroboros())


def test_deserialize():
    d = ListNode._deserialize
    assert d([]) is None
    assert is_equal(d([1, 2, 3]), normal_linked_list())
    with pytest.raises(SerdeError):
        d(1)
