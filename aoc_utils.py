from functools import reduce
from math import gcd  
from typing import Iterable
import numpy as np

def find_all(a_str, sub, overlap=False):
    """
    find all occurances of the substring 'sub' in the source string 'a_str'
    @params
    a_str:    source string
    sub:      target substring
    overlap:  True for overlapping matchs, False for non-overlapping matches
    """
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += 1 if overlap else len(sub)


def lcm(vals: Iterable[int]) -> int:
    """
    Least common multiple

    Parameters:
    vals list[int]: the list of integers as input

    Returns:
    int: the least common multiple of all inputs
    """
    return reduce(lambda a,b: a*b // gcd(a,b), vals)

def pivot_2d_y_to_x(data):
    """
    Given a list of strings, return a new list of strings
    Where the first string is the concatenation of the first
    characters of each original string, the second string
    is the concatenation of the second characters of each 
    original string (reflection along the n,n diagonal)
    
    Parameters:
    data list[str]: the original list of strings as input
    
    Returns:
    list[str]: the return list of strings
    """
    return [''.join([d[l] for d in data ]) for l in range(len(data[0]))]

def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """
    Given two points (as tuples of ints), calculate the 'manhattan' distance
    between them.
    
    Parameters:
    p1 tuple[int, int]: the first point (y, x) or (x, y)
    p2 tuple[int, int]: the second point (y, x) or (x, y)
    
    Returns:
    int: the 'manhattan' distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def check_bounds(y_x, grid):
  """
  Given a list of 'list-like' (strings work),
  Check to see if the given coordinates are in the gride or not
  
  Parameters:
  y int: the up/down row
  x int: the left/right column
  grid list of 'list-like'
  
  Returns:
  bool: True if inside the grid, False otherwise
  """
  return 0 <= y_x[0] < len(grid) and 0 <= y_x[1] < len(grid[0])

def gen_adj_udlr(d, point):
    """
    Given a list of 'list-like' (strings work),
    and given a tuple of (y,x), return a list of the
    up, down, left, and right adjacent coordinates bounded
    by the size of the grid and not including the original
    point
    
    Parameters:
    d list of 'list-like'
    point tuple of (y,x)
    
    Returns:
    list of (y,x) adjacent points
    """
    return [
        p
        for p in [
            (max(0, point[0] - 1), point[1]),
            (min(len(d) - 1, point[0] + 1), point[1]),
            (point[0], max(0, point[1] - 1)),
            (point[0], min(len(d[0]) - 1, point[1] + 1)),
        ]
        if p != (point[0], point[1])
    ]

def list_of_strings_to_2d_nparray_ord(vals):
    """
    Given a list of strings, return as a 2D nparray of ords
    
    Parameters:
    vals: list of strings
    
    Returns:
    array: nparray of ords
    """
    array = np.array([np.array([ord(c) for c in l]) for l in vals])
    return array
