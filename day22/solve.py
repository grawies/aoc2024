from dataclasses import dataclass
from enum import Enum
import itertools as it
import queue
import re
import sys

import numpy as np

def optimize_selling_sequence(seeds):
    # Consecutive differences vary from -9 to +9: 19 different values.
    BASE = 19
    KEY_REDUCTION = BASE**3
    NUM_KEYS = BASE**4

    end_hash_sum = 0
    total_sum = np.zeros(NUM_KEYS, dtype=np.int64)

    N = 1 << 24
    def adv(x):
        x = (x ^ (x << 6)) % N
        x = x ^ (x >> 5)
        x = x ^ (x << 11)
        x = x % N
        return x

    for x in seeds:
        maxdict = np.zeros(NUM_KEYS, dtype=np.int64) - 1
        a = x % 10
        x = adv(x)
        b = x % 10
        x = adv(x)
        c = x % 10
        x = adv(x)
        d = x % 10
        key = 0
        for y in (b-a,c-b,d-c):
            key = key * BASE + y + 9
        for _ in range(1997):
            x = adv(x)
            a, b, c, d = b, c, d, x % 10
            key = BASE * (key % KEY_REDUCTION) + (d-c+9)
            if maxdict[key] < 0:
                maxdict[key] = d

        end_hash_sum += x
        total_sum += np.clip(maxdict, a_min=0, a_max=None)

    return end_hash_sum, max(total_sum)

if __name__ == '__main__':
    filename = sys.argv[1]
    seeds = [int(l.strip()) for l in open(filename).readlines()]

    hash_sum, max_num_bananas = optimize_selling_sequence(seeds)
    print(hash_sum)
    print(max_num_bananas)
