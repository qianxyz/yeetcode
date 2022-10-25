class Problem:

    def __init__(self, class_name: str, methods: dict, test_cases: list):
        self.class_name = class_name
        self.methods = methods
        self.test_cases = test_cases

    def generate_py(self) -> str:
        """Generate a template solution file."""
        src = ""

        # collect imports (using primordial string matching)
        types = [t for args in self.methods.values()
                 for t in args.values() if t is not None]
        typings = ", ".join(s for s in ["List", "Optional"]
                            if any(s in t for t in types))
        structs = ", ".join(s for s in ["ListNode", "TreeNode"]
                            if any(s in t for t in types))
        if typings:
            src += f"from typing import {typings}\n"
        if structs:
            src += f"from yeetcode import {structs}\n"

        src += f"class {self.class_name}:\n"
        for name, args in self.methods.items():
            args_tmp = args.copy()
            ret_type = args_tmp.pop('__return', None)
            arg_str = ", ".join(
                ["self"] + [f"{k}: {v}" for k, v in args_tmp.items()]
            )
            src += f"    def {name}({arg_str}) -> {ret_type}: pass\n"

        from black import format_str, FileMode
        src = format_str(src, mode=FileMode())
        return src

    def run_tests(self, _):
        raise NotImplementedError


class SingleMethodProblem(Problem):
    pass


class MultiMethodProblem(Problem):
    pass
