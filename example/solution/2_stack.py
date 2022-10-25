from typing import Optional


class Stack:
    def __init__(self) -> None:
        self.stk = []

    def is_empty(self) -> bool:
        return not self.stk

    def push(self, item: int) -> None:
        self.stk.append(item)

    def pop(self) -> Optional[int]:
        try:
            return self.stk.pop()
        except IndexError:
            return None

    def peek(self) -> Optional[int]:
        try:
            return self.stk[-1]
        except IndexError:
            return None
