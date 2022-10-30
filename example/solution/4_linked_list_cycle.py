from typing import Optional
from yeetcode import ListNode


class Solution:
    def has_cycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while slow and fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
