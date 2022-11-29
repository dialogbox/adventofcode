from typing import Tuple
import numpy as np
from numpy.core.fromnumeric import shape
from functools import cache
from itertools import product
import utils

def dice():
  while True:
    for i in range(1,101):
      yield i

def score_seq(starts, dice):
  cur = starts - 1
  while True:
    i = next(dice) + next(dice) + next(dice)
    cur = (cur + i) % 10
    yield cur + 1

def play(p1_start, p2_start, d, goal):
  p1 = score_seq(p1_start, d)
  p2 = score_seq(p2_start, d)

  p1_score = 0
  p2_score = 0

  i = 0
  while True:
    p1_score += next(p1)
    i += 3
    if p1_score >= goal:
      return (i, p2_score, (p1_score, p2_score))
      break
    p2_score += next(p2)
    i += 3
    if p2_score >= goal:
      return (i, p1_score, (p1_score, p2_score))
      break

# if throws the dice 3 times, there will be 27 universes with the below results
case_counts = {3:1, 4:3, 5:6, 6:7, 7:6, 8:3, 9:1}

def draw_dd(p):
  new_win = 0
  new_p = np.array([0]*21*10).reshape(21,10)
  for score in range(len(p)):
    for pos in range(len(p[0])):
      n = p[score][pos]
      for d in case_counts:
        next_pos = ((pos + d) % 10)
        next_score = score + next_pos + 1
        n_new_univ = n * case_counts[d]
        if next_score >= 21:
          new_win += n_new_univ
        else:
          new_p[next_score][next_pos] += n_new_univ
  return (new_p, new_win)

all_combinations = [sum(d) for d in product((1, 2, 3), repeat=3)]

@cache
def play_dd(pos1, pos2, score1, score2) -> Tuple[int, int]:
  p1_win = 0
  p2_win = 0

  for d in all_combinations:
    next_pos = ((pos1 + d) % 10)
    next_score = score1 + next_pos + 1

    if next_score >= 21:
      p1_win += 1
      continue

    (new_p2_win, new_p1_win) = play_dd(pos2, next_pos, score2, next_score)
    p1_win += new_p1_win
    p2_win += new_p2_win

  return (p1_win, p2_win)

def parse_input(path):
  return utils.read_number_lines(path)

def part1(path):
  players = parse_input(path)

  result = play(players[0], players[1], dice(), 1000)
  print(result[0] * result[1])

def part2(path):
  players = parse_input(path)

  result = play_dd(players[0]-1, players[1]-1, 0, 0)
  print(result[0])