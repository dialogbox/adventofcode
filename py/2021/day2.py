import utils


def read_input(path):
    return [(l[0], int(l[1]))
            for l in [l.split() for l in utils.read_lines(path)]]


def part1(path):
    input = read_input(path)

    h = 0
    v = 0

    for m in input:
        if m[0] == "forward":
            h += m[1]
        elif m[0] == "up":
            v -= m[1]
        else:
            v += m[1]

    print(h * v)


def part2(path):
    input = read_input(path)

    h = 0
    v = 0
    aim = 0

    for m in input:
        if m[0] == "forward":
            h += m[1]
            v += aim * m[1]
        elif m[0] == "up":
            aim -= m[1]
        else:
            aim += m[1]

    print(h * v)