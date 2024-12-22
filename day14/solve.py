from dataclasses import dataclass
import queue
import re
import sys

import numpy as np

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


def advance(bots, width, height, steps):
    next_bots = []
    for px, py, vx, vy in bots:
        next_bots.append(
                (
                    (px + vx * steps) % width,
                    (py + vy * steps) % height,
                    vx,
                    vy,
                )
            )
    return next_bots

def phash(x, y):
    return 10000 * x + y

def safety_factor(bots, width, height):
    q = [[0, 0], [0, 0]]
    for px, py, _, _ in bots:
        ix = None
        iy = None
        if px < width // 2:
            ix = 0
        if px > width // 2:
            ix = 1
        if py < height // 2:
            iy = 0
        if py > height // 2:
            iy = 1
        if ix is None or iy is None:
            continue
        q[iy][ix] += 1
    return q[0][0] * q[0][1] * q[1][0] * q[1][1]

def to_map(bots, width, height):
    ps = set([phash(x,y) for x,y,_,_ in bots])
    lines = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append('#' if phash(x,y) in ps else '.')
        lines.append(''.join(line))
    return '\n'.join(lines)

pos_matcher = re.compile(r'p=(?P<x>-?\d+),(?P<y>-?\d+) v=(?P<dx>-?\d+),(?P<dy>-?\d+)')
def getbot(s):
    m = pos_matcher.search(s)
    return [int(m.group(name)) for name in ('x', 'y', 'dx', 'dy')]

if __name__ == '__main__':
    filename = sys.argv[1]
    lines = open(filename).readlines()
    bots = [getbot(line.strip()) for line in lines]
    if 'test' in filename:
        width = 11
        height = 7
    else:
        width = 101
        height = 103

    simulated_positions = advance(bots, width, height, 100)
    print(safety_factor(simulated_positions, width, height))

    # I noted a repeating clustering of points every 101 steps, starting at step 20.
    # Investigating.
    for i in range(20, 10000, 101):
        simulated_positions = advance(bots, width, height, i)
        print(f'{i}')
        print(to_map(simulated_positions, width, height))
        print('\n')

    print(to_map(advance(bots, width, height, 6888), width, height))

