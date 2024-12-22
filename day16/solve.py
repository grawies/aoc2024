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

TURN_LEFT = [[0, -1],[1,0]]
TURN_RIGHT = [[0, 1],[-1,0]]


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])

def mul(m, x):
    return tuple(
            sum(
                m[r][c] * x[c]
                for c in range(len(m[0]))
            )
            for r in range(len(m))
        )


def all_shortest_paths(s):
    m, h, w, s, e = read_map(s)
    start_state = (s, RIGHT)
    visit_source = {start_state: (0, set())}
    visited = set()
    to_visit = queue.PriorityQueue()
    to_visit.put((0, start_state, None))
    endscore = None
    while not to_visit.empty():
        score, state, pstate = to_visit.get()
        p, d = state

        if state not in visit_source:
            visit_source[state] = (score, set([pstate]))
        elif visit_source[state][0] == score:
            visit_source[state][1].add(pstate)

        if state in visited:
            continue

        visited.add(state)

        if endscore is not None and score > endscore:
            # No more ends, stop.
            break
        if p == e:
            endscore = score
            continue

        np = add(p, d)
        fwd_state = (np, d)
        if m[np[1]][np[0]] != '#':
            to_visit.put((score + 1, fwd_state, state))
        for mat in (TURN_LEFT, TURN_RIGHT):
            nd = mul(mat, d)
            next_state = (p, nd)
            to_visit.put((score + 1000, next_state, state))

    num_tiles_on_path = 0
    source_states = set()
    rev_states = set([(e, d) for d in (LEFT, RIGHT, UP, DOWN)])
    while len(rev_states) > 0:
        prev_states = set()
        for state in rev_states:
            if state not in visit_source:
                continue
            prev_states.update(visit_source[state][1])
            source_states.add(state[0])
        rev_states = prev_states

    #print(to_map(m, h, w, source_states))

    return endscore, len(source_states)


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
    score, tiles = all_shortest_paths(s)
    print(f'lowest score: {score}')
    print(f'number of tiles: {tiles}')
