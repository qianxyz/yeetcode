import importlib
import os
import sys
import yaml


_PROBLEM_LIST = "problem.yaml"
_PROBLEM_CONFIG_PATH = "problem/{}.yaml"
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


def get_name(pid: int) -> str:
    """Return a formatted problem name."""
    with open(_PROBLEM_LIST) as f:
        plist = yaml.safe_load(f)
    pname = plist[pid]
    return f"{pid}_{pname}"


def get_problem_config(name: str) -> dict:
    """Return the YAML config of a problem."""
    cfg_path = _PROBLEM_CONFIG_PATH.format(name)
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    return cfg


def generate(pid: int):
    name = get_name(pid)

    cfg = get_problem_config(name)
    class_name = cfg['solution']['class']
    method_name = cfg['solution']['method']['name']
    args_name = cfg['solution']['method']['args']

    src = _SOLUTION_TEMPLATE.format(
        class_name, method_name, ', '.join(args_name)
    )

    py_path = _SOLUTION_FILE_PATH.format(name)
    if os.path.exists(py_path):
        choice = input(f"{py_path} already exists. Overwrite? [y/n] ")
        if choice.lower() not in {'y', 'ye', 'yes'}:
            print("Abort.")
            exit(0)

    with open(py_path, 'w') as f:
        f.write(src)
    print(f"template generated at {py_path}")


def run(pid: int):
    name = get_name(pid)

    # get the name of test function from config
    cfg = get_problem_config(name)
    sol_class = cfg['solution']['class']
    sol_method = cfg['solution']['method']['name']

    # import the test function
    py_mod = _SOLUTION_MODULE.format(name)
    py_mod = importlib.import_module(py_mod)
    solver = getattr(py_mod, sol_class)()
    test_func = getattr(solver, sol_method)

    # run test
    test_cases = cfg['test cases']
    for case in test_cases:
        input = case['input']
        expect = case['expect']
        assert test_func(*input) == expect, "Test failed"
    print("Test passed")


if __name__ == '__main__':
    subcommand = sys.argv[1]
    if subcommand == 'generate':
        pid = int(sys.argv[2])
        generate(pid)
    elif subcommand == 'run':
        pid = int(sys.argv[2])
        run(pid)
    else:
        eprint(f"unknown subcommand: {subcommand}")
        exit(1)

