from util import RIGHT, DOWN, LEFT, UP, shoelace, tadd, tmul


DIRECTIONS = {
    "R": RIGHT, "0": RIGHT,
    "D": DOWN, "1": DOWN,
    "L": LEFT, "2": LEFT,
    "U": UP, "3": UP,
}

def polygonize(moves):
    pos = (0, 0)
    path_length = 0
    vertices = [pos]
    for k, dist in moves:
        d = DIRECTIONS[k]
        pos = tadd(pos, tmul(d, dist))
        path_length += dist
        vertices.append(pos)
    area = shoelace(vertices)
    return area + path_length // 2 + 1

def p1parse(line):
    d, l, *_ = line.split()
    return d, int(l)

def p2parse(line):
    hex = line.split()[-1].strip("(#)")
    return hex[-1], int(hex[:-1], 16)

def solve(data):
    p1 = polygonize(map(p1parse, data))
    p2 = polygonize(map(p2parse, data))
    return p1, p2
