import os.path as osp
from yeetcode.loader import load_problem, load_module


def test_load_problem():
    dir = osp.dirname(osp.abspath(__file__))
    example_yaml = osp.join(dir, "example.yaml")
    problem = load_problem(example_yaml)
    assert problem.class_name == "Greeting"
    assert problem.methods == {"hello": {"name": "str", "return": "str"}}
    assert problem.test_cases == [
        {"name": "Jack", "return": "Hello, Jack!"},
        {"name": "World", "return": "Hello, World!"},
    ]


def test_load_module():
    dir = osp.dirname(osp.abspath(__file__))
    example_py = osp.join(dir, "example.py")
    module = load_module(example_py)
    greeting = module.Greeting()
    assert greeting.hello("World") == "Hello, World!"
