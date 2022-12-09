import utils


def parse_input(path):
    lines = utils.read_lines(path)

    return [(d, int(n)) for [d, n] in [l.split(" ") for l in lines]]


def move_tail(h, t):
    (hx, hy) = h
    (tx, ty) = t

    if hx == tx:
        if hy > ty:
            return (tx, hy - 1)
        elif hy < ty:
            return (tx, hy + 1)
        else:
            return t
    elif hy == ty:
        if hx > tx:
            return (hx - 1, ty)
        elif hx < tx:
            return (hx + 1, ty)
        else:
            return t

    if abs(hx - tx) == 1 and abs(hy - ty) == 1:
        return t

    if hx > tx:
        tx += 1
    else:
        tx -= 1

    if hy > ty:
        ty += 1
    else:
        ty -= 1

    return (tx, ty)


def fix_rope(rope):
    for i in range(len(rope) - 1):
        rope[i + 1] = move_tail(rope[i], rope[i + 1])


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