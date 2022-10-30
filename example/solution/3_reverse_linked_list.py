from typing import Optional
from yeetcode import ListNode


class Solution:
    def reverse_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        h = self.reverse_list(head.next)
        head.next.next = head
        head.next = None
        return h
