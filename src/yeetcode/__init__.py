import argparse
import importlib.metadata

from .loader import load_problem, load_module
from .struct import ListNode  # noqa: F401


__version__ = importlib.metadata.version(__package__)


def print_template(args):
    problem = load_problem(args.yaml_path.read())
    src = problem.generate_py()
    # just print the template to stdout, let user redirect
    print(src, end="")


def run_solution(args):
    problem = load_problem(args.yaml_path.read())
    module = load_module(args.py_path.read())
    problem.run_tests(module)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Make your own leetcode problems"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    parser_template = subparsers.add_parser(
        "template", help="print solution template"
    )
    parser_template.add_argument(
        "yaml_path",
        type=argparse.FileType(),
        help="path to problem config",
    )
    parser_template.set_defaults(func=print_template)

    parser_run = subparsers.add_parser("run", help="run your solution")
    parser_run.add_argument(
        "yaml_path",
        type=argparse.FileType(),
        help="path to problem config",
    )
    parser_run.add_argument(
        "py_path",
        type=argparse.FileType(),
        help="path to solution",
    )
    parser_run.set_defaults(func=run_solution)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
