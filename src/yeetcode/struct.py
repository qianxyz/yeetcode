import collections
import typing
from typing import Optional, Union


class SerdeError(Exception):
    pass


class ListNode:

    __doc__ = """

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
"""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, item):
        if not (item is None or isinstance(item, ListNode)):
            raise ValueError("next must be ListNode or None")
        self._next = item

    @staticmethod
    def _serialize(node: Optional["ListNode"]) -> Union[list, dict]:
        """
        When the linked list has no cycles, return a list of vals.
        Otherwise, return a dict { "vals": list, "pos": int }.
        See Leetcode problem #141.
        """
        # NOTE: dict preserves insertion order since Python 3.7
        if not (node is None or isinstance(node, ListNode)):
            raise SerdeError(f"{node} is not an instance of ListNode or None")
        visited = {}
        pos = 0
        while node is not None:
            if node in visited:
                return {
                    "vals": [node.val for node in visited],
                    "pos": visited[node],
                }
            visited[node] = pos
            node = node.next
            pos += 1
        return [node.val for node in visited]

    @staticmethod
    def _deserialize(data: Union[list, dict]) -> Optional["ListNode"]:
        if isinstance(data, list):
            p = None
            while data:
                p = ListNode(val=data.pop(), next=p)
            return p

        elif isinstance(data, dict):
            vals = data["vals"]
            pos = data["pos"]
            p = end = loop_entrance = None
            while vals:
                p = ListNode(val=vals.pop(), next=p)
                if end is None:
                    end = p
                if len(vals) == pos:
                    loop_entrance = p
            if end is not None:
                end.next = loop_entrance
            return p

        else:
            raise SerdeError("unsupported type to deserialize to linked list")


class TreeNode:

    __doc__ = """

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
"""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, item):
        if not (item is None or isinstance(item, TreeNode)):
            raise ValueError("subtree must be TreeNode or None")
        self._left = item

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, item):
        if not (item is None or isinstance(item, TreeNode)):
            raise ValueError("subtree must be TreeNode or None")
        self._right = item

    @staticmethod
    def _serialize(node: Optional["TreeNode"]) -> list:
        if not (node is None or isinstance(node, TreeNode)):
            raise SerdeError(f"{node} is not an instance of TreeNode or None")

        ret = []
        queue = collections.deque([node])
        while queue:
            node = queue.popleft()
            if node is not None:
                ret.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                ret.append(None)

        # trim the trailing Nones
        while ret and ret[-1] is None:
            ret.pop()
        return ret

    @staticmethod
    def _deserialize(data: list) -> Optional["TreeNode"]:
        if not isinstance(data, list):
            raise SerdeError("cannot deserialized non-list to binary tree")

        if not data:
            return None

        nodes = [None if val is None else TreeNode(val) for val in data]
        queue = collections.deque(nodes[1:])
        for node in nodes:
            if node is not None:
                if queue:
                    node.left = queue.popleft()
                if queue:
                    node.right = queue.popleft()
        return nodes[0]


# Serde utils
# Note that we do not really do serde through string.
# Parsing from/to something YAML can understand is enough.


def deserialize(yml_obj, typ: typing.Type):
    """
    type ::= int | float | str | bool | type(None)
            | ListNode
            | List[type] | Optional[type]
    """
    if typ in [int, float, str, bool, type(None)]:
        if not isinstance(yml_obj, typ):
            raise SerdeError(f"{yml_obj} is not an instance of {typ}")
        return yml_obj

    elif typ is ListNode:
        return ListNode._deserialize(yml_obj)

    elif typ is TreeNode:
        return TreeNode._deserialize(yml_obj)

    elif typing.get_origin(typ) is list:
        [subtyp] = typing.get_args(typ)
        if not isinstance(yml_obj, list):
            raise SerdeError(f"{yml_obj} is not an instance of list")
        return [deserialize(n, subtyp) for n in yml_obj]

    elif typing.get_origin(typ) is typing.Union:
        # it must be Optional[T]
        subtyp, _ = typing.get_args(typ)
        return None if yml_obj is None else deserialize(yml_obj, subtyp)

    else:
        raise NotImplementedError(f"{typ} not supported")


def deserialize_kwargs(yml_objs: dict, typs: dict) -> dict:
    ret = {}
    for name, obj in yml_objs.items():
        ret[name] = deserialize(obj, typs[name])
    return ret


def serialize(py_obj, typ: typing.Type):
    if typ in [int, float, str, bool, type(None)]:
        if not isinstance(py_obj, typ):
            raise SerdeError(f"{py_obj} is not an instance of {typ}")
        return None if isinstance(None, typ) else typ(py_obj)

    elif typ is ListNode or typ is Optional[ListNode]:
        return ListNode._serialize(py_obj)

    elif typ is TreeNode or typ is Optional[TreeNode]:
        return TreeNode._serialize(py_obj)

    elif typing.get_origin(typ) is list:
        [subtyp] = typing.get_args(typ)
        if not isinstance(py_obj, list):
            raise SerdeError(f"{py_obj} is not an instance of list")
        return [serialize(n, subtyp) for n in py_obj]

    elif typing.get_origin(typ) is typing.Union:
        # it must be Optional[T]
        subtyp, _ = typing.get_args(typ)
        return None if py_obj is None else serialize(py_obj, subtyp)

    else:
        raise NotImplementedError(f"{typ} not supported")
