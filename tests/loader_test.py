import os
from yeetcode.loader import load_problem, load_module

# NOTE: These tests create temporary files and remove them later.
# For `load_problem` a workaround is to pass in raw yaml directly;
# However, for `load_module`, there seems no way to load python source
# without calling `exec` (a lot more dangerous than creating tmp files).


def test_load_problem():
    yaml_str = """
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

    dir = os.path.dirname(os.path.abspath(__file__))
    tmp_yaml = os.path.join(dir, "tmp.yaml")
    with open(tmp_yaml, "w") as f:
        f.write(yaml_str)
    problem = load_problem(tmp_yaml)
    os.remove(tmp_yaml)

    assert problem.class_name == "Greeting"
    assert problem.methods == {"hello": {"name": "str", "return": "str"}}
    assert problem.test_cases == [
        {"name": "Jack", "return": "Hello, Jack!"},
        {"name": "World", "return": "Hello, World!"},
    ]


def test_load_module():
    py_str = """
class Greeting:
    def hello(self, name: str) -> str:
        return f"Hello, {name}!"
"""

    dir = os.path.dirname(os.path.abspath(__file__))
    tmp_py = os.path.join(dir, "tmp.py")
    with open(tmp_py, "w") as f:
        f.write(py_str)
    module = load_module(tmp_py)
    greeting = module.Greeting()
    assert greeting.hello("World") == "Hello, World!"
    os.remove(tmp_py)
