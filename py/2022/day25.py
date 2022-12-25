import utils
import math


def parse_input(path):
    return utils.read_lines(path)


snafu_digits = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

snafu_digits_reverse = {
    0: "0",
    1: "1",
    2: "2",
    3: "=",
    4: "-",
}


def snafu_to_dec(snafu):
    ndigits = len(snafu)

    digits = [snafu_digits[c] for c in snafu]

    return int(
        sum([math.pow(5, ndigits - i - 1) * d for i, d in enumerate(digits)]))


def dec_to_snafu(dec):
    left = dec
    result = []

    if dec == 0:
        return '0'

    while left > 0:
        cur_digit = left % 5
        if cur_digit >= 3:
            left += 5
        left = left // 5
        result.append(snafu_digits_reverse[cur_digit])

    result.reverse()

    return "".join(result)


def part1(path):
    lines = parse_input(path)

    result = sum([snafu_to_dec(snafu) for snafu in lines])
    print(result, dec_to_snafu(result))
