import utils

def parse_input(path):
    return utils.read_lines(path)

def priority(a):
    if a.isupper():
        return ord(a) - ord('A') + 27
    else:
        return ord(a) - ord('a') + 1

def group_elfs(elfs, group_size):
    for i in range(0, len(elfs), group_size):
        yield elfs[i: i + group_size]

def part1(path):
    data = parse_input(path)

    sacks = [(set(l[:int(len(l)/2)]), set(l[int(len(l)/2):])) for l in data]

    errors = [(a & b) for (a, b) in sacks]

    print(sum([priority(list(e)[0]) for e in errors]))

def part2(path):
    data = parse_input(path)

    elf_groups = [[set(e) for e in g] for g in group_elfs(data, 3)]

    badges = [g[0] & g[1] & g[2] for g in elf_groups]

    print(sum([priority(list(b)[0]) for b in badges]))