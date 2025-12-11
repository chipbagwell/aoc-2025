from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from functools import lru_cache
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os

# You can import your utility functions, e.g.,
from aoc_utils import pivot_2d_y_to_x, check_bounds

# Set a higher recursion limit for puzzles that need it
sys.setrecursionlimit(10000)

# --- Solution ---

# Fill these in for the day
DAY = 7
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

# --- Input Handling ---
use_example = "test" in sys.argv
example_to_use = 0
if use_example:
    try:
        # Check if a specific example number is provided
        example_to_use = int(sys.argv[sys.argv.index("test") + 1])
    except (ValueError, IndexError):
        pass  # Default to example 0
    input_file = os.path.join(INPUT_DIR, f"day{DAY}_example_{example_to_use}.txt")
    print(f"Using example input: {input_file}")
else:
    input_file = INPUT_FILE
    print(f"Using real input: {input_file}")

with open(input_file, "r") as f:
    data = f.read().splitlines()
d = pivot_2d_y_to_x(data)

def find_first_char(c, data):
    for y,a in enumerate(data):
        for x,b in enumerate(a):
            if c == b:
                return (y,x)

@lru_cache(maxsize=None)
def next_splitter(s):
    try:
        return d[s[0]][s[1]+1:].index('^') + s[1]+1
    except ValueError:
        return None

            
def part_1():
    starts = set()
    previous_starts = set()
    splitters = set()
    starts.add(find_first_char('S', d))
    while(len(starts)):
        s = starts.pop()
        if s in previous_starts:
            continue
        previous_starts.add(s)
        splitter = next_splitter(s)
        if splitter is None:
            continue
        splitters.add((s[0],splitter))
        right = (s[0]-1,splitter)
        left = (s[0]+1,splitter)
        if check_bounds(right, d):
            starts.add(right)
        if check_bounds(left, d):
            starts.add(left)
    return len(splitters)


@lru_cache(maxsize=None)
def count_paths(current_pos):
    splitter_col = next_splitter(current_pos)
    if splitter_col is None:
        return 1

    total = 0
    # right (in d coordinates, row - 1)
    r_pos = (current_pos[0] - 1, splitter_col)
    if check_bounds(r_pos, d):
        total += count_paths(r_pos)

    # left (in d coordinates, row + 1)
    l_pos = (current_pos[0] + 1, splitter_col)
    if check_bounds(l_pos, d):
        total += count_paths(l_pos)

    return total


def part_2():
    count_paths.cache_clear()
    start_pos = find_first_char('S', d)
    return count_paths(start_pos)


answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

# submit(answer1)
# submit(answer2)