import utils


def parse_input(path):
    lines = utils.read_lines(path)

    return [(d, int(n)) for [d, n] in [l.split(" ") for l in lines]]


def move_one_knot(h, t):
    (hx, hy) = h
    (tx, ty) = t

    x_dist = abs(hx - tx)
    x_dir = (hx - tx) / x_dist if x_dist > 0 else 0
    y_dist = abs(hy - ty)
    y_dir = (hy - ty) / y_dist if y_dist > 0 else 0

    if x_dist <= 1 and y_dist <= 1:
        return t

    return (tx + x_dir, ty + y_dir)


def fix_rope(rope):
    for i in range(len(rope) - 1):
        rope[i + 1] = move_one_knot(rope[i], rope[i + 1])


def move_up(rope, n):
    tail_visited = set([rope[-1]])
    for i in range(n):
        rope[0] = (rope[0][0], rope[0][1] + 1)
        fix_rope(rope)
        tail_visited.add(rope[-1])

    return (rope, tail_visited)


def move_down(rope, n):
    tail_visited = set([rope[-1]])
    for i in range(n):
        rope[0] = (rope[0][0], rope[0][1] - 1)
        fix_rope(rope)
        tail_visited.add(rope[-1])

    return (rope, tail_visited)


def move_right(rope, n):
    tail_visited = set([rope[-1]])
    for i in range(n):
        rope[0] = (rope[0][0] + 1, rope[0][1])
        fix_rope(rope)
        tail_visited.add(rope[-1])

    return (rope, tail_visited)


def move_left(rope, n):
    tail_visited = set([rope[-1]])
    for i in range(n):
        rope[0] = (rope[0][0] - 1, rope[0][1])
        fix_rope(rope)
        tail_visited.add(rope[-1])

    return (rope, tail_visited)


def simulate(rope, moves):
    tail_visited = set([rope[-1]])
    for m in moves:
        if m[0] == "U":
            (rope, new_tail_visited) = move_up(rope, m[1])
            tail_visited = tail_visited.union(new_tail_visited)
        elif m[0] == "D":
            (rope, new_tail_visited) = move_down(rope, m[1])
            tail_visited = tail_visited.union(new_tail_visited)
        elif m[0] == "R":
            (rope, new_tail_visited) = move_right(rope, m[1])
            tail_visited = tail_visited.union(new_tail_visited)
        elif m[0] == "L":
            (rope, new_tail_visited) = move_left(rope, m[1])
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