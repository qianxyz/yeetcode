#!/usr/bin/env python3
import os
from argparse import Namespace

from yeetcode import run_solution


def listdir(dir, extension):
    return [
        os.path.join(dir, f)
        for f in sorted(os.listdir(dir))
        if f.endswith(extension)
    ]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    problem_dir = os.path.join(here, "problem")
    solution_dir = os.path.join(here, "solution")

    ymls = listdir(problem_dir, (".yaml", ".yml"))
    pys = listdir(solution_dir, ".py")

    for yml, py in zip(ymls, pys):
        print(os.path.basename(yml))
        with open(yml) as y, open(py) as p:
            args = Namespace(yaml_path=y, py_path=p)
            run_solution(args)


if __name__ == "__main__":
    main()
