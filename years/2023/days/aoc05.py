from util import Range, chunks, ints


fmt_dict = { "sep": "\n\n" }

def get_best_location(almanac, start_range):
    r = start_range
    for range_transforms in almanac:
        transformed = Range()
        for source_range, offset in range_transforms:
            transformed |= (r & source_range) + offset
            r -= source_range
        r |= transformed
    return r.min

def solve(data):
    almanac = []
    seeds = ints(data[0])
    for block in data[1:]:
        range_transforms = []
        for dest_start, source_start, length in map(ints, block.split("\n")[1:]):
            range_transforms.append(((source_start, source_start + length), dest_start - source_start))
        almanac.append(range_transforms)
    ans1 = get_best_location(almanac, Range((s, s + 1) for s in seeds))
    ans2 = get_best_location(almanac, Range((s, s + l) for s, l in chunks(seeds, 2)))
    return ans1, ans2
