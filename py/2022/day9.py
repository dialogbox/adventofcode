import utils


def parse_input(path):
    lines = utils.read_lines(path)

    return [(d, int(n)) for [d, n] in [l.split(" ") for l in lines]]


def move_up(h, t, n):
    curh = h
    curt = t

    tail_visited = set([t])
    for i in range(n):
        (hx, hy) = curh
        (tx, ty) = curt
        curh = (hx, hy + 1)
        if hx != tx:
            if hy > ty:
                curt = (hx, ty + 1)
        else:
            if hy > ty:
                curt = (tx, ty + 1)
        tail_visited.add(curt)

    return (curh, curt, tail_visited)


def move_down(h, t, n):
    curh = h
    curt = t

    tail_visited = set([t])
    for i in range(n):
        (hx, hy) = curh
        (tx, ty) = curt
        curh = (hx, hy - 1)
        if hx != tx:
            if hy < ty:
                curt = (hx, ty - 1)
        else:
            if hy < ty:
                curt = (tx, ty - 1)
        tail_visited.add(curt)

    return (curh, curt, tail_visited)


def move_right(h, t, n):
    curh = h
    curt = t

    tail_visited = set([t])
    for i in range(n):
        (hx, hy) = curh
        (tx, ty) = curt
        curh = (hx + 1, hy)
        if hy != ty:
            if hx > tx:
                curt = (tx + 1, hy)
        else:
            if hx > tx:
                curt = (tx + 1, ty)
        tail_visited.add(curt)

    return (curh, curt, tail_visited)


def move_left(h, t, n):
    curh = h
    curt = t

    tail_visited = set([t])
    for i in range(n):
        (hx, hy) = curh
        (tx, ty) = curt
        curh = (hx - 1, hy)
        if hy != ty:
            if hx < tx:
                curt = (tx - 1, hy)
        else:
            if hx < tx:
                curt = (tx - 1, ty)
        tail_visited.add(curt)

    return (curh, curt, tail_visited)


def part1(path):
    data = list(parse_input(path))

    curh = (0, 0)
    curt = (0, 0)

    tail_visited = set()
    tail_visited.add((0, 0))
    for m in data:
        if m[0] == "U":
            (curh, curt, new_tail_visited) = move_up(curh, curt, m[1])
            tail_visited = tail_visited.union(new_tail_visited)
        elif m[0] == "D":
            (curh, curt, new_tail_visited) = move_down(curh, curt, m[1])
            tail_visited = tail_visited.union(new_tail_visited)
        elif m[0] == "R":
            (curh, curt, new_tail_visited) = move_right(curh, curt, m[1])
            tail_visited = tail_visited.union(new_tail_visited)
        elif m[0] == "L":
            (curh, curt, new_tail_visited) = move_left(curh, curt, m[1])
            tail_visited = tail_visited.union(new_tail_visited)

    print(len(tail_visited))


def part2(path):
    data = parse_input(path)

    data = sorted(data, key=lambda a: -a[0])

    print(data[0][0] + data[1][0] + data[2][0])