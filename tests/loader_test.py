from yeetcode.loader import load_problem, load_module


def test_load_problem():
    yaml_raw = """
Greeting:
  hello:
    name: str
    return: str

tests:
- name: "Jack"
  return: "Hello, Jack!"
- name: "World"
  return: "Hello, World!"
"""

    problem = load_problem(yaml_raw)
    assert problem.class_name == "Greeting"
    assert problem.methods == {"hello": {"name": "str", "return": "str"}}
    assert problem.test_cases == [
        {"name": "Jack", "return": "Hello, Jack!"},
        {"name": "World", "return": "Hello, World!"},
    ]


def test_load_multi_method_problem():
    yaml_raw = """
Person:
  __init__:
    name: str
    return: null
  greet:
    return: str

tests:
- - __init__: { name: "Jack" }
  - greet: { return: "Hello, Jack!" }
"""

    problem = load_problem(yaml_raw)
    assert problem.class_name == "Person"
    assert problem.methods == {
        "__init__": {"name": "str", "return": None},
        "greet": {"return": "str"},
    }
    assert problem.test_cases == [
        [{"__init__": {"name": "Jack"}}, {"greet": {"return": "Hello, Jack!"}}]
    ]


def test_load_module():
    py_str = """
class Greeting:
    def hello(self, name: str) -> str:
        return f"Hello, {name}!"
"""

    module = load_module(py_str)
    greeting = module.Greeting()
    assert greeting.hello("World") == "Hello, World!"
