from aocd import get_data, submit
from collections import Counter, defaultdict, deque
from aocd.models import Puzzle
import copy
import gc
import pprint
import sys
import os
import itertools
from concurrent.futures import ProcessPoolExecutor

# You can import your utility functions, e.g.,
import aoc_utils

# Set a higher recursion limit for puzzles that need it
# sys.setrecursionlimit(2000)

# --- Solution ---

# Fill these in for the day
DAY = 10
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


def str_to_int(s):
    """
    Converts a string of '#' and '.' to an integer.
    '#' represents 1, '.' represents 0.
    Example: "#..#" -> 9 (binary 1001)
    """
    return int(s.replace('#', '1').replace('.', '0')[::-1], 2)

def button_to_int(s):
    s = s.strip("()")
    if not s:
        return 0
    return sum(1 << int(x) for x in s.split(","))

def parse_input_part1(l):
    tokens = l.split()
    end_state = str_to_int(tokens[0][1:-1])
    joltage = tokens[-1]
    buttons = [button_to_int(t) for t in tokens[1:-1]]
    return end_state, joltage, buttons

def solve_xor_subset(operands: list[int], target: int) -> list[list[int]]:
    """
    Finds all subsets of operands that XOR sum to the target.
    
    Parameters:
    operands: list[int] - The available numbers to XOR.
    target: int - The number we want to reach.
    
    Returns:
    list[list[int]] - A list of all valid subsets. Returns empty list if impossible.
    """
    # Dictionary to store the basis: { pivot_bit_index: (basis_value, components_mask) }
    # components_mask is a bitmask where the Nth bit is set if the Nth operand is used.
    basis = {} 
    # List to store masks that sum to 0 (the null space of the matrix)
    null_masks = []
    
    # 1. Build Basis with Component Tracking
    for i, op in enumerate(operands):
        temp_val = op
        temp_mask = 1 << i # Track that this value comes from the i-th operand
        
        for pivot_bit in sorted(basis.keys(), reverse=True):
            basis_val, basis_mask = basis[pivot_bit]
            # If the pivot bit is set in our current value, XOR it out
            if (temp_val >> pivot_bit) & 1:
                temp_val ^= basis_val
                temp_mask ^= basis_mask
        
        if temp_val > 0:
            # We found a new basis vector. The pivot is its Most Significant Bit.
            msb = temp_val.bit_length() - 1
            basis[msb] = (temp_val, temp_mask)
        else:
            # This operand is linearly dependent on the basis. It forms a cycle.
            null_masks.append(temp_mask)

    # 2. Solve for Target
    # We try to reduce the target to 0 using our basis.
    # We accumulate the masks of the basis vectors we use.
    result_mask = 0
    temp_target = target
    
    for pivot_bit in sorted(basis.keys(), reverse=True):
        basis_val, basis_mask = basis[pivot_bit]
        if (temp_target >> pivot_bit) & 1:
            temp_target ^= basis_val
            result_mask ^= basis_mask
            
    if temp_target != 0:
        return []

    # 3. Generate All Solutions
    # Any solution is the primary solution XORed with any linear combination of null_masks.
    all_subsets = []
    
    # Iterate through all 2^k combinations of the null space vectors
    for i in range(len(null_masks) + 1):
        for combination in itertools.combinations(null_masks, i):
            current_mask = result_mask
            for m in combination:
                current_mask ^= m
            
            subset = [operands[j] for j in range(len(operands)) if (current_mask >> j) & 1]
            all_subsets.append(subset)
            
    return all_subsets

def solve_linear_diophantine(matrix: list[list[int]], target: list[int]) -> list[int] | None:
    """
    Solves Ax = b for non-negative integer x.
    
    Parameters:
    matrix: list[list[int]] - The coefficient matrix A. 
                              Rows are equations, Columns are variables.
                              matrix[i][j] is the effect of button j on index i.
    target: list[int] - The target vector b.
    
    Returns:
    list[int] | None - A list of integer counts for each variable (button), 
                       or None if no solution exists.
    """
    n_vars = len(matrix[0])
    n_eqs = len(matrix)
    
    # Calculate upper bounds for each variable
    # If A[i][j] * x[j] <= target[i], then x[j] <= target[i] // A[i][j]
    bounds = []
    for j in range(n_vars):
        min_bound = float('inf')
        for i in range(n_eqs):
            coeff = matrix[i][j]
            if coeff > 0:
                min_bound = min(min_bound, target[i] // coeff)
        bounds.append(int(min_bound) if min_bound != float('inf') else 10000) # Default cap if unbounded

    min_total = float('inf')

    def backtrack(idx, current_sums, current_total):
        nonlocal min_total
        
        if current_total >= min_total:
            return

        if idx == n_vars:
            if current_sums == target:
                min_total = current_total
            return

        # Dynamic bound: constrain this variable based on remaining space in target
        limit = bounds[idx]
        for i in range(n_eqs):
            if matrix[i][idx] > 0:
                limit = min(limit, (target[i] - current_sums[i]) // matrix[i][idx])
        
        for val in range(limit + 1):
            new_sums = [current_sums[i] + val * matrix[i][idx] for i in range(n_eqs)]
            backtrack(idx + 1, new_sums, current_total + val)

    backtrack(0, [0] * n_eqs, 0)
    return min_total if min_total != float('inf') else None

def part_1():
    sum = 0
    for d in data:
        print(f"Input: {d}")
        value, joltage, buttons = parse_input_part1(d)
        solutions = solve_xor_subset(buttons, value)
        
        if not solutions:
            print("No solution found.")
        else:
            solutions.sort(key=len)
            print(f"Found {len(solutions)} solutions.")
            print(f"Shortest solution (length {len(solutions[0])}): {solutions[0]}")
            sum += len(solutions[0])
    return sum

def solve_line_part2(d):
    # Parse Input: (0,1) (1,2) [10,20]
    # Tokens: "(0,1)", "(1,2)", "[10,20]"
    tokens = d.split()
    
    # Target vector (b)
    target = [int(c) for c in tokens[-1][1:-1].split(',')]
    
    # Build Matrix (A)
    # Columns = Buttons, Rows = Indices in Target
    # matrix[row][col] = 1 if button 'col' affects index 'row'
    button_tokens = tokens[1:-1]
    matrix = [[0] * len(button_tokens) for _ in range(len(target))]
    
    for col_idx, t in enumerate(button_tokens):
        indices = [int(x) for x in t.strip("()").split(',')]
        for row_idx in indices:
            if row_idx < len(matrix):
                matrix[row_idx][col_idx] = 1
                
    answer = solve_linear_diophantine(matrix, target)
    print(f"Data: {d} Answer: {answer}")
    return answer

def part_2():
    total_sum = 0
    with ProcessPoolExecutor(max_workers=12) as executor:
        results = executor.map(solve_line_part2, data)

    for i, (d, ans) in enumerate(zip(data, results)):
        if ans is not None:
            total_sum += ans
    return total_sum



if __name__ == "__main__":
    answer1 = part_1()
    print(f"Part 1: {answer1}")
    answer2 = part_2()
    print(f"Part 2: {answer2}")

    # submit(answer1)
    # submit(answer2)