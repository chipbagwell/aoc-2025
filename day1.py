from aocd import get_data, submit
from aocd.models import Puzzle
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

puzzle = Puzzle(year=YEAR, day=DAY)

INPUT_DIR = "input"
INPUT_FILE = os.path.join(INPUT_DIR, f"day{DAY}.txt")

if not os.path.exists(INPUT_FILE):
    os.makedirs(INPUT_DIR, exist_ok=True)
    with open(INPUT_FILE, "w") as f:
        f.write(puzzle.input_data)

# Save example inputs
for i, example in enumerate(puzzle.examples):
    EXAMPLE_FILE = os.path.join(INPUT_DIR, f"day{DAY}_example_{i}.txt")
    if not os.path.exists(EXAMPLE_FILE):
        with open(EXAMPLE_FILE, "w") as f:
            f.write(example.input_data)
    # Save example answers
    ANS_FILE = os.path.join(INPUT_DIR, f"day{DAY}_example_{i}.ans")
    if not os.path.exists(ANS_FILE):
        with open(ANS_FILE, "w") as f:
            f.write(f"Part 1: {example.answer_a}\nPart 2: {example.answer_b}\n")

with open(INPUT_FILE, "r") as f:
    data = f.read().splitlines()

# Example data for testing
# with open(os.path.join(INPUT_DIR, f"day{DAY}_example_0.txt"), "r") as f:
#     data = f.read().splitlines()

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