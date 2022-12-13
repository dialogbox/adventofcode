import utils
import functools


def parse_input(path):
    pair_strs = utils.readall(path).split("\n\n")

    lines = utils.read_lines(path)

    data = []
    ld = {"l": None, "r": None}
    for pstr in pair_strs:
        lines = pstr.split("\n")
        exec("l = " + lines[0], globals(), ld)
        exec("r = " + lines[1], globals(), ld)

        data.append((ld["l"].copy(), ld["r"].copy()))

    return data


def compare_two(a, b):
    if type(a) == int and type(b) == int:
        if a == b:
            return 0
        if a < b:
            return -1
        return 1

    if type(a) == int:
        return compare_two([a], b)

    if type(b) == int:
        return compare_two(a, [b])

    for (ia, ib) in zip(a, b):
        t = compare_two(ia, ib)
        if t == 0:
            continue
        return t

    if len(a) < len(b):
        return -1
    if len(a) > len(b):
        return 1
    return 0  # ??


def part1(path):
    data = parse_input(path)

    result = [compare_two(p[0], p[1]) for p in data]
    print(sum([i + 1 for (i, r) in enumerate(result) if r < 0]))


def part2(path):
    data = list(parse_input(path))

    div1 = [[2]]
    div2 = [[6]]

    all_packets = [div1, div2]

    for p in data:
        all_packets.append(p[0])
        all_packets.append(p[1])

    all_packets.sort(key=functools.cmp_to_key(compare_two))

    idx_div1 = 0
    idx_div2 = 0
    for i, v in enumerate(all_packets, start=1):
        if v == div1:
            idx_div1 = i
        if v == div2:
            idx_div2 = i

    print(idx_div1 * idx_div2)
