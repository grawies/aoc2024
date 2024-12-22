import sys

import numpy as np

def hash(a, b=[0,0]):
    return a[0] + a[1] * 1_000 + b[0] * 1_000_000 + b[1] * 1_000_000_000

obstacles = set()
for y, line in enumerate(open(sys.argv[1]).readlines()):
    width = len(line)
    height = y+1
    for x,c in enumerate(line.strip()):
        if c == '#':
            obstacles.add(hash([x,y]))
        elif c != '.':
            pos = np.array([x,y])
            direc = np.array({
                '^': [0, -1],
                'v': [0, 1],
                '>': [1, 0],
                '<': [-1, 0],
                }[c])

# If the guard exits the map from this configuration, returns the number of visited positions. Else return None.
def count_positions(pos, direc, extra_obstacle=np.array([-1,-1])):
    visited = set()
    visited_states = set()
    while pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height:
        if hash(pos, direc) in visited_states:
            return None
        visited.add(hash(pos))
        visited_states.add(hash(pos, direc))
        fpos = pos + direc
        if hash(fpos) not in obstacles and any(fpos != extra_obstacle):
            pos = fpos
        else:
            direc = np.matmul(np.array([[0, -1], [1, 0]]), direc)
    return len(visited)

print(count_positions(pos, direc))

visited = set()
loops = 0
while pos[0] >= 0 and pos[0] < width and pos[1] >= 0 and pos[1] < height:
    visited.add(hash(pos))
    fpos = pos + direc
    if hash(fpos) not in obstacles:
        if hash(fpos) not in visited:
            is_loop = (count_positions(pos, direc, fpos) is None)
            if is_loop:
                loops += 1
        pos = fpos
    else:
        direc = np.matmul(np.array([[0, -1], [1, 0]]), direc)

print(loops)
