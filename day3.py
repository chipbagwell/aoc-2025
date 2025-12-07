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
DAY = 3
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

def part_1():
    sum = 0
    for l in data:
        max = 0
        for i,c in enumerate(l[:-1]):
            for j,d in enumerate(l[i+1:]):
                if int(c) * 10 + int(d) > max:
                    max = int(c) * 10 + int(d)
        sum += max
    return sum

def part_2():
    sum = 0
    for l in data:
        #print(f"original: {l}")
        temp = l[0:12]
        temp_int = int(temp)
        # For each of the next digits, we need to see if adding them at the end,
        # and removing a single digit from the original makes a larger number.
        for i in range(12,len(l)):
            # i is the next digit to check.
            #print(f"checking: '{l[i]}' at index {i}")
            for j in range(0,12):
                # create new concatenation
                new_temp = temp[0:j] + temp[j+1:] + l[i]
                new_temp_int = int(new_temp)
                #print(temp, new_temp)
                if new_temp_int > temp_int:
                    #print(f"selecting: '{new_temp}' at index {i}")
                    temp_int = new_temp_int
                    temp = new_temp
                    break
        sum += temp_int
        
    return sum

answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

#submit(answer1)
#submit(answer2)