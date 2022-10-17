class Search:

    def linear_search(self, nums, target):
        for i, n in enumerate(nums):
            if n == target:
                return i
        return None
