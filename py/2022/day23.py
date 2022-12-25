import utils
import numpy as np


def parse_input(path):
    grid = np.array(utils.read_grid(path)) == '#'

    return grid


def print_grid(grid):
    output_grid = np.reshape(np.array(['.'] * grid.shape[0] * grid.shape[1]),
                             grid.shape)

    output_grid[grid] = '#'
    utils.print_npgrid(output_grid, header="----------")


mat_stay = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) == 1
mat_up = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == 1
mat_down = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]]) == 1
mat_left = np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]]) == 1
mat_right = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]]) == 1


def count_adjacent(grid, filter):
    padded = np.pad(grid, [(1, 1), (1, 1)])

    return np.array([[
        np.count_nonzero(padded[y:y + 3, x:x + 3][filter])
        for x in range(padded.shape[1] - 2)
    ] for y in range(padded.shape[0] - 2)])


def simulate_round(grid, try_order):
    proposal = np.full(grid.shape, fill_value=".")

    n_all = count_adjacent(grid, mat_stay) == 0
    n_right = count_adjacent(grid, mat_right) == 0
    n_left = count_adjacent(grid, mat_left) == 0
    n_down = count_adjacent(grid, mat_down) == 0
    n_up = count_adjacent(grid, mat_up) == 0

    proposal[grid] = 'S'

    for dir in np.flip(try_order):
        if dir == 'R':
            proposal[np.logical_and(grid, n_right)] = 'R'
        elif dir == 'L':
            proposal[np.logical_and(grid, n_left)] = 'L'
        elif dir == 'D':
            proposal[np.logical_and(grid, n_down)] = 'D'
        elif dir == 'U':
            proposal[np.logical_and(grid, n_up)] = 'U'

    proposal[np.logical_and(grid, n_all)] = 'S'

    # utils.print_npgrid(proposal, header="======")

    stay = np.pad(proposal == 'S', [(1, 1), (1, 1)])
    up = np.pad(proposal == 'U', [(0, 2), (1, 1)])
    down = np.pad(proposal == 'D', [(2, 0), (1, 1)])
    left = np.pad(proposal == 'L', [(1, 1), (0, 2)])
    right = np.pad(proposal == 'R', [(1, 1), (2, 0)])

    num_proposed = (stay.astype(int) + up.astype(int) + down.astype(int) +
                    left.astype(int) + right.astype(int))
    conflict = num_proposed > 1
    no_conflict = num_proposed == 1

    conflict_while_up = np.roll(np.logical_and(up, conflict), 1, axis=0)
    conflict_while_down = np.roll(np.logical_and(down, conflict), -1, axis=0)
    conflict_while_left = np.roll(np.logical_and(left, conflict), 1, axis=1)
    conflict_while_right = np.roll(np.logical_and(right, conflict), -1, axis=1)

    result = (np.logical_or(
        stay,
        np.logical_or(
            no_conflict,
            np.logical_or(
                conflict_while_up,
                np.logical_or(
                    conflict_while_down,
                    np.logical_or(conflict_while_left,
                                  conflict_while_right))))))

    n_diff = np.count_nonzero(
        np.logical_xor(np.pad(grid, [(1, 1), (1, 1)]), result))
    return strip_grid(result), n_diff


def strip_grid(grid):
    ystart = 0
    yend = grid.shape[0] - 1
    xstart = 0
    xend = grid.shape[1] - 1
    for i in range(grid.shape[0]):
        if np.any(grid[i, :]):
            ystart = i
            break

    for i in range(grid.shape[0] - 1, -1, -1):
        if np.any(grid[i, :]):
            yend = i
            break

    for i in range(grid.shape[1]):
        if np.any(grid[:, i]):
            xstart = i
            break

    for i in range(grid.shape[1] - 1, -1, -1):
        if np.any(grid[:, i]):
            xend = i
            break

    return grid[ystart:yend + 1, xstart:xend + 1]


def part1(path):
    grid = parse_input(path)

    try_order = np.array(['U', 'D', 'L', 'R'])

    for i in range(10):
        grid, _ = simulate_round(grid, try_order)
        try_order = np.roll(try_order, -1)
    print_grid(grid)

    print(np.count_nonzero(grid != True))


def part2(path):
    grid = parse_input(path)

    try_order = np.array(['U', 'D', 'L', 'R'])

    round = 0

    while True:
        round += 1
        grid, n_moved = simulate_round(grid, try_order)
        try_order = np.roll(try_order, -1)
        if n_moved == 0:
            print(round)
            break