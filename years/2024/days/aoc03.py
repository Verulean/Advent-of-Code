import re


fmt_dict = { "sep": None }

def solve(data):
    ans1 = ans2 = 0
    pattern = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"
    mul_enabled = True
    for a, b, do, dont in re.findall(pattern, data):
        if do:
            mul_enabled = True
        elif dont:
            mul_enabled = False
        else:
            product = int(a) * int(b)
            ans1 += product
            if mul_enabled:
                ans2 += product
    return ans1, ans2
