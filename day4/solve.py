import sys

import numpy as np
import scipy


data = [line.strip() for line in open(sys.argv[1]).readlines()]

ctoi = {'X':1,'M':2,'A':3,'S':4}

grid = np.zeros((len(data),len(data[0])))
for i,line in enumerate(data):
    for j,c in enumerate(line):
        grid[i][j] = ctoi.get(c, 0)

filters = []
f = np.array([[1, 10, 100, 1000]])
filters.append(f)
filters.append(f.T)
filters.append(np.flip(f))
filters.append(np.flip(f).T)
f = np.diag([1, 10, 100, 1000])
filters.append(f)
filters.append(np.flip(f))
filters.append(np.fliplr(f))
filters.append(np.fliplr(np.flip(f)))

num_xmas = 0
for f in filters:
    conv = scipy.signal.convolve2d(grid, f, mode='valid')
    num_xmas += np.count_nonzero(conv == 4321)

print(num_xmas)

filters = []
f = np.array([[1, 0, 100],
              [0, 10, 0],
              [1000, 0, 10000]])
filters.append(f)
filters.append(f.T)
filters.append(np.flip(f))
filters.append(np.flip(f).T)

num_xmas = 0
for f in filters:
    conv = scipy.signal.convolve2d(grid, f, mode='valid')
    num_xmas += np.count_nonzero(conv == 42432)

print(num_xmas)


