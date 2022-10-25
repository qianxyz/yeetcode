import sys
import yaml
import importlib.util
from .problem import Problem, SingleMethodProblem, MultiMethodProblem


def load_problem(yaml_path: str) -> Problem:
    with open(yaml_path) as f:
        cfg = yaml.safe_load(f)

    test_cases = cfg.pop("tests", [])
    assert len(cfg) == 1, "too many classes"
    [(class_name, methods)] = list(cfg.items())
    if len(methods) == 1:
        return SingleMethodProblem(class_name, methods, test_cases)
    else:
        return MultiMethodProblem(class_name, methods, test_cases)


def load_module(py_path: str, module_name: str = "solution"):
    spec = importlib.util.spec_from_file_location(module_name, py_path)
    assert spec is not None, "cannot load module"
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None, "cannot get loader"
    spec.loader.exec_module(module)
    return module
