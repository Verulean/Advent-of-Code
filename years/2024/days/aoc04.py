from util import to_array


xmas = {"XMAS", "SAMX"}

def solve(data):
    ans1 = 0
    ans2 = 0
    arr = to_array(data)
    m, n = arr.shape
    for i in range(m):
        for j in range(n):
            # check row
            if "".join(arr[i, j:j + 4]) in xmas:
                ans1 += 1
            # check column
            if "".join(arr[i:i + 4, j]) in xmas:
                ans1 += 1
            # check diagonal
            if i <= m - 4 and j <= n - 4:
                if "".join(arr[i + d, j + d] for d in range(4)) in xmas:
                    ans1 += 1
            # check other diag
            if i >= 3 and j <= n - 4:
                if "".join(arr[i - d, j + d] for d in range(4)) in xmas:
                    ans1 += 1
            # part 2
            if not (1 <= i <= m - 2 and 1 <= j <= n - 2):
                continue
            if arr[i, j] != "A":
                continue
            if { arr[i - 1, j - 1], arr[i + 1, j + 1] } == {"M", "S"} and { arr[i + 1, j - 1], arr[i - 1, j + 1] } == {"M", "S"}:
                ans2 += 1
    return ans1, ans2
