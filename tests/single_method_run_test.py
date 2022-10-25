import sys
import pytest
from yeetcode.problem import SingleMethodProblem


class Addition:
    def sum_of_two(self, a: int, b: int) -> int:
        return a + b


class WrongAddition:
    def sum_of_two(self, a: int, b: int) -> int:
        return a * b


def single_method_problem(name: str) -> SingleMethodProblem:
    class_name = name
    methods = {"sum_of_two": {"a": "int", "b": "int", "return": "int"}}
    test_cases = [
        {"a": 0, "b": 1, "return": 1},
        {"a": 2, "b": 2, "return": 4},
    ]
    return SingleMethodProblem(class_name, methods, test_cases)


def test_good_run():
    problem = single_method_problem("Addition")
    problem.run_tests(sys.modules[__name__])


def test_bad_run():
    problem = single_method_problem("WrongAddition")
    with pytest.raises(AssertionError):
        problem.run_tests(sys.modules[__name__])
