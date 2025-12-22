from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from functools import lru_cache
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os
import networkx as nx
import matplotlib as plt

# You can import your utility functions, e.g.,
import aoc_utils

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(2000)

# --- Solution ---

# Fill these in for the day
DAY = 11
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


def part_1():
    G = nx.DiGraph()
    for d in data:
        tokens = d.split()
        start = tokens[0][:-1]
        ends = tokens[1:]
        for end in ends:
            G.add_edge(start, end)
    paths = list(nx.all_simple_paths(G, "you", "out"))
    return(len(paths) )

G = nx.DiGraph()

@lru_cache(maxsize=None)
def count_paths(current_node, target_node):
    if current_node == target_node:
        return 1
    total_paths = 0
    for next_node in G[current_node]:
        total_paths += count_paths(next_node, target_node)
    return total_paths
    
def part_2():
    global G
    sum = 0
    nodes = set()
    for d in data:
        tokens = d.split()
        start = tokens[0][:-1]
        nodes.add(start)
        ends = tokens[1:]
        for end in ends:
            G.add_edge(start, end)
            nodes.add(end)

    paths_to_fft = count_paths("svr", "fft")
    paths_to_dac = count_paths("fft", "dac")
    paths_to_out = count_paths("dac", "out")

    print(f"paths to fft: {paths_to_fft}")
    print(f"paths to dac: {paths_to_dac}")
    print(f"paths to out: {paths_to_out}")
    return paths_to_fft * paths_to_dac * paths_to_out

def part_3():
    sum = 0
    G = nx.DiGraph()
    for d in data:
        tokens = d.split()
        start = tokens[0][:-1]
        ends = tokens[1:]
        for end in ends:
            G.add_edge(start, end)

    if nx.has_path(G, "svr", "fft"):
        print("there is a path from svr to fft")
    else:
        print("there is no path from svr to fft")
    if nx.has_path(G, "fft", "dac"):
        print("there is a path from fft to dac")
    else:
        print("there is no path from fft to dac")
    if nx.has_path(G, "dac", "out"):
        print("there is a path from dac to out")
    else:
        print("there is no path from dac to out")

    paths = deque()
    paths.append(("svr",))
    paths_to_fft = 0
    while paths:
        path = paths.pop()
        if(path[-1] == "fft"):
            print(f"path to fft found: {path}")
            paths_to_fft +=1
            continue
        elif(path[-1] == "dac"):
            print(f"dropping path to dac before fft")
            continue
        elif(path[-1] == "out"):
            print(f"dropping path to out before fft")
            continue
        else:
            paths.extend(path + (node,) for node in G[path[-1]] if node not in path)
            print(f"paths len: {len(paths)}")
    print(f"paths to fft: {paths_to_fft}")
    pass


#answer1 = part_1()
#print(f"Part 1: {answer1}")
answer2 = part_2()
print(f"Part 2: {answer2}")

# submit(answer1)
# submit(answer2)