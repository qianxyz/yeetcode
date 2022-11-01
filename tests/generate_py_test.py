from yeetcode.problem import Problem


def build_problem(methods: dict) -> Problem:
    return Problem("Foo", methods, [])


def test_plain():
    methods = {"foo": {"a": "int", "b": "int", "return": "int"}}
    problem = build_problem(methods)
    assert (
        problem.generate_py()
        == """\
class Foo:
    def foo(self, a: int, b: int) -> int:
        pass
"""
    )


def test_multi_method():
    methods = {"foo": {"s": "str", "return": None}, "bar": {}}
    problem = build_problem(methods)
    assert (
        problem.generate_py()
        == """\
class Foo:
    def foo(self, s: str) -> None:
        pass

    def bar(self) -> None:
        pass
"""
    )


def test_import_listnode():
    methods = {"foo": {"s": "Optional[ListNode]", "return": None}}
    problem = build_problem(methods)
    assert (
        problem.generate_py()
        == """\
from typing import Optional
from yeetcode import ListNode


# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Foo:
    def foo(self, s: Optional[ListNode]) -> None:
        pass
"""
    )


def test_import_treenode():
    methods = {"foo": {"s": "List[Optional[TreeNode]]", "return": None}}
    problem = build_problem(methods)
    assert (
        problem.generate_py()
        == """\
from typing import List, Optional
from yeetcode import TreeNode


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Foo:
    def foo(self, s: List[Optional[TreeNode]]) -> None:
        pass
"""
    )
