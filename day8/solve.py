import itertools
import math
import sys

import numpy as np

lines = [l.strip() for l in open(sys.argv[1]).readlines()]
height = len(lines)
width = len(lines[0])

arrays = {}

for y,line in enumerate(lines):
    for x, c in enumerate(line):
        if c != '.':
            arrays.setdefault(c, []).append(np.array((x,y), dtype=np.int64))

def hash(a):
    return a[0] * 1000 + a[1]

def count_antinodes(generate_points):
    antinodes = set()
    for key in arrays:
        for p, q in itertools.permutations(arrays[key], 2):
            for r in generate_points(p, q):
                antinodes.add(hash(r))

    return len(antinodes)

def in_bounds(p):
    return p[0] >= 0 and p[0] < width and p[1] >= 0 and p[1] < height

def generate_basic_points(p, q):
    r = p + p - q
    if in_bounds(r):
        return [r]
    return []

print(count_antinodes(generate_basic_points))

def generate_resonant_points(p, q):
    points = []
    d = p - q
    # This division happens to be unnecessary for the particular input, but whatever.
    d //= math.gcd(*d)
    r = p
    while in_bounds(r):
        points.append(r)
        r = r + d
    r = q
    while in_bounds(r):
        points.append(r)
        r = r - d
    return points

print(count_antinodes(generate_resonant_points))
