class Search:

    def binary_search(self, nums, target):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            p = nums[mid]
            if p == target:
                return mid
            elif p > target:
                hi = mid
            else:
                lo = mid + 1
        return None
