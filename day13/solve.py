from dataclasses import dataclass
import math
import queue
import re
import sys

import numpy as np

pos_matcher = re.compile(r'X.(?P<x>\d*), Y.(?P<y>\d*)')
def getpos(s):
    m = pos_matcher.search(s)
    return np.array((int(m.group('x')), int(m.group('y'))), dtype=np.int64)

def euclid(a, b, c):
    """Solves ax + by = c, diophantine.

    Requires a >= b.
    Requires gcd(a,b) | c.
    """
    if b == 0:
        return c // a, 0

    q = a // b
    r = a - b * q
    x0, y0 = euclid(b, r, c)
    return y0, x0 - q * y0

def gcd(a, b):
    a = abs(a)
    b = abs(b)
    if a * b == 0:
        return max(a, b)
    if b > a:
        a,b = b,a
    while b != 0:
        q = a // b
        a, b = b, a - b * q
    return a

def diophantine(a, b, c):
    """Parameterizes all integer solutions to ax + by = c.

    Returns x0, y0, dx, dy such that:
        x0 + n * dx, y0 + n * dy
    is a solution for all n, with x0 non-negative for n >= 0 and minimal for n = 0.

    If there are no solutions, returns None.
    """
    g = gcd(a, b)
    if c % g != 0:
        return None

    if a < b:
        x0, y0, dx, dy = diophantine(b, a, c)
        return y0, x0, dy, dx

    if g != 1:
        a //= g
        b //= g
        c //= g
    x0, y0 = euclid(max(a,b), min(a,b), c)
    dx = b
    dy = -a
    n0 = -(x0 // dx)
    x0, y0 = x0 + n0 * dx, y0 + n0 * dy
    return x0, y0, dx, dy

def dioptimize(inputs, offset):
    num_tokens = 0
    for a,b,c in inputs:
        c += offset
        # Find all solutions for x, y in:
        #   a[0] x + b[0] y = c[0]
        initial_solution = diophantine(a[0], b[0], c[0])
        if initial_solution is None:
            continue
        x0, y0, dx, dy = initial_solution
        # Now solve for n in:
        #   a[1] x + b[1] y = c[1]
        #   x = x0 + n * dx
        #   y = y0 + n * dy
        # Substitution reduces this to s * n = t, with:
        s = a[1]* dx + b[1] * dy
        t = c[1] - a[1] * x0 - b[1] * y0
        if s == 0:
            # All n are solutions. Pick n = 0, which minimizes x.
            n = 0
        elif t % s == 0:
            n = t // s
        else:
            # No solutions.
            continue
        x = x0 + n * dx
        y = y0 + n * dy
        if x >= 0 and y >= 0:
            num_tokens += 3 * x + y
    return num_tokens

if __name__ == '__main__':
    blocks = open(sys.argv[1]).read().strip().split('\n\n')
    inputs = [[getpos(line) for line in block.split('\n')] for block in blocks]

    print(dioptimize(inputs, 0))
    print(dioptimize(inputs, 10_000_000_000_000))
