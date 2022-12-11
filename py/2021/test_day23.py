#
# This is a legacy standalone script
# python3 dayXX.py
#
from day23 import *

done = [
    list("..........."),
    list("##A#B#C#D##"),
    list(" #A#B#C#D"),
]

not_done1 = [
    list("..........."),
    list("##A#C#B#D##"),
    list(" #A#B#C#D"),
]

not_done2 = [
    list(".A........."),
    list("##.#C#B#D##"),
    list(" #A#B#C#D"),
]


def test_is_done():
    assert is_done(done)
    assert is_done(not_done1)
    assert is_done(not_done2)
