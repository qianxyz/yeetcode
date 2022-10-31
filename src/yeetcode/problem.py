from typing import get_type_hints
from .struct import serialize, deserialize_kwargs, ListNode


class Problem:
    def __init__(self, class_name: str, methods: dict, test_cases: list):
        self.class_name = class_name
        self.methods = methods
        self.test_cases = test_cases

    def generate_py(self) -> str:
        """Generate a template solution file."""
        src = ""

        import re

        # collect imports
        typings = set()
        structs = set()
        for args in self.methods.values():
            for typ in args.values():
                if typ is None:
                    continue
                for k in ["List", "Optional"]:
                    if re.search(k + r"\[.*\]", typ) is not None:
                        typings.add(k)
                for k in ["ListNode", "TreeNode"]:
                    if k in typ:
                        structs.add(k)
        if typings:
            src += f"from typing import {', '.join(sorted(typings))}\n"
        if structs:
            src += f"from yeetcode import {', '.join(sorted(structs))}\n"
        if "ListNode" in structs:
            src += ListNode.__doc__

        src += f"class {self.class_name}:\n"
        for name, args in self.methods.items():
            args_tmp = args.copy()
            ret_type = args_tmp.pop("return", None)
            arg_str = ", ".join(
                ["self"] + [f"{k}: {v}" for k, v in args_tmp.items()]
            )
            src += f"    def {name}({arg_str}) -> {ret_type}: pass\n"

        from black import format_str, FileMode

        src = format_str(src, mode=FileMode(line_length=79))
        return src

    def run_tests(self, module):
        raise NotImplementedError


class SingleMethodProblem(Problem):
    def run_tests(self, module):
        # create instance of base class (`Solution` or something)
        cls = getattr(module, self.class_name)
        sol_instance = cls()
        # get the test function
        [func_name] = list(self.methods.keys())
        test_func = getattr(sol_instance, func_name)
        type_hints = get_type_hints(test_func)

        for kwargs in self.test_cases:
            expect = kwargs.pop("return", None)
            kwargs_de = deserialize_kwargs(kwargs, type_hints)
            ret = test_func(**kwargs_de)
            ret_ser = serialize(ret, type_hints["return"])
            assert ret_ser == expect, "test failed"
        print("test passed")


class MultiMethodProblem(Problem):
    def run_tests(self, module):
        cls = getattr(module, self.class_name)

        for routine in self.test_cases:
            sol_instance = None
            for action in routine:
                assert len(action) == 1, "illegal step"
                [(func_name, kwargs)] = list(action.items())
                if kwargs is None:
                    kwargs = {}
                expect = kwargs.pop("return", None)
                if func_name == "__init__":
                    assert sol_instance is None, "multiple __init__"
                    type_hints = get_type_hints(cls.__init__)
                    kwargs_de = deserialize_kwargs(kwargs, type_hints)
                    sol_instance = cls(**kwargs_de)
                else:
                    assert sol_instance is not None, "not initialized"
                    test_func = getattr(sol_instance, func_name)
                    type_hints = get_type_hints(test_func)
                    kwargs_de = deserialize_kwargs(kwargs, type_hints)
                    ret = test_func(**kwargs_de)
                    ret_ser = serialize(ret, type_hints["return"])
                    assert ret_ser == expect, "test failed"
        print("test passed")
