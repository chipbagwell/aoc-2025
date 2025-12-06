from aocd import get_data, submit
from collections import Counter, defaultdict, deque
import copy
import gc
import pprint
import sys
import os

# You can import your utility functions, e.g.,
# from aoc_utils import lcm, manhattan_distance

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(2000)

DAY = 1
YEAR = 2025

INPUT_DIR = "input"
INPUT_FILE = os.path.join(INPUT_DIR, f"day{DAY}.txt")

if not os.path.exists(INPUT_FILE):
    os.makedirs(INPUT_DIR, exist_ok=True)
    with open(INPUT_FILE, "w") as f:
        f.write(get_data(day=DAY, year=YEAR))

with open(INPUT_FILE, "r") as f:
    data = f.read().splitlines()

# Example data for testing
# data = [
# ]

def part_1():
  pass

def part_2():
  pass

answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

#submit(answer1)
#submit(answer2)