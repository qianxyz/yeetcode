import importlib
import os
import sys
import yaml


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


class Problem:

    _SOLUTION_MODULE = "solution.{}_{}"
    _SOLUTION_FILE_PATH = "solution/{}_{}.py"

    def __init__(self, pid: int, name: str,
                 clazz: str, method: dict, test: list) -> None:
        self.pid = pid
        self.name = name
        self.sol_mod = self._SOLUTION_MODULE.format(pid, name)
        self.sol_pth = self._SOLUTION_FILE_PATH.format(pid, name)
        self.clazz = clazz
        self.method = method
        self.test = test

    def generate_py(self):
        """Generate a template solution file."""
        import_optional = False

        src = f"""\
class {self.clazz}:
"""
        for name, args in self.method.items():

            # check if we need to from typing import Optional
            types = args.values()
            if any('Optional' in t for t in types if t is not None):
                import_optional = True

            ret_type = args.pop('__return')
            arg_str = ", ".join(
                ["self"] + [f"{k}: {v}" for k, v in args.items()]
            )
            src += f"""\

    def {name}({arg_str}) -> {ret_type}:
        pass
"""

        if import_optional:
            src = "from typing import Optional\n\n\n" + src

        if os.path.exists(self.sol_pth):
            choice = input(f"{self.sol_pth} already exists. Overwrite? [y/n] ")
            if choice.lower() not in {'y', 'ye', 'yes'}:
                print("Abort.")
                exit(0)

        with open(self.sol_pth, 'w') as f:
            f.write(src)
        print(f"template generated at {self.sol_pth}")

    def run(self):
        raise NotImplementedError


class ProblemList:

    _PROBLEM_LIST = "problem.yaml"
    _CONFIG_TEMPLATE = """"""  # TODO
    _CONFIG_PATH = "problem/{}_{}.yaml"

    def __init__(self) -> None:
        with open(self._PROBLEM_LIST) as f:
            self.plist: dict = yaml.safe_load(f)

    def get_problem(self, pid: int) -> Problem:
        """Factory method to get a problem instance."""
        name = self.plist[pid]
        cfg_path = self._CONFIG_PATH.format(pid, name)
        with open(cfg_path) as f:
            cfg: dict = yaml.safe_load(f)

        test = cfg.pop('__test')
        assert len(cfg) == 1, "too many classes"
        [(clazz, method)] = list(cfg.items())
        if len(method) == 1:
            return SingleMethodProblem(pid, name, clazz, method, test)
        else:
            return MultiMethodProblem(pid, name, clazz, method, test)

    def add_problem(self, name):
        new_id = max(self.plist) + 1
        self.plist[new_id] = name
        with open(self._PROBLEM_LIST, 'w') as f:
            yaml.safe_dump(self.plist, f)

        cfg_path = self._CONFIG_PATH.format(new_id, name)
        with open(cfg_path, 'w') as f:
            f.write(self._CONFIG_TEMPLATE)
        print(f"config template generated at {cfg_path}")

    def run_all(self):
        for pid in self.plist:
            problem = self.get_problem(pid)
            problem.run()

    def __str__(self) -> str:
        return '\n'.join(f"{id}: {name}" for id, name in self.plist.items())


class SingleMethodProblem(Problem):

    def run(self):
        # import the test function
        py_mod = importlib.import_module(self.sol_mod)
        solver = getattr(py_mod, self.clazz)()
        [test_func] = list(self.method.keys())
        test_func = getattr(solver, test_func)

        # run test
        for kwargs in self.test:
            expect = kwargs.pop('__return')
            assert test_func(**kwargs) == expect, "Test failed"
        print("Test passed")


class MultiMethodProblem(Problem):

    def run(self):
        py_mod = importlib.import_module(self.sol_mod)
        clazz = getattr(py_mod, self.clazz)

        for routine in self.test:
            solver = None
            for action in routine:
                [(name, args)] = list(action.items())
                if args is None:
                    args = {}
                expect = args.pop('__return', None)
                if name == '__init__':
                    assert solver is None, "multiple __init__ in one routine"
                    solver = clazz(**args)
                else:
                    assert solver is not None, "class not initialized"
                    test_fn = getattr(solver, name)
                    assert test_fn(**args) == expect, "Test failed"
        print("Test passed")


if __name__ == '__main__':
    subcommand = sys.argv[1]
    if subcommand == 'generate':
        pid = int(sys.argv[2])
        ProblemList().get_problem(pid).generate_py()
    elif subcommand == 'run':
        if len(sys.argv) <= 2:
            ProblemList().run_all()
        else:
            pid = int(sys.argv[2])
            ProblemList().get_problem(pid).run()
    elif subcommand == 'list':
        print(ProblemList())
    elif subcommand == 'add':
        name = sys.argv[2]
        ProblemList().add_problem(name)
    else:
        eprint(f"unknown subcommand: {subcommand}")
        exit(1)
