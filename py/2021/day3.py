import utils
import numpy as np


def read_input(path):
    return np.array([[int(b) for b in l]
                     for l in [list(l) for l in utils.read_lines(path)]])


def gamma(input):
    bin_str = np.char.mod(
        '%d', np.floor(np.sum(input, axis=0) / (input.shape[0] / 2)))
    return int("".join(bin_str), 2)


def epsilon(input):
    bin_str = np.char.mod(
        '%d', np.floor(np.sum(input, axis=0) / (input.shape[0] / 2)))
    return int("".join(['1' if b == '0' else '0' for b in bin_str]), 2)


def part1(path):
    input = read_input(path)
    g = gamma(input)
    e = epsilon(input)

    print(g * e)