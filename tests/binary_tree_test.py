import pytest
from yeetcode.struct import TreeNode, SerdeError


def is_equal_tree(root1, root2) -> bool:
    if root1 is None or root2 is None:
        return root1 is root2
    return (
        root1.val == root2.val
        and is_equal_tree(root1.left, root2.left)
        and is_equal_tree(root1.right, root2.right)
    )


def one_two_three():
    return TreeNode(1, TreeNode(2), TreeNode(3))


def une_duex_trois():
    return TreeNode(1, None, TreeNode(2, TreeNode(3)))


def complex_tree():
    return TreeNode(
        val=5,
        left=TreeNode(4, TreeNode(3, TreeNode(-1))),
        right=TreeNode(7, TreeNode(2, TreeNode(9))),
    )


def test_invalid_subtree():
    with pytest.raises(ValueError):
        TreeNode(left=0)

    with pytest.raises(ValueError):
        t = TreeNode()
        t.right = 0


def test_serialize():
    s = TreeNode._serialize
    assert s(None) == []
    assert s(TreeNode()) == [0]
    assert s(one_two_three()) == [1, 2, 3]
    assert s(une_duex_trois()) == [1, None, 2, 3]
    assert s(complex_tree()) == [5, 4, 7, 3, None, 2, None, -1, None, 9]
    with pytest.raises(SerdeError):
        s("not supported")


def test_deserialize():
    d = TreeNode._deserialize
    assert d([]) is None
    assert is_equal_tree(d([0]), TreeNode())
    assert is_equal_tree(d([1, 2, 3]), one_two_three())
    assert is_equal_tree(d([1, None, 2, 3]), une_duex_trois())
    assert is_equal_tree(
        d([5, 4, 7, 3, None, 2, None, -1, None, 9]), complex_tree()
    )
    with pytest.raises(SerdeError):
        d("not supported")
