import utils
from collections import deque
import numpy as np


def parse_input(path):
    return utils.readall(path)


def first_uniq_n_at(str, n):
    data = list(str)

    q = deque(data[:n])

    i = 0
    for c in data[n:]:
        if len(set(q)) == n:
            return i

        i += 1
        q.popleft()
        q.append(c)


def first_uniq_n_at_np(str, n):
    data = np.array(list(str)).view(np.uint32)
    nbyte_packet = np.reshape([np.roll(data, -i) for i in range(n)],
                              (n, len(data)))[:, :-(n - 1)]
    sorted_packet = np.sort(nbyte_packet, axis=0)
    uniq_char_count = np.count_nonzero(np.diff(sorted_packet, axis=0),
                                       axis=0) + 1
    idx = np.argmax(uniq_char_count == n)

    return idx


def part1(path):
    idx = first_uniq_n_at(parse_input(path), 4)
    print(idx + 4)


def part2(path):
    idx = first_uniq_n_at(parse_input(path), 14)
    print(idx + 14)


def part1np(path):
    idx = first_uniq_n_at_np(parse_input(path), 4)
    print(idx + 4)


def part2np(path):
    idx = first_uniq_n_at_np(parse_input(path), 14)
    print(idx + 14)
