from dataclasses import dataclass
import queue
import sys

import numpy as np

lines = open(sys.argv[1]).readlines()
grid = np.array([[int(c) for c in line.strip()] for line in lines], dtype=np.int64)
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

    def __eq__(self, q):
        return self.__hash__() == q.__hash__()

    def __hash__(self):
        return self.x * (1 << 16) + self.y

    def __str__(self):
        return f'({self.x},{self.y})'

    def __repr__(self):
        return str(self)

trail_metadata = {}
for y in range(height):
    for x in range(width):
        if grid[y][x] == 0:
            p = Point(x,y)
            trail_metadata[p] = [set((p,)), 1]

for i in range(9):
    new_trail_metadata = {}
    for p, (trailheads, trailcounts) in trail_metadata.items():
        for q in p.nbrs():
            if grid[q.y][q.x] == grid[p.y][p.x] + 1:
                if q not in new_trail_metadata:
                    new_trail_metadata[q] = [set(), 0]
                new_trail_metadata[q][0].update(trailheads)
                new_trail_metadata[q][1] += trailcounts
    trail_metadata = new_trail_metadata

total_trailheads = sum([len(hs) for hs,_ in trail_metadata.values()])
print(total_trailheads)

total_trailcounts = sum([n for _,n in trail_metadata.values()])
print(total_trailcounts)
