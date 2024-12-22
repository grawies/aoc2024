from dataclasses import dataclass
from enum import Enum
import queue
import re
import sys

import numpy as np

LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,1)
DOWN = (0,-1)
DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


DEBUG = False

def min_path(points, h, w, k):
    obst = set((x,y) for x,y in points[:k])

    def in_bounds(p):
        return p[0] >= 0 and p[0] < w and p[1] >= 0 and p[1] < h

    start = (0, 0)
    end = (w-1, h-1)
    num_steps = 0
    positions = [start]
    visited = set(positions)
    while len(positions) > 0:
        if end in positions:
            break
        num_steps += 1
        new_positions = []
        for p in positions:
            for d in DIRECTIONS:
                np = (p[0]+d[0],  p[1]+d[1])
                if np not in visited and in_bounds(np) and np not in obst:
                    visited.add(np)
                    new_positions.append(np)
        positions = new_positions
        #print(f'map after {num_steps} steps:\n{to_map(h,w,positions,obst)}')
    else:
        return None

    return num_steps


def to_map(h, w, positions, o):
    s = set(positions)
    lines = []
    for y in range(h):
        line = []
        for x in range(w):
            if (x,y) in o:
                line.append('#')
            elif (x,y) in s:
                line.append('O')
            else:
                line.append('.')
        lines.append(''.join(line))
    return '\n'.join(lines)


def binary_search(xs, predicate):
    lo = 0
    hi = len(xs)
    # Always search in [lo,hi)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        match predicate(mid):
            case False:
                lo = mid
            case True:
                hi = mid
    # [lo, hi) = [x, x+1)
    return lo if predicate(lo) else lo + 1 if predicate(lo + 1) else hi

if __name__ == '__main__':
    filename = sys.argv[1]
    lines = [line.strip() for line in open(filename).readlines()]
    points = [[int(x) for x in line.split(',')] for line in lines]
    h,w = 71, 71
    k = 1024
    if 'test' in filename:
        h,w = 7, 7
        k = 12

    min_steps_after_k = min_path(points, h, w, k)
    print(min_steps_after_k)

    predicate = lambda k: min_path(points, h, w, k) is None
    num_bytes_to_failure = binary_search(list(range(len(points))), predicate)
    fail_byte = points[num_bytes_to_failure - 1]
    print(','.join(str(x) for x in fail_byte))
