import sys

from .loader import load_problem, load_module


def main():
    subcommand = sys.argv[1]
    if subcommand == "template":
        yaml_path = sys.argv[2]
        problem = load_problem(yaml_path)
        src = problem.generate_py()
        # just print the template to stdout, let user redirect
        print(src, end="")
    elif subcommand == "run":
        yaml_path = sys.argv[2]
        py_path = sys.argv[3]
        problem = load_problem(yaml_path)
        module = load_module(py_path)
        problem.run_tests(module)
