def read_lines(filename):
    f = open(filename, "r")
    lines = [line.strip() for line in f]

    return lines


def read_csv(filename):
    lines = read_lines(filename)
    return [line.strip().split(",") for line in lines]


def read_numbers_csv(filename):
    lines = read_csv(filename)

    return [[int(i) for i in l] for l in lines]


def read_number_pair_csv(filename, pair_sep):
    lines = read_csv(filename)

    return [[parse_number_pair(c, pair_sep) for c in r] for r in lines]


def parse_number_pair(str, sep):
    p = str.split(sep)

    return (int(p[0]), int(p[1]))


def read_number_lines(filename):
    f = open(filename, "r")
    lines = [int(line.strip()) for line in f]

    return lines

def readall(filename):
    f = open(filename, "r")
    return f.read()