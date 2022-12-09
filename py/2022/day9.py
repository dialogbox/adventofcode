import utils


def parse_input(path):
    lines = utils.read_lines(path)

    return [(d, int(n)) for [d, n] in [l.split(" ") for l in lines]]


STEP = {
    "U": (0, 1),
    "D": (0, -1),
    "R": (1, 0),
    "L": (-1, 0),
}


def move_head(rope, direction, n):
    tail_visited = set([rope[-1]])
    (step_x, step_y) = STEP[direction]
    for i in range(n):
        rope[0] = (rope[0][0] + step_x, rope[0][1] + step_y)
        fix_knots(rope)
        tail_visited.add(rope[-1])

    return (rope, tail_visited)


def fix_one_knot(h, t):
    (hx, hy) = h
    (tx, ty) = t

    x_dist = abs(hx - tx)
    x_dir = (hx - tx) / x_dist if x_dist > 0 else 0
    y_dist = abs(hy - ty)
    y_dir = (hy - ty) / y_dist if y_dist > 0 else 0

    if x_dist <= 1 and y_dist <= 1:
        return t

    return (tx + x_dir, ty + y_dir)


def fix_knots(rope):
    for i in range(len(rope) - 1):
        rope[i + 1] = fix_one_knot(rope[i], rope[i + 1])


def simulate(rope, moves):
    tail_visited = set([rope[-1]])
    for m in moves:
        (rope, new_tail_visited) = move_head(rope, m[0], m[1])
        tail_visited = tail_visited.union(new_tail_visited)

    return (rope, tail_visited)


def part1(path):
    data = list(parse_input(path))
    (_, tail_visited) = simulate([(0, 0)] * 2, data)
    print(len(tail_visited))


def part2(path):
    data = list(parse_input(path))
    (_, tail_visited) = simulate([(0, 0)] * 10, data)
    print(len(tail_visited))