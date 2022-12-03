import utils


def parse_input(path):
    return [l.split(" ") for l in utils.read_lines(path)]


shape_score = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

result_score = {
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('C', 'Y'): 0,
    ('A', 'X'): 3,
    ('B', 'Y'): 3,
    ('C', 'Z'): 3,
    ('A', 'Y'): 6,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
}

to_win = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X',
}

to_draw = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z',
}

to_lose = {
    'A': 'Z',
    'B': 'X',
    'C': 'Y',
}


def score_of_round(a, b):
    return shape_score[b] + result_score[(a, b)]


def score_of_round2(round):
    [a, r] = round

    b = ""
    if r == 'X':  # have to lose
        b = to_lose[a]
    elif r == 'Y':  # have to draw
        b = to_draw[a]
    else:  # have to win
        b = to_win[a]

    return score_of_round(a, b)


def part1(path):
    guide = parse_input(path)

    result = [score_of_round(a, b) for [a, b] in guide]

    print(sum(result))


def part2(path):
    guide = parse_input(path)

    result = [score_of_round2(r) for r in guide]

    print(sum(result))