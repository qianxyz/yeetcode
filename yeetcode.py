import importlib
import os
import sys
import yaml


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


class ProblemList:

    _PATH = "problem.yaml"

    def __init__(self) -> None:
        with open(self._PATH) as f:
            self.plist: dict = yaml.safe_load(f)

    def get_title(self, pid: int) -> str:
        name = self.plist[pid]
        return f"{pid}_{name}"

    def __str__(self) -> str:
        return '\n'.join(f"{id}: {name}" for id, name in self.plist.items())

    def add_problem(self, name):
        max_id = max(self.plist)
        self.plist[max_id + 1] = name
        with open(self._PATH, 'w') as f:
            yaml.safe_dump(self.plist, f)
        # TODO: create template problem config


class Problem:

    _CONFIG_PATH        = "problem/{}.yaml"
    _SOLUTION_MODULE    = "solution.{}"
    _SOLUTION_FILE_PATH = "solution/{}.py"
    _SOLUTION_TEMPLATE  = """\
class {}:

    def {}(self, {}):
        pass
"""

    def __init__(self, pid: int) -> None:
        self.title = ProblemList().get_title(pid)
        with open(self._CONFIG_PATH.format(self.title)) as f:
            self.cfg = yaml.safe_load(f)

    def generate(self):
        """Generate a template solution file."""
        class_name = self.cfg['solution']['class']
        method_name = self.cfg['solution']['method']['name']
        args_name = self.cfg['solution']['method']['args']

        src = self._SOLUTION_TEMPLATE.format(
            class_name, method_name, ', '.join(args_name)
        )

        py_path = self._SOLUTION_FILE_PATH.format(self.title)
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
        py_mod = self._SOLUTION_MODULE.format(self.title)
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
        Problem(pid).generate()
    elif subcommand == 'run':
        pid = int(sys.argv[2])
        Problem(pid).run()
    elif subcommand == 'list':
        print(ProblemList())
    elif subcommand == 'add':
        name = sys.argv[2]
        ProblemList().add_problem(name)
    else:
        eprint(f"unknown subcommand: {subcommand}")
        exit(1)
