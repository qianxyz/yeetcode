import importlib
import os
import sys
import yaml


_PROBLEM_LIST = "problem.yaml"

_CONFIG_PATH = "problem/{}.yaml"
_CONFIG_TEMPLATE = """\
solution:
  class: Addition
  method:
    name: add_two_numbers
    args:
      - a
      - b

test cases:

  - input:
    - 2
    - 2
    expect: 4
"""

_SOLUTION_MODULE = "solution.{}"
_SOLUTION_FILE_PATH = "solution/{}.py"
_SOLUTION_TEMPLATE = """\
class {}:

    def {}(self, {}):
        pass
"""


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


class ProblemList:

    def __init__(self) -> None:
        with open(_PROBLEM_LIST) as f:
            self.plist: dict = yaml.safe_load(f)

    def get_title(self, pid: int) -> str:
        name = self.plist[pid]
        return f"{pid}_{name}"

    def __str__(self) -> str:
        return '\n'.join(f"{id}: {name}" for id, name in self.plist.items())

    def add_problem(self, name):
        max_id = max(self.plist)
        self.plist[max_id + 1] = name
        with open(_PROBLEM_LIST, 'w') as f:
            yaml.safe_dump(self.plist, f)

        cfg_path = _CONFIG_PATH.format(self.get_title(max_id + 1))
        with open(cfg_path, 'w') as f:
            f.write(_CONFIG_TEMPLATE)
        print(f"config template generated at {cfg_path}")

    def run_all(self):
        for pid in self.plist:
            problem = Problem(pid, self)
            problem.run()


class Problem:

    def __init__(self, pid: int, plist: ProblemList) -> None:
        self.title = plist.get_title(pid)
        with open(_CONFIG_PATH.format(self.title)) as f:
            self.cfg = yaml.safe_load(f)

    def generate(self):
        """Generate a template solution file."""
        class_name = self.cfg['solution']['class']
        method_name = self.cfg['solution']['method']['name']
        args_name = self.cfg['solution']['method']['args']

        src = _SOLUTION_TEMPLATE.format(
            class_name, method_name, ', '.join(args_name)
        )

        py_path = _SOLUTION_FILE_PATH.format(self.title)
        if os.path.exists(py_path):
            choice = input(f"{py_path} already exists. Overwrite? [y/n] ")
            if choice.lower() not in {'y', 'ye', 'yes'}:
                print("Abort.")
                exit(0)

        with open(py_path, 'w') as f:
            f.write(src)
        print(f"template generated at {py_path}")

    def run(self):
        sol_class = self.cfg['solution']['class']
        sol_method = self.cfg['solution']['method']['name']

        # import the test function
        py_mod = _SOLUTION_MODULE.format(self.title)
        py_mod = importlib.import_module(py_mod)
        solver = getattr(py_mod, sol_class)()
        test_func = getattr(solver, sol_method)

        # run test
        test_cases = self.cfg['test cases']
        for case in test_cases:
            input = case['input']
            expect = case['expect']
            assert test_func(*input) == expect, "Test failed"
        print("Test passed")


if __name__ == '__main__':
    subcommand = sys.argv[1]
    if subcommand == 'generate':
        pid = int(sys.argv[2])
        Problem(pid, ProblemList()).generate()
    elif subcommand == 'run':
        if len(sys.argv) <= 2:
            ProblemList().run_all()
        else:
            pid = int(sys.argv[2])
            Problem(pid, ProblemList()).run()
    elif subcommand == 'list':
        print(ProblemList())
    elif subcommand == 'add':
        name = sys.argv[2]
        ProblemList().add_problem(name)
    else:
        eprint(f"unknown subcommand: {subcommand}")
        exit(1)
