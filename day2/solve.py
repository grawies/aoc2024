import sys

import numpy as np

reports = [np.array([int(x) for x in s.strip().split()]) for s in open(sys.argv[1]).readlines()]

num_safe = 0
for levels in reports:
  diffs = levels[1:] - levels[:-1]
  if {1,2,3}.issuperset(diffs) or {-1,-2,-3}.issuperset(diffs):
    num_safe += 1

print(num_safe)

num_dampener_safe = 0
for levels in reports:
  # While iterating over levels:
  # State: (n, s, d):
  #   n = number of processed levels
  #   s = sign / direction of levels
  #   d = skipped index, or 0
  # If we can iterate over the entire list and some state survives, we're done.
  states = {(0, -1, -1), (0, 1, -1)}
  while len(states) > 0:
    n, s, d = states.pop()
    if n == len(levels):
      num_dampener_safe += 1
      break
    if d < 0:
      states.add((n+1, s, n))
    if n == 0 or (n == 1 and d == 0):
      # No previous number to check compatibility with, auto pass.
      states.add((n+1, s, d))
      continue
    diff = levels[n] - levels[n-1 if d != n-1 else n-2]
    if diff * s > 0 and abs(diff) in [1,2,3]:
      states.add((n+1, s, d))

print(num_dampener_safe)
