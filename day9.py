from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os
import matplotlib.pyplot as plt

# You can import your utility functions, e.g.,
from aoc_utils import is_point_in_polygon

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(2000)

# --- Solution ---

# Fill these in for the day
DAY = 9
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

def str_to_coords(a):
    return (int(a.split(',')[0]),int(a.split(',')[1]))

def calc_area(a,b):
    return (abs(a[0] - b[0])+1) * (abs(a[1] - b[1])+1) 

def get_rectangle_perimeter(corners):
    xs = [p[0] for p in corners]
    ys = [p[1] for p in corners]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    perimeter = set()
    for x in range(min_x, max_x + 1):
        perimeter.add((x, min_y))
        perimeter.add((x, max_y))
    for y in range(min_y, max_y + 1):
        perimeter.add((min_x, y))
        perimeter.add((max_x, y))
    return list(perimeter)

def plot_polygon(points, shape):
    """
    Plots the polygon defined by the given list of vertices.
    """
    if not points:
        return

    x = [p[0] for p in points]
    y = [p[1] for p in points]

    x2 = [p[0] for p in shape]
    y2 = [p[1] for p in shape]

    # Close the loop to visualize the complete polygon
    x.append(x[0])
    y.append(y[0])

    plt.figure()
    plt.plot(x, y, marker='o', linestyle='-')
    plt.plot(x2, y2, marker='X', linestyle='--', color='red')
    plt.show()

def part_1():
    area = []
    for i,a in enumerate(data):
        for b in data[i:]:
            area.append(calc_area(str_to_coords(a),str_to_coords(b)))
    return max(area)


def part_2():
    max_area = 0
    points = [str_to_coords(d) for d in data]
    diags = [(a,b,(a[0],b[1]),(b[0],a[1])) for i,a in enumerate(points) for b in points[i+1:]]
    for d in diags:
        a = calc_area(d[0], d[1])
        # Check if all points on the perimeter of the rectangle are inside the polygon
        if a < max_area:
            continue
        test = [is_point_in_polygon(p, points) for p in get_rectangle_perimeter([d[0], d[1], d[2], d[3]])]
        if all(test):
            max_area = max(max_area, a)
    return max_area


answer1 = part_1()
print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

# submit(answer1)
# submit(answer2)