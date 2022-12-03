import utils


def parse_input(path):
    lines = utils.read_lines(path)

    f = 0
    for i in range(len(lines)):
        if lines[i] == "":
            g = [int(l) for l in lines[f:i]]
            yield (sum(g), g)
            f = i + 1


def part1(path):
    data = list(parse_input(path))

    data = sorted(data, key=lambda a: -a[0])

    print(data[0][0])


def part2(path):
    data = parse_input(path)

    data = sorted(data, key=lambda a: -a[0])

    print(data[0][0] + data[1][0] + data[2][0])