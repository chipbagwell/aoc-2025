from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os

# You can import your utility functions, e.g.,
from aoc_utils import show_diff

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(2000)

# --- Solution ---

# Fill these in for the day
DAY = 5
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

def split_lists(data):
    try:
        # Find the index of the first empty string.
        split_index = data.index('')
        
        # The first list contains all strings before the empty one.
        first_list = data[:split_index]
        
        # The second list contains all strings after the empty one.
        second_list = data[split_index + 1:]
        
        return first_list, second_list
            
    except ValueError:
        # This will happen if there is no empty string in the data.
        print("No empty string found to split the list.")
    
def range_reduce(range1: tuple[int, int], range_list: list[tuple[int, int]]):
    """
    Reduces two ranges if they overlap or are adjacent.

    Parameters:
    range1 (tuple[int, int]): The first range.
    range2 (list[tuple[int, int]]): The list of ranges to check against.
    """
    retval = range1
    for range2 in range_list:
        #print(f"testing range1: {range1} against range2: {range2}")
        # first range is completely less than second, do nothing
        if range1[0] < range2[0] and range1[1] < range2[0]:
            #print(". first range is completely less than second")
            continue
        # first range is completely greater than second, do nothing
        if range1[0] > range2[1] and range1[1] > range2[1]:
            #print(". first range is completely greater than second")
            continue
        if range1[0] >= range2[0] and range1[0] <= range2[1]:
            #print(". first range start is within second range")
            if range1[1] >= range2[0] and range1[1] <= range2[1]:
                #print(". first range end is within second range")
                #print(". first range is completely covered by second range")
                retval = range2
                break
            else:
                #print(". first range end is not within second range")
                retval = (range2[0],range1[1])
                break
        else:
            #print(". first range start is not within second range")
            if range1[1] >= range2[0] and range1[1] <= range2[1]:
                #print(". first range end is within second range")
                retval = (range1[0],range2[1])
                break
            else:
                #print(". first range end is not within second range")
                #print(". first range completely overlaps second range")
                continue
    #print(f"returning: {retval}")
    return retval


        

def part_1():
    fresh = 0
    ranges, fruit = split_lists(data)
    boundaries = [(int(r.split('-')[0]),int(r.split('-')[1])) for r in ranges]
    for f in fruit:
        item = int(f)
        for b in boundaries:
            if b[0] <= item <= b[1]:
                fresh += 1
                break
    return fresh

def part_2():
    fresh = 0
    ranges, fruit = split_lists(data)
    boundaries = [(int(r.split('-')[0]),int(r.split('-')[1])) for r in ranges]
    new_boundaries = []
    
    while(True):
        new_set = set()
        for i,r in enumerate(boundaries):
            new_set.add(range_reduce(r,boundaries[:i]+boundaries[i+1:]))
        
        new_boundaries = list(new_set)
        #show_diff(boundaries,new_boundaries)
        if set(new_boundaries) == set(boundaries):
            break
        boundaries = new_boundaries.copy()
    for r in boundaries:
        fresh += r[1] - r[0] + 1
    return fresh

answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

#submit(answer1)
#submit(answer2)