import utils
import numpy as np


def parse_input(path):
    lines = utils.read_lines(path)

    paths = [[utils.parse_coord_str(p) for p in l.split(" -> ")]
             for l in lines]

    height = 0
    width = 0

    for path in paths:
        for p in path:
            width = max(width, p[0])
            height = max(height, p[1])

    # 0: Air
    # 1: Rock
    # 2: Sand
    grid = np.zeros((height + 1, width + 1))

    for path in paths:
        for [f, t] in zip(path[:-1], path[1:]):
            fx = min(f[0], t[0])
            tx = max(f[0], t[0])
            fy = min(f[1], t[1])
            ty = max(f[1], t[1])
            grid[fy:ty + 1, fx:tx + 1] = 1

    return grid


def drop_a_sand(grid, sx, sy):
    (height, width) = grid.shape
    x, y = sx, sy

    if grid[sy, sx] != 0:
        return False

    while True:
        if y == height - 1:
            # drop
            return False

        if (grid[y + 1, x] != 0 and grid[y + 1, x - 1] != 0
                and grid[y + 1, x + 1] != 0):
            # come to rest
            grid[y, x] = 2
            return True

        if grid[y + 1, x] == 0:
            y += 1
        elif grid[y + 1, x - 1] == 0:
            y += 1
            x -= 1
        elif grid[y + 1, x + 1] == 0:
            y += 1
            x += 1


def hpad(grid, n):
    height = grid.shape[0]

    return np.concatenate([np.zeros(
        (height, n)), grid, np.zeros((height, n))],
                          axis=1)


def part1(path):
    grid = parse_input(path)
    width = grid.shape[1]

    grid = np.concatenate([grid, np.zeros((1, width))], axis=0)
    grid = hpad(grid, 1)

    n = 0
    while drop_a_sand(grid, 500 + 1, 0):
        n += 1

    print(n)


def part2(path):
    grid = parse_input(path)
    width = grid.shape[1]

    padding_size = 500

    grid = np.concatenate([grid, np.zeros((2, width))], axis=0)
    grid = hpad(grid, padding_size)
    grid[-1, :] = 1

    n = 0
    while drop_a_sand(grid, 500 + padding_size, 0):
        n += 1

    print(n)