import utils
import numpy as np
from collections import deque


def parse_input(path):
    grid = np.array(utils.read_grid(path))

    grid_up = grid == '^'
    grid_down = grid == 'v'
    grid_left = grid == '<'
    grid_right = grid == '>'
    grid_wall = grid == '#'

    return (grid_up, grid_down, grid_left, grid_right, grid_wall)


def print_grid(grid):
    h, w = grid[0].shape

    for y in range(h):
        for x in range(w):
            t = np.array([
                grid[0][y, x], grid[1][y, x], grid[2][y, x], grid[3][y, x],
                grid[4][y, x]
            ])
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
            elif t[4]:
                print("#", end="")

        print("")


def n_steps(grid, n):
    h, w = grid[0].shape

    nh = n % (h - 2)
    nw = n % (w - 2)

    up = np.pad(np.roll(grid[0][1:-1, 1:-1], -nh, axis=0), [(1, 1), (1, 1)])
    down = np.pad(np.roll(grid[1][1:-1, 1:-1], nh, axis=0), [(1, 1), (1, 1)])
    left = np.pad(np.roll(grid[2][1:-1, 1:-1], -nw, axis=1), [(1, 1), (1, 1)])
    right = np.pad(np.roll(grid[3][1:-1, 1:-1], nw, axis=1), [(1, 1), (1, 1)])

    return (up, down, left, right, grid[4])


def create_grid_cache(grid):
    h, w = grid[0].shape

    t = [n_steps(grid, i) for i in range((h - 2) * (w - 2))]

    return [u | d | l | r | wall for (u, d, l, r, wall) in t]


def shortest_path(grid, start_time, starty, startx, endy, endx):
    h, w = grid[0].shape

    start_grid_idx = start_time % ((h - 2) * (w - 2))

    grid_cache = create_grid_cache(grid)

    search_queue = deque([((starty, startx, start_grid_idx),
                           [(starty, startx, start_grid_idx)])])
    visited = set([(starty, startx, start_grid_idx)])

    while len(search_queue) > 0:
        ((y, x, grid_idx), path) = search_queue.popleft()

        next_grid_idx = (grid_idx + 1) % ((h - 2) * (w - 2))
        next_grid = grid_cache[next_grid_idx]

        # arrived
        if (y, x) == (endy, endx):
            return path[1:]

        # if it's safe to stay at the current position
        if not next_grid[y, x] and (y, x, next_grid_idx) not in visited:
            search_queue.append(
                ((y, x, next_grid_idx), path + [(y, x, next_grid_idx)]))
            visited.add((y, x, next_grid_idx))

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

    h, w = grid[0].shape

    path = shortest_path(grid, 0, 0, 1, h - 1, w - 2)

    print(len(path))


def part2(path):
    grid = parse_input(path)

    h, w = grid[0].shape

    path = shortest_path(grid, 0, 0, 1, h - 1, w - 2)
    ela_to_goal = len(path)

    path2 = shortest_path(grid, ela_to_goal, h - 1, w - 2, 0, 1)
    ela_to_return_back = len(path2)

    path3 = shortest_path(grid, ela_to_goal + ela_to_return_back, 0, 1, h - 1,
                          w - 2)
    ela_to_goal_again = len(path3)

    print(ela_to_goal + ela_to_return_back + ela_to_goal_again)