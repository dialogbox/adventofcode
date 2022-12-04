import utils


def parse_input(path):
    lines = utils.read_number_pair_csv(path, '-')

    return lines

def is_fully_contained(a, b):
    if a[0] <= b[0] and a[1] >= b[1]:
        return 2
    if a[0] >= b[0] and a[1] <= b[1]:
        return 1
    
    return 0

def is_overlap(a, b):
    if a[0] > b[1] or a[1] < b[0]:
        return False

    return True

def part1(path):
    data = list(parse_input(path))

    print(len([True for l in data if is_fully_contained(l[0], l[1])]))


def part2(path):
    data = parse_input(path)

    print(len([True for l in data if is_overlap(l[0], l[1])]))