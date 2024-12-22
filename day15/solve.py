from dataclasses import dataclass
from enum import Enum
import queue
import re
import sys

import numpy as np

LEFT = np.array((-1,0), dtype='int64')
RIGHT = np.array((1,0), dtype='int64')
UP = np.array((0,1), dtype='int64')
DOWN = np.array((0,-1), dtype='int64')


def read_map(s, big):
    m = []
    for y, line in enumerate(s.split('\n')):
        row = []
        for x, c in enumerate(line):
            match c:
                case '@':
                    row.append('@.' if big else '@')
                    pos = np.array((2 * x if big else x, y), 'int64')
                case '.' | '#':
                    row.append(2 * c if big else c)
                case 'O':
                    row.append('[]' if big else 'O')
        m.append([c for c in ''.join(row)])
    height = len(m)
    width = len(m[0])
    return m, height, width, pos


def readmoves(s):
    move_map = {
            '^': (0, -1),
            'v': (0, 1),
            '<': (-1, 0),
            '>': (1, 0),
        }
    return [np.array(move_map[c], dtype='int64') for c in s if c !='\n']


def to_map(m, h, w):
    lines = []
    for y in range(h):
        line = []
        for x in range(w):
            line.append(m[y][x])
        lines.append(''.join(line))
    return '\n'.join(lines)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def simulate_big_robot(s, big):
    m,h,w,pos = read_map(s, big=big)
    for d in steps:
        npos = add(pos, d)
        # Detect if we can move to npos.
        if d[0] == 0:
            # Positions p that need to be moved to from position p - d.
            new_positions = [set(), set([npos])]
            can_move = True
            while True:
                maybe_moving = new_positions[-1]
                new_layer = set()
                for p in maybe_moving:
                    np = add(p, d)
                    match m[p[1]][p[0]]:
                        case '.':
                            # Can move without issue, no further action.
                            continue
                        case '#':
                            # Obstacle! Move impossible.
                            can_move = False
                            break
                        case '[':
                            # Need to move this and neighbor.
                            new_layer.update([np, add(np, RIGHT)])
                        case ']':
                            # Need to move this and neighbor.
                            new_layer.update([np, add(np, LEFT)])
                        case 'O':
                            # Need to move this.
                            new_layer.add(np)
                if not can_move:
                    break
                if not new_layer:
                    break
                new_positions.append(new_layer)
            if not can_move:
                continue

            # All that remains is to advance all positions to new_positions.
            new_positions.reverse()
            for i,layer in enumerate(new_positions):
                for np in layer:
                    pp = np - d
                    m[np[1]][np[0]] = m[pp[1]][pp[0]]
                    m[pp[1]][pp[0]] = '.'

            pos = npos

        else:
            chain = 0
            while m[npos[1]][npos[0]] in ('[', ']', 'O'):
                chain += 1
                npos += d
            end = m[npos[1]][npos[0]]
            if end == '#':
                # Blocked, no move.
                continue
            # Can move, so move all the boxes.
            assert end == '.', f'unexpected end={end}'
            for _ in range(chain + 1):
                ppos = npos - d
                m[npos[1]][npos[0]] = m[ppos[1]][ppos[0]]
                npos = ppos
            m[pos[1]][pos[0]] = '.'
            pos = pos + d

    coordinate_sum = 0
    for y in range(h):
        for x in range(w):
            if m[y][x] in ('O', '['):
                coordinate_sum += 100 * y + x
    return coordinate_sum


if __name__ == '__main__':
    filename = sys.argv[1]
    inputs = open(filename).read().split('\n\n')
    steps = readmoves(inputs[1])
   
    print(f'sum: {simulate_big_robot(inputs[0], big=False)}')
    print(f'sum: {simulate_big_robot(inputs[0], big=True)}')
