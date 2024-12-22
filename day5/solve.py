from queue import Queue
import sys

poset_str, query_str = open(sys.argv[1]).read().strip().split('\n\n')

# Build forward / backward adjacency lists of pages.
fwd_adj = {} # Maps from a page u to pages that must be printed after u.
rev_adj = {} # Maps from a page u to pages that must be printed before u.

# Utility function to get the entry of key k from dict d. Inserts and returns [] if not already present.
def dget(k, d):
    if k not in d:
        d[k] = []
    return d[k]

for line in poset_str.split('\n'):
    u, v = [int(x) for x in line.split('|')]
    dget(u, fwd_adj).append(v)
    dget(v, rev_adj).append(u)
    # Make sure all pages are keys in both dicts.
    dget(u, rev_adj)
    dget(v, fwd_adj)

# Loop over the input lists, and identify valid and invalid sequences.
invalid_sequences = []
s = 0
for line in query_str.split('\n'):
    query = [int(x) for x in line.split(',')]
    # prereq contains all the pages that have to be printed before the pages we've already printed.
    prereq = set()
    for x in query:
        if x in prereq or prereq.intersection(fwd_adj.get(x, [])):
            # Either x had to be printed before an already printed page, or we've already printed some page that had to come after x.
            invalid_sequences.append(query)
            break
        prereq.add(x)
    else:
        s += query[len(query) // 2]

print(s)

s = 0
for query in invalid_sequences:
    q = set(query)
    order = []
    while q:
        # Identify pages whose must-be-printed-before pages are already printed.
        # They are safe to print => add to order.
        new = [x for x in q if not q.intersection(rev_adj[x])]
        order.extend(new)
        q.difference_update(new)
    s += order[len(query) // 2]

print(s)
