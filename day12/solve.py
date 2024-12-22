from dataclasses import dataclass
import queue
import sys

import numpy as np

lines = open(sys.argv[1]).readlines()
grid = np.array([[ord(c) for c in line.strip()] for line in lines], dtype=np.int64)
height = len(grid)
width = len(grid[0])

@dataclass
class Point:
    x: int
    y: int

    def in_bounds(self):
        res = self.x >= 0 and self.x < width and self.y >= 0 and self.y < height
        return res

    def nbrs(self):
        ns = []
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            p = Point(self.x + dx, self.y + dy)
            if p.in_bounds():
                ns.append(p)
        return ns

    def maybe_nbrs(self):
        ns = []
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
            p = Point(self.x + dx, self.y + dy)
            ns.append(p)
        return ns

    def maybe_nbrs_incl_diag(self):
        ns = []
        for dx,dy in [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            p = Point(self.x + dx, self.y + dy)
            ns.append(p)
        return ns

    def __eq__(self, q):
        return self.__hash__() == q.__hash__()

    def __hash__(self):
        return self.x * (1 << 16) + self.y

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return str(self)


# DFS over map
# for each region, count up area and perimeter during DFS
# for part 2, we count the corners instead

def is_same(p, q):
    return q.in_bounds() and grid[p.y][p.x] == grid[q.y][q.x]

visited = set()
metrics = []
for y in range(height):
    for x in range(width):
        p = Point(x, y)
        if p in visited:
            continue
        # DFS from here
        to_visit = [p]
        area = 0
        perimeter = 0
        discount_perimeter = 0
        while len(to_visit) > 0:
            p = to_visit.pop()
            if p in visited:
                continue
            visited.add(p)
            area += 1
            for q in p.maybe_nbrs():
                if is_same(p,q):
                    to_visit.append(q)
                else:
                    perimeter += 1
            for cdir in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                a = is_same(p, Point(p.x+cdir[0],p.y))
                b = is_same(p, Point(p.x,p.y+cdir[1]))
                d = is_same(p, Point(p.x+cdir[0],p.y+cdir[1]))
                if not a and not b:
                    discount_perimeter += 1
                elif d:
                    pass
                elif a and b:
                    discount_perimeter += 1

        metrics.append((area, perimeter, discount_perimeter))

print(sum([a*p for a,p,_ in metrics]))

print(sum([a*dp for a,_,dp in metrics]))
