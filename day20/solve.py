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


def read_map(s):
    m = []
    for y, line in enumerate(s.split('\n')):
        row = []
        for x, c in enumerate(line):
            row.append(c)
            if c == 'S':
                startpos = (x,y)
            if c == 'E':
                endpos = (x, y)
        m.append(row)
    height = len(m)
    width = len(m[0])
    return m, height, width, startpos, endpos


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def mul(x, c):
    return (c * x[0], c * x[1])


def shortest_path(m, h, w, s, e, cheat_threshold, cheat_duration):
    distmap = {s: 0}
    visited = set([s])
    to_visit = queue.PriorityQueue()
    to_visit.put((0, s))
    path_length = None
    while not to_visit.empty():
        steps, p = to_visit.get()
        distmap[p] = steps

        if p == e:
            path_length = steps
            break

        for d in (LEFT, RIGHT, UP, DOWN):
            np = add(p, d)
            if m[np[1]][np[0]] != '#' and np not in visited:
                # Can move here.
                visited.add(np)
                to_visit.put((steps + 1, np))

    def in_bounds(p):
        return p[0] >= 0 and p[0] < w and p[1] >= 0 and p[1] < h
    def is_blocked(p):
        return m[p[1]][p[0]] == '#'
    def valid_pos(p):
        return in_bounds(p) and not is_blocked(p)

    cheat_vectors = []
    # Adjust cheat duration for later logic to decide when to activate.
    cheat_duration -= 2
    # a+b for all integers a,b with |a|+|b| = cheat_duration
    for i in range(-cheat_duration, cheat_duration + 1):
        remaining_steps = cheat_duration - abs(i)
        for j in range(-remaining_steps, remaining_steps + 1):
            vector = add(mul(RIGHT, i), mul(UP, j))
            cheat_vectors.append(vector)

    num_good_cheats = {}
    cheats = set()
    for y in range(h):
        for x in range(w):
            p = (x,y)
            if not valid_pos(p):
                continue
            steps = distmap[p]
            # Try all relevant cheats.
            for d1 in (LEFT, RIGHT, UP, DOWN):
                for d2 in cheat_vectors:
                    for d3 in (LEFT, RIGHT, UP, DOWN):
                        cheat_start = add(p, d1)
                        cheat_end = add(cheat_start, d2)
                        np = add(cheat_end, d3)
                        cheat = (p, np)
                        if cheat in cheats:
                            continue
                        if not valid_pos(np):
                            continue
                        d = add(d1, add(d2, d3))
                        cheat_len = abs(d[0]) + abs(d[1])
                        cheats.add(cheat)
                        saved_steps = distmap[np] - steps - cheat_len
                        if saved_steps >= cheat_threshold:
                            if saved_steps not in num_good_cheats:
                                num_good_cheats[saved_steps] = 0
                            num_good_cheats[saved_steps] += 1
                    continue

    return path_length, sum(num_good_cheats.values())


def to_map(m, h, w, s):
    lines = []
    for y in range(h):
        line = []
        for x in range(w):
            line.append(m[y][x] if (x,y) not in s else 'O')
        lines.append(''.join(line))
    return '\n'.join(lines)


if __name__ == '__main__':
    filename = sys.argv[1]
    s = open(filename).read().strip()
    m, h, w, s, e = read_map(s)
    cheat_threshold = 100
    if 'test' in filename:
        cheat_threshold = 50

    shortest_path_t, num_good_short_cheats = shortest_path(
            m, h, w, s, e,
            cheat_threshold=1 if 'test' in filename else 100,
            cheat_duration=2)
    print(f'shortest path: {shortest_path_t}')
    print(f'num good short cheats: {num_good_short_cheats}')

    shortest_path_t, num_good_long_cheats = shortest_path(
            m, h, w, s, e,
            cheat_threshold=50 if 'test' in filename else 100,
            cheat_duration=20)
    print(f'shortest path: {shortest_path_t}')
    print(f'num good long cheats: {num_good_long_cheats}')
