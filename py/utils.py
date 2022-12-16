from __future__ import annotations
import itertools
import re
import functools


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


def read_grid(filename):
    return [list(l) for l in read_lines(filename)]


def read_number_grid(filename):
    lines = read_lines(filename)
    return [[int(n) for n in list(line)] for line in lines]


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


def split_list_by_elem(l, delim):
    return [
        list(y) for x, y in itertools.groupby(l, lambda z: z == delim) if not x
    ]


def parse_coord_str(str):
    x, y = str.split(",")
    return (int(x), int(y))


def print_line_by_line(somelist):
    for l in somelist:
        print(l)


@functools.total_ordering
class Coord:
    x: int = 0
    y: int = 0

    def __init__(self, *args) -> None:
        if len(args) == 1:
            if type(args[0]) == tuple:
                (self.x, self.y) = args[0]
            elif type(args[0]) == str:
                m = re.match(r"(x=)?([-0-9].*)\s*,\s*(y=)?([-0-9].*)", args[0])
                if not m:
                    raise ValueError(f"Invalid coordinate string {args[0]}")

                self.x = int(m.group(2))
                self.y = int(m.group(4))
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def to_tuple_y_first(self) -> tuple[int, int]:
        return (self.y, self.x)

    def __lt__(self, other) -> bool:
        return self.to_tuple() < other.to_tuple()

    def __str__(self) -> str:
        return f"x={self.x},y={self.y}"

    def __repr__(self) -> str:
        return f"x={self.x},y={self.y}"

    def __eq__(self, other: Coord) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


#
# Include Range
#
@functools.total_ordering
class Range:
    From: int = 0
    To: int = 0

    def __init__(self, f: int, t: int) -> None:
        self.From = f
        self.To = t

    def __lt__(self, other: Range) -> bool:
        return self.to_tuple() < other.to_tuple()

    def __str__(self) -> str:
        return f"[{self.From},{self.To}]"

    def __repr__(self) -> str:
        return f"[{self.From},{self.To}]"

    def __eq__(self, other: Range) -> bool:
        return self.From == other.From and self.To == other.To

    def __hash__(self) -> int:
        return hash((self.From, self.To))

    def __len__(self):
        return self.To - self.From + 1

    def to_tuple(self) -> tuple[int, int]:
        return (self.From, self.To)

    def is_included(self, i: int) -> bool:
        return i >= self.From and i <= self.To

    def merge(self, other: Range) -> list[Range]:
        # no overlap nor meet
        if self.To + 1 < other.From or other.To + 1 < self.From:
            return sorted([self, other])

        return [Range(min(self.From, other.From), max(self.To, other.To))]


# TODO
class DiscreteRanges:
    ranges: list[Range] = list()

    def __init__(self) -> None:
        pass

    def __init__(self, l: list[Range]) -> None:
        self.ranges = l.copy()

    def __init__(self, *argv) -> None:
        self.ranges = argv
