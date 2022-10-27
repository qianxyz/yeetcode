import yaml
import importlib.util
from .problem import Problem, SingleMethodProblem, MultiMethodProblem


def load_problem(yaml_raw: str) -> Problem:
    cfg = yaml.safe_load(yaml_raw)

    test_cases = cfg.pop("tests", [])
    assert len(cfg) == 1, "too many classes"
    [(class_name, methods)] = list(cfg.items())
    if len(methods) == 1:
        return SingleMethodProblem(class_name, methods, test_cases)
    else:
        return MultiMethodProblem(class_name, methods, test_cases)


def load_module(py_raw: str, module_name: str = "solution"):
    spec = importlib.util.spec_from_loader(module_name, loader=None)
    module = importlib.util.module_from_spec(spec)
    # exec is dangerous, but it does not run on my computer
    exec(py_raw, module.__dict__)
    return module
