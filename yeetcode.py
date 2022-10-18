import importlib
import os
import sys
import yaml


_PROBLEM_LIST = "problem.yaml"
_CONFIG_PATH = "problem/{}.yaml"
_SOLUTION_MODULE = "solution.{}"
_SOLUTION_FILE_PATH = "solution/{}.py"


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


class Problem:

    def __init__(self) -> None:
        raise NotImplementedError

    def generate_py(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class ProblemFactory:

    def __init__(self) -> None:
        with open(_PROBLEM_LIST) as f:
            self.plist = yaml.safe_load(f)

    def get_problem(self, pid: int) -> Problem:
        name = self.plist[pid]

    def add_problem(self, name):
        max_id = max(self.plist)
        self.plist[max_id + 1] = name
        with open(_PROBLEM_LIST, 'w') as f:
            yaml.safe_dump(self.plist, f)

        cfg_path = _CONFIG_PATH.format(self.get_title(max_id + 1))
        with open(cfg_path, 'w') as f:
            f.write(self._CONFIG_TEMPLATE)
        print(f"config template generated at {cfg_path}")

    def run_all(self):
        for pid in self.plist:
            problem = Problem(pid, self)
            problem.run()

    def __str__(self) -> str:
        return '\n'.join(f"{id}: {name}" for id, name in self.plist.items())


class SingleMethodProblem(Problem):

    def __init__(self, pid: int, plist: ProblemList) -> None:
        self.title = plist.get_title(pid)
        with open(_CONFIG_PATH.format(self.title)) as f:
            self.cfg: dict = yaml.safe_load(f)

        self.test = self.cfg.pop('__test')
        # assure that self.cfg only has one key left
        [(self.clazz, self.method)] = list(self.cfg.items())

        self.has_multiple_methods = (len(self.method) > 1)

    def generate(self):
        """Generate a template solution file."""
        src = [f"class {self.clazz}:", ""]
        for name, args in self.method.items():
            ret_type = args.pop('__return')
            args = ", ".join(
                ["self"] + [f"{k}: {v}" for k, v in args.items()]
            )
            src += [
                f"    def {name}({args}) -> {ret_type}:",
                "        pass", ""
            ]
        src = '\n'.join(src)

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
