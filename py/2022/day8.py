import utils
import numpy as np
import bisect


def parse_input(path):
    grid = utils.read_number_grid(path)

    return grid


def visible_trees(grid):
    (h, w) = grid.shape

    visible = np.full(grid.shape, False)

    curmax = np.full(h, -1)
    for i in range(w):
        newvisible = curmax < grid[:, i]
        curmax[newvisible] = grid[:, i][newvisible]
        visible[:, i] = visible[:, i] | newvisible

    curmax = np.full(h, -1)
    for i in range(w - 1, -1, -1):
        newvisible = curmax < grid[:, i]
        curmax[newvisible] = grid[:, i][newvisible]
        visible[:, i] = visible[:, i] | newvisible

    curmax = np.full(w, -1)
    for i in range(h):
        newvisible = curmax < grid[i, :]
        curmax[newvisible] = grid[i, :][newvisible]
        visible[i, :] = visible[i, :] | newvisible

    curmax = np.full(w, -1)
    for i in range(h - 1, -1, -1):
        newvisible = curmax < grid[i, :]
        curmax[newvisible] = grid[i, :][newvisible]
        visible[i, :] = visible[i, :] | newvisible

    return visible


def score_onedirection(view, cur):
    view = list(view)
    score = 0
    for i in view:
        score += 1
        if i >= cur:
            break

    return score


def scenic_score(grid):
    score = np.zeros(grid.shape)
    (h, w) = grid.shape

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            cur = grid[i, j]
            left_score = score_onedirection(reversed(grid[i, 0:j]), cur)
            right_score = score_onedirection(grid[i, j + 1:], cur)
            up_score = score_onedirection(reversed(grid[0:i, j]), cur)
            down_score = score_onedirection(grid[i + 1:, j], cur)

            score[i, j] = int(left_score * right_score * up_score * down_score)

    return score


def part1(path):
    grid = parse_input(path)
    visible = visible_trees(np.array(grid))

    print(np.count_nonzero(visible))


def part2(path):
    grid = parse_input(path)
    score = scenic_score(np.array(grid))

    print(int(np.amax(score)))