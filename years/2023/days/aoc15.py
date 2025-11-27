from collections import defaultdict
from util import smap


fmt_dict = { "sep": "," }

def hash_alg(s):
    r=0
    for c in s:
        r += ord(c)
        r *= 17
        r %= 256
    return r

def solve(data):
    p1 = smap(hash_alg, data)
    m = defaultdict(dict)
    for l in data:
        if l[-1] == "-":
            label = l[:-1]
            box = hash_alg(label)
            if label in m[box]:
                del m[box][label]
        else:
            label, focal_length = l.split("=")
            box = hash_alg(label)
            focal_length = int(focal_length)
            m[box][label] = focal_length
    p2 = 0
    for box, lenses in m.items():
        for i, (label, length) in enumerate(lenses.items()):
            p2 += (box + 1) * (i + 1) * length
    return p1, p2
