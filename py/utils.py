
def read_lines(filename):
    f = open(filename, "r")
    lines = [line.strip() for line in f]

    return lines


def read_numbers_csv(filename):
    f = open(filename, "r")
    lines = [int(line.split(",")) for line in f]

    return lines


def read_number_lines(filename):
    f = open(filename, "r")
    lines = [int(line.strip()) for line in f]

    return lines
