import pytest
from yeetcode.struct import ListNode, SerdeError


def une_duex_trois():
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


def test_invalid_next():
    # when initializing
    with pytest.raises(ValueError):
        _ = ListNode(next=0)

    # modify after initialization
    a = ListNode()
    with pytest.raises(ValueError):
        a.next = 0


def test_serialize():
    assert ListNode()._serialize() == [0]
    assert une_duex_trois()._serialize() == [1, 2, 3]
    assert cycle_included()._serialize() == {"vals": [0, 0, 0], "pos": 1}
    assert ouroboros()._serialize() == {"vals": [0], "pos": 0}


def test_deserialize():
    d = ListNode._deserialize

    a = d([])
    assert a is None

    a = d([1, 2, 3])
    assert (a.val, a.next.val, a.next.next.val) == (1, 2, 3)
    assert a.next.next.next is None

    a = d({"vals": [0, 0, 0], "pos": 1})
    assert (a.val, a.next.val, a.next.next.val) == (0, 0, 0)
    assert a.next.next.next is a.next

    a = d({"vals": [0], "pos": 0})
    assert a.val == 0
    assert a.next == a

    a = d({"vals": [], "pos": 0})
    assert a is None

    with pytest.raises(SerdeError):
        d("string is unsupported")
