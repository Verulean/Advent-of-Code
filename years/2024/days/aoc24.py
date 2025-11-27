fmt_dict = { "sep": "\n\n" }


def evaluate_wires(variables, wires):
    q = list(wires.items())
    while q:
        new_q = []
        for elem in q:
            c, (op, a, b) = elem
            va = variables.get(a, None)
            vb = variables.get(b, None)
            if va is None or vb is None:
                new_q.append(elem)
                continue
            match op:
                case "XOR":
                    variables[c] = va ^ vb
                case "AND":
                    variables[c] = va and vb
                case "OR":
                    variables[c] = va or vb
        q = new_q

def parse_wires(wires):
    xy_xors = {}
    xy_ands = {}
    xor_wires = {}
    and_wires = {}
    or_argwires = {}
    for c, (op, a, b) in wires.items():
        match op:
            case "XOR":
                xor_wires[a] = c
                xor_wires[b] = c
                if a.startswith("x"):
                    xy_xors[int(a[1:])] = c
            case "AND":
                and_wires[a] = c
                and_wires[b] = c
                if a.startswith("x"):
                    xy_ands[int(a[1:])] = c
            case "OR":
                or_argwires[a] = b, c
                or_argwires[b] = a, c
    return xy_xors, xy_ands, xor_wires, and_wires, or_argwires

def find_swaps(variables, wires):
    input_length = sum(1 for v in variables if v.startswith("x"))
    xy_xors, xy_ands, xor_wires, and_wires, or_argwires = parse_wires(wires)
    swaps = set()
    for i in range(1, input_length):
        suffix = f"{i:02d}"
        z = f"z{suffix}"
        zop, za, zb = wires[z]
        x_xor_y = xy_xors[i]
        x_and_y = xy_ands[i]
        if x_xor_y == z:
            # m and z
            swaps.add(z)
            r = or_argwires[x_and_y][0]
            _, _, m = wires[r]
            swaps.add(xor_wires[m])
        elif x_and_y == z:
            # n and z
            swaps.add(z)
            swaps.add(xor_wires[x_xor_y])
        elif zop == "AND":
            # r and z
            swaps.add(z)
            swaps.add(xor_wires[za])
        elif zop == "OR":
            # d and z
            swaps.add(z)
            swaps.add(xor_wires[x_xor_y])
        else:
            c_and_m = and_wires[za]
            if c_and_m not in or_argwires:
                swaps.add(c_and_m)
                if c_and_m in {za, zb}:
                    # m and r
                    swaps.add(x_xor_y)
                else:
                    # d and r
                    swaps.add(or_argwires[x_and_y][1])
            else:
                n, c = or_argwires[c_and_m]
                if c == n:
                    # d and n
                    swaps.add(x_and_y)
                    swaps.add(n)
                elif x_xor_y == n:
                    # m and n
                    swaps.add(x_and_y)
                    swaps.add(x_xor_y)
    return swaps

def solve(data):
    values, gates = data
    variables = {}
    for line in values.split("\n"):
        v, b = line.split(": ")
        variables[v] = b == "1"
    wires = {}
    for line in gates.split("\n"):
        a, op, b, _, c = line.split()
        wires[c] = (op, *sorted([a, b]))
    evaluate_wires(variables, wires)
    z_vars = sorted((v for v in variables if v.startswith("z")), reverse=True)
    ans1 = int("".join(("0", "1")[variables[v]] for v in z_vars), 2)
    swaps = find_swaps(variables, wires)
    return ans1, ",".join(sorted(swaps))
