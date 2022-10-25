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


def test_import():
    methods = {"foo": {"s": "List[Optional[ListNode]]", "return": None}}
    problem = build_problem(methods)
    assert (
        problem.generate_py()
        == """\
from typing import List, Optional
from yeetcode import ListNode


class Foo:
    def foo(self, s: List[Optional[ListNode]]) -> None:
        pass
"""
    )
