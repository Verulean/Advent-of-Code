from collections import defaultdict, deque
import heapq


fmt_dict = { "sep": None }

def part1(files, blanks):
    ret = 0
    while blanks:
        i, id = files.pop()
        j = blanks.popleft()
        if j > i:
            ret += i * id
            break
        ret += j * id
    return ret + sum(i * id for i, id in files)

def find_space(blanks, length):
    min_index = None
    found_length = None
    for n in range(length, 10):
        li = blanks[n]
        if not li:
            continue
        i = li[0]
        if min_index is None or i < min_index:
            min_index = i
            found_length = n
    if min_index is None:
        return None
    heapq.heappop(blanks[found_length])
    if found_length > length:
        heapq.heappush(blanks[found_length - length], min_index + length)
    return min_index

def part2(files, blanks):
    for id in range(max(files), 0, -1):
        i, n = files[id]
        j = find_space(blanks, n)
        if j is None or j > i:
            continue
        files[id] = j, n
    return sum(id * (i * n + n * (n - 1) // 2) for id, (i, n) in files.items())

def solve(data):
    i = id = 0
    is_file = True
    files1 = deque()
    blanks1 = deque()
    files2 = {}
    blanks2 = defaultdict(list)
    for n in map(int, data):
        if is_file:
            for di in range(n):
                files1.append((i + di, id))
            files2[id] = i, n
            id += 1
        else:
            for di in range(n):
                blanks1.append(i + di)
            heapq.heappush(blanks2[n], i)
        i += n
        is_file = not is_file
    return part1(files1, blanks1), part2(files2, blanks2)
