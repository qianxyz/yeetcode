from yeetcode.problem import Problem


def test_plain():
    class_name = "Foo"
    methods = {
        "foo": {
            "a": "int",
            "b": "int",
            "__return": "int",
        },
    }
    test_cases = []
    problem = Problem(class_name, methods, test_cases)
    assert problem.generate_py() == """\
class Foo:

    def foo(self, a: int, b: int) -> int:
        pass
"""


def test_multi_method():
    class_name = "Foo"
    methods = {
        "foo": {
            "s": "str",
            "__return": None,
        },
        "bar": {},
    }
    test_cases = []
    problem = Problem(class_name, methods, test_cases)
    assert problem.generate_py() == """\
class Foo:

    def foo(self, s: str) -> None:
        pass

    def bar(self) -> None:
        pass
"""


def test_import():
    class_name = "Foo"
    methods = {
        "foo": {
            "s": "List[Optional[ListNode]]",
            "__return": None,
        },
    }
    test_cases = []
    problem = Problem(class_name, methods, test_cases)
    assert problem.generate_py() == """\
from typing import List, Optional
from yeetcode import ListNode


class Foo:

    def foo(self, s: List[Optional[ListNode]]) -> None:
        pass
"""
