import importlib
import sys
import yaml


def main():
    pid = int(sys.argv[1])

    with open("problem.yaml") as f:
        plist = yaml.safe_load(f)
    pname = plist[pid]

    yaml_path = f"problem/{pid}_{pname}.yaml"
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f)
    sol_class = cfg['solution']['class']
    sol_method = cfg['solution']['method']

    py_mod = f"solution.{pid}_{pname}"
    py_mod = importlib.import_module(py_mod)
    solver = getattr(py_mod, sol_class)()
    test_func = getattr(solver, sol_method)

    test_cases = cfg['test cases']
    for case in test_cases:
        input = case['input']
        expect = case['expect']
        assert test_func(*input) == expect, "Test failed"

    print("Test passed")


if __name__ == '__main__':
    main()
