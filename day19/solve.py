from dataclasses import dataclass
from enum import Enum
import queue
import re
import sys

import numpy as np


def count_ways_to_match(query, blocks):
     # Use dynamic programming to count # of ways to get to each prefix.

     # ways[k] = num ways to build the prefix of the first k characters.
    ways = [0] * (len(query) + 1)
    ways[0] = 1

    bs = set(blocks)

    for k in range(1, len(ways)):
        for j in range(0, k):
            # Test if query[j:k] is a valid block.
            if query[j:k] in bs:
                ways[k] += ways[j]

    return ways[-1]


if __name__ == '__main__':
    filename = sys.argv[1]
    block_input, query_input = [line.strip() for line in open(filename).read().split('\n\n')]
    blocks = block_input.split(', ')
    queries = query_input.split()

    matcher = re.compile(f'({"|".join(blocks)})*')
    matchable_queries = list(filter(lambda q: matcher.fullmatch(q) is not None, queries))
    
    print(len(matchable_queries))

    total_num_ways = 0
    for q in matchable_queries:
        total_num_ways += count_ways_to_match(q, blocks)

    print(total_num_ways)
