from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from functools import lru_cache
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os
import math

# You can import your utility functions, e.g.,
import aoc_utils

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(10000)

# --- Solution ---

# Fill these in for the day
DAY = 8
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

def calc_distance(a, b):
    return math.sqrt((int(a[0]) - int(b[0]))**2 + (int(a[1]) - int(b[1]))**2 + (int(a[2]) - int(b[2]))**2)


def part_1():
    distances = []
    for i, line in enumerate(data):
        for b in data[i+1:]:
            distances.append((calc_distance(line.split(','), b.split(',')), line, b))
    distances.sort(key=lambda x: x[0])
    count_compare = 10 if use_example else 1000
    count = 0
    connections = []
    for d in distances:
        d_1_match = None
        d_2_match = None
        for i,c in enumerate(connections):
            if d[1] in c:
                d_1_match = i
            if d[2] in c:
                d_2_match = i
            
        if d_1_match is not None and d_2_match is not None and d_1_match == d_2_match:
            pass
        elif d_1_match is not None and d_2_match is None:
            connections[d_1_match].add(d[2])
        elif d_1_match is None and d_2_match is not None:
            connections[d_2_match].add(d[1])
        elif d_1_match is not None and d_2_match is not None:
            connections[d_1_match].update(connections[d_2_match])
            connections.pop(d_2_match)
        else:
            connections.append({d[1], d[2]})
        count += 1
        if count == count_compare:
            break

    c = sorted(connections, key=lambda x: len(x), reverse=True)
    return len(c[0]) * len(c[1]) * len(c[2])

def part_2():
    distances = []
    total_boxes = len(data)
    for i, line in enumerate(data):
        for b in data[i+1:]:
            distances.append((calc_distance(line.split(','), b.split(',')), line, b))
    distances.sort(key=lambda x: x[0])
    count = 0
    connections = []
    connections.append({distances[0][1], distances[0][2]})
    for d in distances[1:]:
        d_1_match = None
        d_2_match = None
        for i,c in enumerate(connections):
            if d[1] in c:
                d_1_match = i
            if d[2] in c:
                d_2_match = i
            
        if d_1_match is not None and d_2_match is not None and d_1_match == d_2_match:
            pass
        elif d_1_match is not None and d_2_match is None:
            connections[d_1_match].add(d[2])
        elif d_1_match is None and d_2_match is not None:
            connections[d_2_match].add(d[1])
        elif d_1_match is not None and d_2_match is not None:
            connections[d_1_match].update(connections[d_2_match])
            connections.pop(d_2_match)
        else:
            connections.append({d[1], d[2]})
        count += 1
        if len(connections) == 1:
            if len(connections[0]) == total_boxes:
                return int(d[1].split(',')[0]) * int(d[2].split(',')[0])

    c = sorted(connections, key=lambda x: len(x), reverse=True)
    return len(c[0]) * len(c[1]) * len(c[2])



answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

# submit(answer1)
# submit(answer2)