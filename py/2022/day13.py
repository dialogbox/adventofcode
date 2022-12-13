import utils
import functools
import itertools


def parse_input(path):
    lines = utils.readall(path).split("\n")
    pairs = [
        list(y) for x, y in itertools.groupby(lines, lambda z: z == "")
        if not x
    ]
    data = [(eval(p1), eval(p2)) for [p1, p2] in pairs]

    return data


def compare_ints(a, b):
    if a < b:
        return -1
    if a == b:
        return 0
    return 1


def compare_two(a, b):
    if type(a) == int and type(b) == int:
        return compare_ints(a, b)

    if type(a) == int:
        return compare_two([a], b)

    if type(b) == int:
        return compare_two(a, [b])

    for (ia, ib) in zip(a, b):
        t = compare_two(ia, ib)
        if t == 0:
            continue
        return t

    return compare_ints(len(a), len(b))


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
        all_packets.extend(p)

    all_packets.sort(key=functools.cmp_to_key(compare_two))

    idx_div1 = all_packets.index(div1) + 1
    idx_div2 = all_packets.index(div2) + 1

    print(idx_div1 * idx_div2)
