import sys

tokens = map(lambda s: s.strip().split(), open(sys.argv[1]).readlines())
a,b = zip(*[(int(t[0]),int(t[-1])) for t in tokens])

a = sorted(a)
b = sorted(b)

s = 0
for x,y in zip(a,b):
  s += abs(x-y)

print(s)

freq = dict()
for x in b:
  freq[x] = freq.get(x, 0) + 1

t = 0
for x in a:
  t += x * freq.get(x, 0)

print(t)
