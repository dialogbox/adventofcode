import utils
import numpy as np


def solve_part1(data):
    increased = np.diff(data) > 0
    return len(data[1:][increased])


def part1(path):
    data = np.array(utils.read_number_lines(path))

    print(solve_part1(data))

def part2(path):
    data = np.array(utils.read_number_lines(path))

    wins = data[0:-2] + data[1:-1] + data[2:]

    print(solve_part1(wins))