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


key_pos_0 = {
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
}

key_pos_1 = {
            'A': (2,0),
            '^': (1,0),
            'v': (1,-1),
            '<': (0,-1),
            '>': (2,-1),
}

pos_key_0 = {v:k for k,v in key_pos_0.items()}
pos_key_1 = {v:k for k,v in key_pos_1.items()}

key_dir = {
        '>': RIGHT,
        '<': LEFT,
        '^': UP,
        'v': DOWN,
}

syms0 = '0123456789A'
syms1 = '<>v^A'

def advance(pos, instruction, kp, pk):
    if instruction in key_dir:
        d = key_dir[instruction]
        p = kp[pos]
        np = add(p, d)
        if np in pk:
            return pk[np]
        else:
            # Invalid position, panic.
            return None
    # Not a directional instruction, no movement.
    return pos

def shortest_path(code, num_intermediates):
    states = list(it.product(syms1, syms1, syms0, range(len(code)+1)))
    nbrs = {state: [] for state in states}
    for state in states:
        a,b,c,d = state
        # All possible key presses on the human-controlled keypad.
        # Directions.
        for k in key_dir:
            # Directional instruction, try to advance a.
            na = advance(a, k, key_pos_1, pos_key_1)
            if na is not None:
                nbrs[state].append((na,b,c,d))
        # A.
        # Pressing button |a| on next keypad.
        if a in key_dir:
            # Advance b.
            nb = advance(b, a, key_pos_1, pos_key_1)
            if nb is not None:
                nbrs[state].append((a,nb,c,d))
        else:
            # A on the next keypad.
            if b in key_dir:
                # Advance c.
                nc = advance(c, b, key_pos_0, pos_key_0)
                if nc is not None:
                    nbrs[state].append((a,b,nc,d))
            else:
                # A on the next keypad.
                # Execute command c.
                if d < len(code) and code[d] == c:
                    nbrs[state].append((a,b,c,d+1))

    start = ('A','A','A',0)
    end = ('A','A','A',len(code))
    print(f'finding path from {start} to {end}')
    to_visit = queue.PriorityQueue()
    to_visit.put((0, start))
    visited = set((start,))
    while not to_visit.empty():
        steps, state = to_visit.get()
        print(f'  visiting {state} after {steps} steps')
        if state == end:
            return steps
        for ns in nbrs[state]:
            if ns not in visited:
                print(f'  new neighbor: {ns}')
                visited.add(ns)
                to_visit.put((steps+1, ns))

    return None

if __name__ == '__main__':
    filename = sys.argv[1]
    codes = [l.strip() for l in open(filename).readlines()]

    complexity_sum = 0
    for code in codes:
        min_sequence = shortest_path(code)
        print(f'path for robot 3: {min_sequence}')
        print(f'  robot multiplier code: {int(code[:-1])}')
        complexity_sum += int(code[:-1]) * min_sequence

    print(complexity_sum)
