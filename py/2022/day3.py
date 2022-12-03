import utils

def parse_input(path):
    return utils.read_lines(path)

def find_common_char(a, b):
    return list(set(a).intersection(set(b)))

def priority(a):
    if a >= 'A' and a <= 'Z':
        return ord(a) - ord('A') + 27
    else:
        return ord(a) - ord('a') + 1

def group_elfs(elfs, group_size):
    for i in range(0, len(elfs), group_size):
        yield elfs[i: i + group_size]

def part1(path):
    data = parse_input(path)

    sacks = [(l[0:int(len(l)/2)], l[int(len(l)/2):len(l)]) for l in data]

    errors = [find_common_char(a, b)[0] for (a, b) in sacks]

    print(sum([priority(e) for e in errors]))

def part2(path):
    data = parse_input(path)

    elf_groups = [list(g) for g in group_elfs(data, 3)]

    badges = [set(g[0]).intersection(set(g[1]), set(g[2])) for g in elf_groups]

    print(sum([priority(list(b)[0]) for b in badges]))