import re
import sys

import numpy as np


memory = open(sys.argv[1]).read().strip()

s = 0
for match in re.findall(r'mul\([0-9]+,[0-9]+\)', memory):
  x,y = match.split(',')
  x,y = int(x[4:]), int(y[:-1])
  s += x * y

print(s)

s = 0
enabled = True
for match in re.findall(r'mul\([0-9]+,[0-9]+\)|do\(\)|don\'t\(\)', memory):
  if match == 'do()':
    enabled = True
  elif match == 'don\'t()':
    enabled = False
  elif enabled:
    x,y = match.split(',')
    x,y = int(x[4:]), int(y[:-1])
    s += x * y

print(s)

