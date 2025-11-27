from util import ints


fmt_dict = { "sep": None }

def get_out(A):
    partial = (A % 8) ^ 2
    return ((partial ^ (A >> partial)) ^ 7) % 8

def run(A):
    out = []
    while A > 0:
        out.append(get_out(A))
        A >>= 3
    return ",".join(map(str, out))

def solve(data):
    A, _, _, *program = ints(data)
    meta_inputs = { 0 }
    for num in reversed(program):
        new_meta_inputs = set()
        for curr_num in meta_inputs:
            for new_segment in range(8):
                new_num = (curr_num << 3) + new_segment
                if get_out(new_num) == num:
                    new_meta_inputs.add(new_num)
        meta_inputs = new_meta_inputs
    return run(A), min(meta_inputs)
