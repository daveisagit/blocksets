"""Tests for the BlockSet class with a focus on normalisation"""

from itertools import permutations, product
from math import inf
import pytest

from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet, OperationType
from block_data import (
    blocks_1D_all_arrangements_of_2,
    blocks_1D_all_arrangements_of_3,
    blocks_1D_arbitrary_set_1,
    blocks_2D_all_arrangements_of_2,
    blocks_2D_arbitrary_set_example,
    blocks_3D_all_arrangements_of_2,
)
from util import apply_to_block_set, apply_to_tuple_set


#
# Helper functions for test identification
#


def block_ids(blocks):
    return f" Blocks: " + " | ".join([str(block) for block in blocks]) + " "


def operation_ids(operations):
    return (
        " Operations: ("
        + " ".join([operation.value for operation in operations])
        + ") "
    )


#######################################################################################
# 1 Dimensional normalisation
#######################################################################################


# Dimensions: 1
# All possible operations (9)
# All possible arrangements of 2 (13)


@pytest.mark.parametrize(
    "test_sets",
    blocks_1D_all_arrangements_of_2(),
    ids=block_ids,
)
@pytest.mark.parametrize(
    "operations",
    product(list(OperationType), repeat=2),
    ids=operation_ids,
)
def test_normalisation_all_2_blocks_1D(test_sets, operations):

    ts = set()
    bs = BlockSet(1)
    for idx, block in enumerate(test_sets):
        apply_to_tuple_set(ts, operations[idx], block)
        apply_to_block_set(bs, operations[idx], block)
    assert ts == set(bs.units())


# Dimensions: 1
# 1st fixed as + (9)
# All possible arrangements of 3 (409)


def operation_permutations_fixed_first(n):
    repeats = n - 1
    perms = [
        (OperationType.ADD,) + t for t in product(list(OperationType), repeat=repeats)
    ]
    return perms


@pytest.mark.parametrize(
    "test_sets",
    blocks_1D_all_arrangements_of_3(),
    ids=block_ids,
)
@pytest.mark.parametrize(
    "operations",
    operation_permutations_fixed_first(3),
    ids=operation_ids,
)
#
# WARNING - this test has 3681 instances so for development
# this has been disabled x_
#
# It only adds on 30s though, but feels like a drag ...
#
# Given the coverage from all of any 2 above and the
# 3 of an arbitrary 7 below, it might not add much
# value to the overall coverage of cases
#
def x_test_normalisation_all_3_blocks_1D(test_sets, operations):

    ts = set()
    bs = BlockSet(1)
    for idx, block in enumerate(test_sets):
        apply_to_tuple_set(ts, operations[idx], block)
        apply_to_block_set(bs, operations[idx], block)
    assert ts == set(bs.units())


# Dimensions: 1
# 1st fixed as + (9)
# Any 3 from blocks_1D_arbitrary_set_1 (210: any 3 from the 7)


@pytest.mark.parametrize(
    "test_sets",
    permutations(blocks_1D_arbitrary_set_1(), 3),
    ids=block_ids,
)
@pytest.mark.parametrize(
    "operations",
    operation_permutations_fixed_first(3),
    ids=operation_ids,
)
def test_normalisation_arbitrary_3_1D(test_sets, operations):
    ts = set()
    bs = BlockSet(1)
    for idx, block in enumerate(test_sets):
        apply_to_tuple_set(ts, operations[idx], block)
        apply_to_block_set(bs, operations[idx], block)
    assert ts == set(bs.units())


def test_normalisation_on_open_intervals_1D(d1_positives, d1_negatives):
    all = Block(inf)
    neg = Block(-inf, 0)
    rmv = Block(-5, 5)
    bs = BlockSet(1)
    bs.add(all)
    bs.remove(rmv)
    assert set(bs) == {
        ((-inf,), (-5,)),
        ((5,), (inf,)),
    }
    bs.toggle(rmv)
    assert set(bs) == {all}

    d1_positives.remove(rmv)
    assert set(d1_positives) == {
        ((5,), (inf,)),
    }

    d1_positives.toggle(rmv)
    assert set(d1_positives) == {
        ((-5,), (inf,)),
    }

    d1_positives.add(neg)
    assert set(bs) == {all}

    bs.clear()
    bs.add(all)
    bs.toggle(all)
    assert set(bs) == set()

    bs.add(all)
    bs.toggle(neg)
    assert set(bs) == {
        ((0,), (inf,)),
    }


#######################################################################################
# 2 Dimensional normalisation
#######################################################################################


