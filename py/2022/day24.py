import utils
import numpy as np
from collections import deque
import time as timemod


def parse_input(path):
    src = np.array(utils.read_grid(path))

    grid = src[1:-1, 1:-1]

    grid_up = grid == '^'
    grid_down = grid == 'v'
    grid_left = grid == '<'
    grid_right = grid == '>'

    return (grid_up, grid_down, grid_left, grid_right)


def n_steps(grid, n):
    h, w = grid[0].shape
    nh = n % h
    nw = n % w

    up = grid[0]
    down = grid[1]
    left = grid[2]
    right = grid[3]
    if nh > 0:
        up = np.concatenate((up[nh:, :], np.reshape(up[0:nh, :], (nh, w))),
                            axis=0)
        down = np.concatenate((np.reshape(down[-nh:, :],
                                          (-nh, w)), down[:-nh, :]),
                              axis=0)
    if nw > 0:
        left = np.concatenate((left[:, nw:], np.reshape(left[:, :nw],
                                                        (h, nw))),
                              axis=1)
        right = np.concatenate((np.reshape(right[:, -nw:],
                                           (h, nw)), right[:, :-nw]),
                               axis=1)

    return (up, down, left, right)


def print_grid(grid):
    h, w = grid[0].shape

    print("#." + "#" * w)

    for y in range(grid[0].shape[0]):
        print("#", end="")
        for x in range(grid[0].shape[1]):
            t = np.array(
                [grid[0][y, x], grid[1][y, x], grid[2][y, x], grid[3][y, x]])
            n = np.count_nonzero(t)

            if n == 0:
                print(".", end="")
            elif n > 1:
                print(n, end="")
            elif t[0]:
                print("^", end="")
            elif t[1]:
                print("v", end="")
            elif t[2]:
                print("<", end="")
            elif t[3]:
                print(">", end="")
        print("#")

    print("#" * w + ".#")


def create_grid_cache(grid):
    h, w = grid[0].shape

    t = [n_steps(grid, i) for i in range(h * w)]

    return [u | d | l | r for (u, d, l, r) in t]


def shortest_path(grid):
    h, w = grid[0].shape

    grid_cache = create_grid_cache(grid)

    search_queue = deque([((-1, 0, 0), [(-1, 0, 0)])])
    visited = set([(-1, 0, 0)])

    while len(search_queue) > 0:
        ((y, x, grid_idx), path) = search_queue.popleft()

        next_grid_idx = (grid_idx + 1) % (h * w)
        next_grid = grid_cache[next_grid_idx]

        # arrived
        if (y, x) == (h - 1, w - 1):
            return path + [(y + 1, x, next_grid_idx)]

        # if it's safe to stay at the current position
        if not next_grid[y, x] and (y, x, next_grid_idx) not in visited:
            search_queue.append(
                ((y, x, next_grid_idx), path + [(y, x, next_grid_idx)]))
            visited.add((y, x, next_grid_idx))

        if (y, x) == (-1, 0):
            if not next_grid[0, 0] and (0, 0, next_grid_idx) not in visited:
                search_queue.append(
                    ((0, 0, next_grid_idx), path + [(0, 0, next_grid_idx)]))
                visited.add((0, 0, next_grid_idx))
            elif (-1, 0, next_grid_idx) not in visited:
                search_queue.append(
                    ((-1, 0, next_grid_idx), path + [(-1, 0, next_grid_idx)]))
                visited.add((-1, 0, next_grid_idx))
        else:
            if y > 0:
                if not next_grid[y - 1, x] and (y - 1, x,
                                                next_grid_idx) not in visited:
                    search_queue.append(((y - 1, x, next_grid_idx),
                                         path + [(y - 1, x, next_grid_idx)]))
                    visited.add((y - 1, x, next_grid_idx))
            if y < h - 1 and (y + 1, x, next_grid_idx) not in visited:
                if not next_grid[y + 1, x]:
                    search_queue.append(((y + 1, x, next_grid_idx),
                                         path + [(y + 1, x, next_grid_idx)]))
                    visited.add((y + 1, x, next_grid_idx))
            if x > 0 and (y, x - 1, next_grid_idx) not in visited:
                if not next_grid[y, x - 1]:
                    search_queue.append(((y, x - 1, next_grid_idx),
                                         path + [(y, x - 1, next_grid_idx)]))
                    visited.add((y, x - 1, next_grid_idx))
            if x < w - 1 and (y, x + 1, next_grid_idx) not in visited:
                if not next_grid[y, x + 1]:
                    search_queue.append(((y, x + 1, next_grid_idx),
                                         path + [(y, x + 1, next_grid_idx)]))
                    visited.add((y, x + 1, next_grid_idx))

    print("wtf")


def part1(path):
    grid = parse_input(path)

    path = shortest_path(grid)

    print(len(path))
    print(path)

    # for i in range(100):
    #     print_grid(n_steps(grid, i))
    #     timemod.sleep(1)