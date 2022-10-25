import sys
import pytest
from yeetcode.problem import MultiMethodProblem


class Button:
    def __init__(self) -> None:
        self.count = 0

    def push(self, times: int) -> None:
        self.count += times

    def show(self) -> int:
        return self.count


class BrokenButton(Button):
    def push(self, times: int) -> None:
        _ = times  # discard input


def normal_test_cases():
    return [
        [
            {"__init__": {}},
            {"push": {"times": 1}},
            {"show": {"return": 1}},
        ]
    ]


def no_init_test_cases():
    return [
        [
            {"push": {"times": 1}},
            {"show": {"return": 1}},
        ]
    ]


def multi_init_test_cases():
    return [
        [
            {"__init__": {}},
            {"push": {"times": 1}},
            {"__init__": {}},
            {"show": {"return": 1}},
        ]
    ]


def multi_method_problem(
    test_cases: list, name: str = "Button"
) -> MultiMethodProblem:
    methods = {
        "__init__": {"return": None},
        "push": {"times": "int", "return": None},
        "show": {"return": "int"},
    }
    return MultiMethodProblem(name, methods, test_cases)


def test_good_run():
    problem = multi_method_problem(normal_test_cases())
    problem.run_tests(sys.modules[__name__])


def test_wrong_answer():
    problem = multi_method_problem(normal_test_cases(), "BrokenButton")
    with pytest.raises(AssertionError):
        problem.run_tests(sys.modules[__name__])


def test_no_init():
    problem = multi_method_problem(no_init_test_cases())
    with pytest.raises(AssertionError):
        problem.run_tests(sys.modules[__name__])


def test_multiple_init():
    problem = multi_method_problem(multi_init_test_cases())
    with pytest.raises(AssertionError):
        problem.run_tests(sys.modules[__name__])
