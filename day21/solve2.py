from dataclasses import dataclass
from enum import Enum
import itertools as it
import queue
import re
import sys

import numpy as np

LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,1)
DOWN = (0,-1)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def mul(x, c):
    return (c * x[0], c * x[1])


def pad_seq_table():
    """Map to press c2 starting at c1 for c1,c2 in [0-9A] or in [<>^vA].

    Examples:
      seq['16'] = '>>^A'
      seq['<^'] = '>^A'
    """
    pos = {
            '0': (1,0),
            'A': (2,0),
            '1': (0,1),
            '2': (1,1),
            '3': (2,1),
            '4': (0,2),
            '5': (1,2),
            '6': (2,2),
            '7': (0,3),
            '8': (1,3),
            '9': (2,3),
            '^': (1,0),
            'v': (1,-1),
            '<': (0,-1),
            '>': (2,-1),
        }
    pos = {k: np.array(v, dtype=np.int64) for k,v in pos.items()}
    seq = {}
    for s,ps in pos.items():
        for t,pt in pos.items():
            key = s + t
            val = []
            dx, dy = pt - ps
            val.append(('>' if dx > 0 else '<') * abs(dx))
            val.append(('^' if dy > 0 else 'v') * abs(dy))
            # Ensure we do not pass through (0,0), which does not exist.
            # This only happens if we go left before we go up / down.
            # Other situations are covered by first going horizontally.
            if val[0] and val[0][0] == '<':
                val[0], val[1] = val[1], val[0]
            val.append('A')
            seq[key] = ''.join(val)

    return seq

seq_table = pad_seq_table()

def expand_code(code):
    expanded = []
    for s,t in it.pairwise('A' + code):
        print(f'bot goes from {s} to {t}')
        print(f'  steps: {seq_table[s+t]}')
        expanded.append(seq_table[s+t])
    return ''.join(expanded)


def shortest_path(code):
    print('seq_table:')
    print('\n'.join(f'  {k}: {v}' for k,v in seq_table.items()))

    # For each pair in A d1 d2 ... A:
    #   Get path
    #   Compute steps necessary on keypad to enter
    path3 = []
    print(f'path for robot 0: {code}')
    for s0,t0 in it.pairwise('A' + code):
        print(f'level 0 bot goes from {s0} to {t0}')
        print(f'  steps: {seq_table[s0+t0]}')
        for s1,t1 in it.pairwise('A' + seq_table[s0 + t0]):
            print(f'    level 1 bot goes from {s1} to {t1} and presses A')
            print(f'    steps: {seq_table[s1+t1]}')
            for s2, t2 in it.pairwise('A' + seq_table[s1 + t1]):
                print(f'      level 2 bot goes from {s2} to {t2} and presses A')
                print(f'      steps: {seq_table[s2+t2]}')
                print(f'{seq_table[s2 + t2]}\t{t2}\t')
                path3.append(seq_table[s2 + t2])

    return ''.join(path3)

if __name__ == '__main__':
    filename = sys.argv[1]
    codes = [l.strip() for l in open(filename).readlines()]

    complexity_sum = 0
    for code in codes:
        min_sequence = shortest_path(code)
        min_sequence = expand_code(expand_code(expand_code(code)))
        print(f'path for robot 3: {min_sequence}')
        print(f'  robot length: {len(min_sequence)}')
        print(f'  robot multiplier code: {int(code[:-1])}')
        complexity_sum += int(code[:-1]) * len(min_sequence)

    print(complexity_sum)
