"""Test the testing utilities"""

from blocksets.classes.block import Block
from blocksets.classes.blockset import OperationType
from util import (
    apply_to_tuple_set,
    generate_interval_patterns,
    generate_interval_test_set_1D,
)


def test_apply_to_tuple_set():

    s = set()

    b = Block(2, 6)
    apply_to_tuple_set(s, OperationType.ADD, b)
    assert s == {(2,), (3,), (4,), (5,)}

    b = Block(4, 8)
    apply_to_tuple_set(s, OperationType.REMOVE, b)
    assert s == {(2,), (3,)}

    b = Block(0, 5)
    apply_to_tuple_set(s, OperationType.TOGGLE, b)
    assert s == {(0,), (1,), (4,)}

    s = set()

    b = Block((0, 0), (3, 3))
    apply_to_tuple_set(s, OperationType.ADD, b)
    assert s == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }

    b = Block((1, 1), (2, 4))
    apply_to_tuple_set(s, OperationType.REMOVE, b)
    assert s == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
    }

    b = Block((1, 0), (2, 5))
    apply_to_tuple_set(s, OperationType.TOGGLE, b)
    assert s == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 0),
        (2, 1),
        (2, 2),
    }


def test_generate_interval_test_set_1D():
    test_set_2 = generate_interval_test_set_1D(2)
    assert len(test_set_2) == 13
    assert ((0, 1), (0, 1)) in test_set_2

    assert ((0, 1), (0, 2)) in test_set_2
    assert ((0, 2), (0, 1)) in test_set_2
    assert ((0, 1), (1, 2)) in test_set_2
    assert ((1, 2), (0, 1)) in test_set_2
    assert ((0, 2), (1, 2)) in test_set_2
    assert ((1, 2), (0, 2)) in test_set_2

    assert ((0, 1), (2, 3)) in test_set_2
    assert ((2, 3), (0, 1)) in test_set_2
    assert ((0, 2), (1, 3)) in test_set_2
    assert ((1, 3), (0, 2)) in test_set_2
    assert ((0, 3), (1, 2)) in test_set_2
    assert ((1, 2), (0, 3)) in test_set_2

    test_set_3 = generate_interval_test_set_1D(3)
    assert len(test_set_3) == 409

    summary = [0] * 7
    for block_set in test_set_3:
        points_used = {a for a, _ in block_set} | {b for _, b in block_set}
        summary[len(points_used)] += 1

    assert summary == [0, 0, 1, 24, 114, 180, 90]

    # There is an already known sequence on OEIS for the number of different
    # relations between n intervals on a line. https://oeis.org/A055203

    # This takes about l.5s to run and adds no value, left for reference.
    # test_set_4 = generate_interval_test_set_1D(4)
    # assert len(test_set_4) == 23917


def test_generate_interval_patterns():
    assert generate_interval_patterns(0) == {()}
    assert generate_interval_patterns(1) == {(), ((0, 1),)}
    assert generate_interval_patterns(2) == {
        (),
        ((0, 1),),
        ((0, 2),),
        ((1, 2),),
    }
    assert generate_interval_patterns(3) == {
        (),
        ((0, 1),),
        ((0, 2),),
        ((0, 3),),
        ((1, 2),),
        ((1, 3),),
        ((2, 3),),
        ((0, 1), (2, 3)),
    }
    assert len(generate_interval_patterns(4)) == 16


def test_example_use():
    from blocksets import example_use
