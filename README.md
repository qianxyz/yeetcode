# Yeetcode

[![PyPI version](
https://badge.fury.io/py/yeetcode.svg
)](https://badge.fury.io/py/yeetcode)
[![CI status](
https://github.com/qianxyz/yeetcode/actions/workflows/ci.yml/badge.svg
)](https://github.com/qianxyz/yeetcode/actions)

> Why leetcode, if you can write your own?

Yeetcode is a leetcode imitation, where you can create your own
declarative problem specifications with YAML, auto-generate a solution
template in Python, fill in your solution, then run against your own
test cases.

## Quick start

### User

1. Create and activate a [virtual environment](
   https://docs.python.org/3/library/venv.html) (highly recommended)
2. Upgrade pip and install yeetcode:
```sh
python -m pip install --upgrade pip
python -m pip install yeetcode
```
3. Create a [problem configuration](./example/README.md)
4. Generate a Python solution template:
```sh
yeetcode template problem.yaml > solution.py
```
5. Work out your solutions in the `.py` file
6. Run against your test cases:
```sh
yeetcode run problem.yaml solution.py
```

### Developer

Clone this repo and install in development mode with test dependencies:
```sh
python -m pip install -e .[tests]
```

## Roadmap

- [x] Create a minimal proof of concept
- [x] Solution files auto-generation
- [x] Multiple methods test routine
- [x] Data structure: singly linked list
- [x] Data structure: binary tree
- [ ] Prettify user messages
- [ ] Docstring field describing problem
- [ ] Problem config documentation
- [ ] Inplace problems with no return
