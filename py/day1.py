import utils
import numpy as np


def part1(data):
    increased = np.diff(data) > 0
    return len(data[1:][increased])


def part2(data):
    wins = data[0:-2] + data[1:-1] + data[2:]
    return part1(wins)


if __name__ == '__main__':
    data = np.array(utils.read_number_lines("inputs/day1.txt"))

    print(part1(data))
    print(part2(data))
