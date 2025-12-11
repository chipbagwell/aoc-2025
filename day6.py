from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os

# You can import your utility functions, e.g.,
import aoc_utils

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(2000)

# --- Solution ---

# Fill these in for the day
DAY = 6
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
use_example = 'test' in sys.argv
example_to_use = 0
if use_example:
    try:
        # Check if a specific example number is provided
        example_to_use = int(sys.argv[sys.argv.index('test') + 1])
    except (ValueError, IndexError):
        pass # Default to example 0
    input_file = os.path.join(INPUT_DIR, f"day{DAY}_example_{example_to_use}.txt")
    print(f"Using example input: {input_file}")
else:
    input_file = INPUT_FILE
    print(f"Using real input: {input_file}")
    
with open(input_file, "r") as f:
    data = f.read().splitlines()

def rpn_calc(input_string):
    tokens = input_string.split()
    op = tokens[-1]
    operands = [int(t) for t in tokens[:-1]]
    if op == '+':
        return sum(operands)
    elif op == '*':
        product = 1
        for operand in operands:
            product *= operand
        return product

def part_1():
    tokens = [d.split() for d in data]
    equations = [" ".join([d[l] for d in tokens]) for l in range(len(tokens[0]))]
    total = sum([rpn_calc(e) for e in equations])
    return(total)

def part_2():
    equations = ["".join([d[l] for d in data]).replace(' ','') for l in range(len(data[0]))]
    new_e = []
    try:
        while(True):
            i = equations.index('')
            temp = [t for e in equations[0:i] for t in e.replace('+',' +').replace('*',' *').split()]
            new_e.append(sorted(temp,reverse=True))
            equations = equations[i+1:]
    except (ValueError):
        temp = [t for e in equations for t in e.replace('+',' +').replace('*',' *').split()]
        new_e.append(sorted(temp, reverse=True))
    total = sum([rpn_calc(' '.join(e)) for e in new_e])
    return(total)

answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

#submit(answer1)
#submit(answer2)