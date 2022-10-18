class Search:

    def two_crystal_balls(self, breaks):
        import math
        step = int(math.sqrt(len(breaks)))

        i = step
        while i < len(breaks):
            if breaks[i]:
                break
            i += step

        i -= step
        j = 0
        while j < step and i < len(breaks):
            if breaks[i]:
                return i
            i += 1
            j += 1
        return None
