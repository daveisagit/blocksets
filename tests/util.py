"""Code to assist testing"""

from collections import deque
from itertools import combinations
from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet, OperationType


def apply_to_tuple_set(s: set, op_type: OperationType, block: Block):
    """We trust the manipulation of tuple points in a set
    This will provide a means to verify results from normalisation when tests
    cases are generated dynamically

    Args:
        s (set): A set
        op_type (OperationType): Add, Remove or Toggle
        block (Block): A block object
    """
    for t in block:
        if op_type == OperationType.ADD:
            s.add(t)
        if op_type == OperationType.REMOVE:
            s.discard(t)
        if op_type == OperationType.TOGGLE:
            if t in s:
                s.discard(t)
            else:
                s.add(t)


def apply_to_block_set(block_set: BlockSet, op_type: OperationType, block: Block):
    """Simple helper for testing

    Args:
        block_set (BlockSet): A BlockSet object
        op_type (OperationType): Add, Remove or Toggle
        block (Block): A block object
    """
    if op_type == OperationType.ADD:
        block_set.add(block)
    if op_type == OperationType.REMOVE:
        block_set.remove(block)
    if op_type == OperationType.TOGGLE:
        block_set.toggle(block)


def block_set_to_tuple_set(bs: BlockSet) -> set:
    """Covert a BlockSet to a set of tuple points
    and assert that the make-up of Blocks are disjoint

    Args:
        bs (BlockSet): A given BlockSet object

    Returns:
        set: The equivalent as a set of tuple points
    """
    tuple_set = set()
    for b in bs:
        bs = set(b)
        assert tuple_set & bs == set()
        tuple_set.update(bs)
    return tuple_set


def generate_interval_test_set_1D(n: int) -> set:
    """Generates all possible arrangements of intervals on a line
    for a given number of intervals required.

    Args:
        n (int): The number of intervals required in a test set

    Returns:
        set: A set of tuples, each tuple being a set of intervals
    """
    test_set = set()

    # perform a BFS for all ways to construct n intervals there are multiple
    # roots for the search from 2 points up to 2n points
    # if we don't use all the points then reject the outcome

    bfs = deque()
    for points in range(2, 2 * n + 1):
        point_usage = [0] * points
        state = (tuple(point_usage), tuple())
        bfs.append(state)

    while bfs:
        point_usage, blocks = bfs.popleft()
        points = len(point_usage)
        if len(blocks) == n:
            if all(True if pu > 0 else False for pu in point_usage):
                test_set.add(blocks)
            continue
        for a, b in combinations(range(points), 2):
            a, b = min(a, b), max(a, b)
            new_point_usage = list(point_usage)
            new_point_usage[a] += 1
            new_point_usage[b] += 1
            new_blocks = list(blocks)
            new_blocks.append((a, b))
            new_state = tuple(new_point_usage), tuple(new_blocks)
            bfs.append(new_state)

    return test_set


def multiple_of_tuple(t, m):
    return tuple([m * x for x in t])


def marker_to_ordinate(m, markers=None, scale=1):
    r = m
    if markers:
        r = markers[m]
    r *= scale
    return r


def generate_interval_patterns(n):
    """Splitting the line into n segments return all possible patterns.
    Effectively the binary pattern of 2^n"""
    patterns = set()
    for v in range(2**n):
        p = f"{v:0{n}b}"  # pad with leading zeros to n digits
        reading_ones = False
        pattern = []
        for idx, ch in enumerate(p):
            if ch == "1" and not reading_ones:
                interval = [idx]
                reading_ones = True
            if ch == "0" and reading_ones:
                interval.append(idx)
                pattern.append(tuple(interval))
                reading_ones = False
        if reading_ones:
            interval.append(len(p))
            pattern.append(tuple(interval))

        pattern = tuple(sorted(pattern))
        patterns.add(pattern)
    return patterns
