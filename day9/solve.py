import math
import queue
import sys

import numpy as np

code = open(sys.argv[1]).read().strip()
lens = [int(c) for c in code]

i = 0  # forward index
j = len(lens)-1  # backward index

s = 0
index = 0
while i <= j:
    if i % 2 == 0:
        # File occupies space, add it to sum.
        fid = i // 2
        block_len = lens[i]
        s += fid * (2 * index + block_len - 1) * block_len // 2
        index += block_len
        i += 1
    else:
        # Take data from the other end of memory.
        available_mem = lens[i]
        next_file_len = lens[j]
        fid = j // 2
        block_len = min(available_mem, next_file_len)
        s += fid * (2 * index + block_len - 1) * block_len // 2
        index += block_len
        if available_mem == block_len:
            i += 1
        else:
            lens[i] -= block_len
        if next_file_len == block_len:
            j -= 2
        else:
            lens[j] -= block_len

print(s)

s = 0
lens = [int(c) for c in code]
mem_locs = np.zeros((len(lens) + 1), dtype=np.int64)
mem_locs[1:] = np.cumsum(lens)
best_indices = {block_size: queue.PriorityQueue() for block_size in range(1, 10)}
for i in range(1, len(lens), 2):
    block_size = lens[i]
    if block_size > 0:
        best_indices[block_size].put(i)

for j in range(len(lens) - 1, -1, -2):
    fid = j // 2
    file_size = lens[j]
    file_loc = mem_locs[j]
    # Find location with minimal index that matches the file.
    min_viable_index = j
    viable_block_size = 0
    for block_size, index_queue in best_indices.items():
        if block_size < file_size or index_queue.empty():
            continue
        index = index_queue.get()
        if index < min_viable_index:
            if min_viable_index != j:
                # Reinsert the ditched block into its queue.
                best_indices[viable_block_size].put(min_viable_index)
            min_viable_index = index
            viable_block_size = block_size
        else:
            index_queue.put(index)

    # Add the file to sum, using selected location to compute checksum.
    s += fid * (2 * mem_locs[min_viable_index] + file_size - 1) * file_size // 2
    remaining_block_size = viable_block_size - file_size
    if min_viable_index != j and remaining_block_size > 0:
        mem_locs[min_viable_index] += file_size
        best_indices[remaining_block_size].put(min_viable_index)

print(s)
