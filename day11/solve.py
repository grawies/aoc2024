from dataclasses import dataclass
import math
import queue
import sys

import numpy as np

lines = open(sys.argv[1]).readlines()
stones = [int(s) for s in lines[0].strip().split()]

def add_val(x, n, d):
    if x not in d:
        d[x] = 0
    d[x] += n

def sim(num_steps):
    freq = {x: 1 for x in stones}
    for i in range(num_steps):
        new_freq = {}
        for x, n in freq.items():
            if x == 0:
                add_val(1, n, new_freq)
                continue
            num_digits = int(math.log10(x)) + 1
            if num_digits % 2 == 0:
                q = int(10**(num_digits // 2))
                add_val(x // q, n, new_freq)
                add_val(x % q, n, new_freq)
            else:
                add_val(x * 2024, n, new_freq)
        freq = new_freq
    return sum(freq.values())

print(sim(25))
print(sim(75))