def test_normalisation_sanity_2D():
    """
    Just want to be sure this really works on a simple easy to read example

    x = (1,1)..(9,7)
    y = (5,4)..(13,10)

        yyyyyyyy
        y      y
        y      y
    xxxxyxxx   y
    x   y  x   y
    x   yyyyyyyy
    x      x
    x      x
    xxxxxxxx

    Normalises to
    x = (1,1)..(5,7)
    | = (5,1)..(9,10)
    y = (9,4)..(13,10)

        yyyyyyyy
        |  |   y
        |  |   y
    xxxx|  |   y
    x   |  |   y
    x   |  |yyyy
    x   |  |
    x   |  |
    xxxxxxxx

    """
    bs = BlockSet(2)
    x = Block((1, 1), (9, 7))
    y = Block((5, 4), (13, 10))

    bs.add(x)
    bs.add(y)
    assert set(bs) == {
        ((1, 1), (5, 7)),
        ((5, 1), (9, 10)),
        ((9, 4), (13, 10)),
    }

    bs.clear()
    bs.add(x)
    bs.remove(y)
    s = set(bs)
    assert set(bs) == {
        ((1, 1), (5, 7)),
        ((5, 1), (9, 4)),
    }

    bs.clear()
    bs.add(x)
    bs.toggle(y)
    assert set(bs) == {
        ((1, 1), (5, 7)),
        ((5, 1), (9, 4)),
        ((5, 7), (9, 10)),
        ((9, 4), (13, 10)),
        ((5, 1), (9, 4)),
    }


# Dimensions: 2
# 1st fixed as + (27)
# Any 4 from blocks_2D_arbitrary_set_example (24)


@pytest.mark.parametrize(
    "test_sets",
    permutations(blocks_2D_arbitrary_set_example(), 4),
    ids=block_ids,
)
@pytest.mark.parametrize(
    "operations",
    operation_permutations_fixed_first(4),
    ids=operation_ids,
)
def test_normalisation_example_2D(test_sets, operations):

    ts = set()
    bs = BlockSet(2)
    for idx, block in enumerate(test_sets):
        apply_to_tuple_set(ts, operations[idx], block)
        apply_to_block_set(bs, operations[idx], block)
    assert ts == set(bs.units())


# Dimensions: 2
# All possible operations (9)
# All possible arrangements of 2 (13x13 = 169)


@pytest.mark.parametrize(
    "test_sets",
    blocks_2D_all_arrangements_of_2(),
    ids=block_ids,
)
@pytest.mark.parametrize(
    "operations",
    product(list(OperationType), repeat=2),
    ids=operation_ids,
)
def test_normalisation_all_2_blocks_2D(test_sets, operations):
    ts = set()
    bs = BlockSet(2)
    for idx, block in enumerate(test_sets):
        apply_to_tuple_set(ts, operations[idx], block)
        apply_to_block_set(bs, operations[idx], block)

    assert ts == set(bs.units())


def test_normalisation_on_open_intervals_2D():
    square = Block((-5, -5), (5, 5))
    quad = Block((0, 0), (inf, inf))
    all = Block((-inf, -inf), (inf, inf))
    bs = BlockSet(2)
    bs.add(square)
    bs.remove(quad)
    assert set(bs) == {
        ((-5, -5), (0, 5)),
        ((0, -5), (5, 0)),
    }

    bs.clear()
    bs.add(square)
    bs.toggle(all)
    assert set(bs) == {
        ((-inf, -inf), (-5, inf)),
        ((-5, 5), (5, inf)),
        ((-5, -inf), (5, -5)),
        ((5, -inf), (inf, inf)),
    }

    bs.clear()
    bs.add(all)
    bs.toggle(quad)
    assert set(bs) == {
        ((-inf, -inf), (0, inf)),
        ((0, -inf), (inf, 0)),
    }


#######################################################################################
# 3 Dimensional normalisation
#######################################################################################


def test_normalisation_sanity_3D():
    """
    Just want to be sure this really works on a simple example
    Rubik cube,

    Remove 2356 from Top layer
    ---
    123      1xx
    456  ->  4xx
    789      789


    """
    bs = BlockSet(3)
    x = Block((0, 0, 0), (3, 3, 3))  # cube
    y = Block((1, 1, 2), (3, 3, 3))  # 2356 on top layer

    bs.add(x)
    bs.add(y)
    assert set(bs) == {x}

    bs.clear()
    bs.add(x)
    bs.remove(y)
    assert set(bs) == {
        ((0, 0, 0), (1, 3, 3)),  # left face
        ((1, 1, 0), (3, 3, 2)),  # 2x2x2 section in middle+bottom
        ((1, 0, 0), (3, 1, 3)),  # 6 on front 235689
    }

    # Construct the same result another way
    bs2 = BlockSet(3)
    left_face = Block((0, 0, 0), (1, 3, 3))
    front_face = Block((0, 0, 0), (3, 1, 3))
    bottom_2_layers = Block((0, 0, 0), (3, 3, 2))
    bs2.add(left_face)
    bs2.add(front_face)
    bs2.add(bottom_2_layers)
    assert set(bs2) == set(bs)


# Dimensions: 3
# Just ADD
# All possible arrangements of 2 (13x13x13 = 2197)


@pytest.mark.parametrize(
    "test_sets",
    blocks_3D_all_arrangements_of_2(),
    ids=block_ids,
)
@pytest.mark.parametrize(
    "operations",
    [[OperationType.ADD] * 3],
    ids=operation_ids,
)
def test_normalisation_all_2_blocks_3D(test_sets, operations):
    ts = set()
    bs = BlockSet(3)
    for idx, block in enumerate(test_sets):
        apply_to_tuple_set(ts, operations[idx], block)
        apply_to_block_set(bs, operations[idx], block)

    assert ts == set(bs.units())
