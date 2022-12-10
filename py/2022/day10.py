import utils


def clock_generator(path):
    lines = utils.read_lines(path)

    for inst in [l.split(" ") for l in lines]:
        if inst[0] == 'noop':
            yield 0
        elif inst[0] == 'addx':
            yield 0
            yield int(inst[1])


def part1(path):
    clocks = list(clock_generator(path))

    x = 1
    signal_strength = 0
    for clock, op in enumerate(clocks, start=1):
        if (clock - 20) % 40 == 0:
            signal_strength += clock * x
        x += op

    print(signal_strength)


def part2(path):
    clocks = list(clock_generator(path))

    crt = [[' '] * 40 for i in range(6)]

    x = 1
    for clock, op in enumerate(clocks):
        v = clock // 40
        h = clock % 40
        if h >= x - 1 and h <= x + 1:
            crt[v][h] = '#'
        x += op

    for l in crt:
        print("".join(l))
