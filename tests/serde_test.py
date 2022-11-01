import pytest
from typing import List, Optional
from yeetcode.struct import ListNode, TreeNode, SerdeError
from yeetcode.struct import serialize, deserialize, deserialize_kwargs


def test_serialize():
    s = serialize

    # primitive data types
    assert s(1, int) == 1
    assert s(1.0, float) == 1.0
    assert s("hello", str) == "hello"
    assert s(True, bool) is True
    assert s(None, type(None)) is None
    with pytest.raises(SerdeError):
        s(1, str)

    # linked list
    assert s(None, Optional[ListNode]) == []
    assert s(ListNode(next=ListNode()), Optional[ListNode]) == [0, 0]

    # binary tree
    assert s(None, Optional[TreeNode]) == []
    assert s(TreeNode(right=TreeNode()), TreeNode) == [0, None, 0]

    # List
    assert s([1, 2], List[int]) == [1, 2]
    assert s([[1, 2], [3, 4]], List[List[int]]) == [[1, 2], [3, 4]]
    assert s(["a", "b"], List[str]) == ["a", "b"]
    assert s([["a", "b"], ["c"]], List[List[str]]) == [["a", "b"], ["c"]]
    with pytest.raises(SerdeError):
        s(0, List[int])
    with pytest.raises(SerdeError):
        s([1], List[List[int]])

    # Optional
    assert s(None, Optional[int]) is None
    assert s(1, Optional[int]) == 1


def test_deserialize():
    d = deserialize

    # primitive data types
    assert d(1, int) == 1
    assert d(1.0, float) == 1.0
    assert d("hello", str) == "hello"
    assert d(True, bool) is True
    assert d(None, type(None)) is None
    with pytest.raises(SerdeError):
        d(1, str)

    # linked list
    assert d([], Optional[ListNode]) is None
    a = d([1, 2], Optional[ListNode])
    assert (a.val, a.next.val, a.next.next) == (1, 2, None)

    # binary tree
    assert d([], Optional[TreeNode]) is None
    a = d([1, 2, 3], TreeNode)
    assert (a.val, a.left.val, a.right.val) == (1, 2, 3)

    # List
    assert d([1, 2], List[int]) == [1, 2]
    assert d([[1, 2], [3, 4]], List[List[int]]) == [[1, 2], [3, 4]]
    assert d(["a", "b"], List[str]) == ["a", "b"]
    assert d([["a", "b"], ["c"]], List[List[str]]) == [["a", "b"], ["c"]]
    with pytest.raises(SerdeError):
        d(0, List[int])
    with pytest.raises(SerdeError):
        d([1], List[List[int]])

    # Optional
    assert d(None, Optional[int]) is None
    assert d(1, Optional[int]) == 1


def test_deserialize_kwargs():
    kwargs = {"a": 1, "s": "hello", "l": [1, 2], "n": None}
    types = {"a": int, "s": str, "l": List[int], "n": type(None)}
    assert deserialize_kwargs(kwargs, types) == kwargs
