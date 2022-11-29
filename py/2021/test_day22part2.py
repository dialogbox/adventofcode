from day22part2 import diff_range

diff_range_test_data = [
    [((-5, 5), (1, 10)), ([(-5, 0)], [(1, 5)])],
    [((-5, 5), (1, 3)), ([(-5, 0), (4, 5)], [(1, 3)])],
    [((-5, 5), (-10, 10)), ([], [(-5, 5)])],
    [((-5, 5), (-10, 0)), ([(1, 5)], [(-5, 0)])],
    [((-5, 5), (6, 10)), ([(-5, 5)], [])],
    [((-36, 17), (-21, 23)), ([(-36, -22)], [(-21, 17)])],
]


def test_diff_range():
    for (input, out) in diff_range_test_data:
        assert diff_range(input[0], input[1]) == out
