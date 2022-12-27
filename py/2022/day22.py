import utils
import numpy as np
import re


def parse_input(path):
    lines = utils.readall(path).split('\n')

    w = max([len(l) for l in lines[:-2]])
    grid = np.array([list(l.ljust(w, ' ')) for l in lines[:-2]])

    inst = re.split("([LR])", lines[-1])

    inst = tuple([int(e) if e != 'R' and e != 'L' else e for e in inst])

    grid = np.pad(grid, [(1, 1), (1, 1)], constant_values=' ')

    return (grid, inst)


def start_position(grid):
    n = np.argmax(grid != ' ')
    x = n % grid.shape[1]
    y = n // grid.shape[1]
    return (y, x)


DIR_RIGHT = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_UP = 3


def get_next_position(grid, y, x, dir, dist):
    if dir in (DIR_RIGHT, DIR_LEFT):
        line = grid[y, :]
    else:
        line = grid[:, x]

    start = np.argmax(line != ' ')
    end = start + np.argmax(line[start:] == ' ') - 1

    real_line = line[start:end + 1]
    if dir in (DIR_RIGHT, DIR_LEFT):
        real_start = x - start
    else:
        real_start = y - start

    # flip to handle the non natural directions
    if dir in (DIR_LEFT, DIR_UP):
        real_line = np.flip(real_line)
        real_start = len(real_line) - real_start - 1

    if len(real_line[real_start + 1:]) < dist:
        # to handle wraparound
        temp = np.concatenate([real_line, real_line
                               ])[real_start + 1:real_start + dist + 1]
    else:
        temp = real_line[real_start + 1:real_start + dist + 1]

    if np.any(temp == '#'):
        possible_dist = min(dist, np.argmax(temp == '#'))
    else:
        # np.argmax returns 0 if there is no true
        possible_dist = dist

    if len(real_line[real_start + 1:]) >= possible_dist:
        arrived_at = real_start + possible_dist
    else:
        arrived_at = real_start + possible_dist - len(real_line)

    # flip again
    if dir in (DIR_LEFT, DIR_UP):
        arrived_at = len(real_line) - arrived_at - 1

    if dir in (DIR_RIGHT, DIR_LEFT):
        return y, start + arrived_at
    else:
        return start + arrived_at, x


def navigate(grid, startpos, instructions):
    cury, curx = startpos
    direction = DIR_RIGHT

    for inst in instructions:
        if type(inst) == int:
            cury, curx = get_next_position(grid, cury, curx, direction, inst)
        elif inst == 'L':
            if direction > 0:
                direction -= 1
            else:
                direction = 3
        else:
            if direction < 3:
                direction += 1
            else:
                direction = 0

    return cury, curx, direction


def part1(path):
    grid, instructions = parse_input(path)

    startpos = start_position(grid)
    y, x, dir = navigate(grid, startpos, instructions)

    print(1000 * y + 4 * x + dir)


def part2(path):
    grid, instructions = parse_input(path)