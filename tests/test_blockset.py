"""Tests for the BlockSet class"""

from math import inf
import pytest

from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet, OperationType
from blocksets.classes.exceptions import (
    DimensionMismatchError,
    InvalidDimensionsError,
    NotFiniteError,
)


def test_construction():
    bs = BlockSet()
    assert not bs
    assert bs.dimensions is None
    assert bs.is_normalised == True

    with pytest.raises(InvalidDimensionsError):
        bs = BlockSet("1")

    with pytest.raises(InvalidDimensionsError):
        bs = BlockSet(0)

    bs = BlockSet(2)
    assert not bs
    assert bs.dimensions == 2
    assert set(bs) == set()
    assert bs.is_normalised == True


def test_dimensions():
    bs = BlockSet()
    assert bs.dimensions is None
    blk = Block((1, 1))
    bs.add(blk)
    assert bs.dimensions == 2
    bs.clear()
    assert bs.dimensions is None


def test_empty():
    bs = BlockSet()
    assert bs.is_empty
    assert not bs
    blk = Block((1, 1))
    bs.add(blk)
    assert not bs.is_empty
    assert bs
    bs.toggle(blk)
    assert bs.is_empty

    bs.add(blk)
    bs.add(blk)
    bs.remove(blk)
    assert bs.is_empty
    assert not bs
    assert len(bs) == 0


def test_finite(d1_A):
    bs = BlockSet()
    assert bs.is_finite
    bs.add(Block(5))
    assert bs.is_finite
    bs.add(Block(inf))
    assert not bs.is_finite

    with pytest.raises(NotFiniteError):
        _ = set(bs.units())

    bs &= d1_A
    assert bs.is_finite


def test_add():
    bs = BlockSet()
    blk = Block(1)
    bs.add(blk)
    assert bs._operation_stack[0] == (OperationType.ADD, blk)
    assert bs.is_normalised == False

    blk_2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        bs.add(blk_2)

    blk_2 = Block(3)
    bs.add(blk_2)
    assert bs._operation_stack[1] == (OperationType.ADD, blk_2)
    assert len(bs) == 2
    assert bs.is_normalised == False


def test_clear():
    bs = BlockSet()
    bs.add(Block(1))
    bs.add(Block(2))
    assert len(bs) == 2
    assert bs.is_normalised == False
    bs.clear()
    assert len(bs) == 0
    assert bs.is_normalised == True


def test_remove():
    bs = BlockSet()
    blk = Block(1)
    bs.remove(blk)
    assert bs._operation_stack[0] == (OperationType.REMOVE, blk)
    assert bs.is_normalised == False

    blk_2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        bs.remove(blk_2)

    blk_2 = Block(3)
    bs.remove(blk_2)
    assert bs._operation_stack[1] == (OperationType.REMOVE, blk_2)
    assert len(bs) == 2
    assert bs.is_normalised == False


def test_toggle():
    bs = BlockSet()
    blk = Block(1)
    bs.toggle(blk)
    assert bs._operation_stack[0] == (OperationType.TOGGLE, blk)
    assert bs.is_normalised == False

    blk_2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        bs.toggle(blk_2)

    blk_2 = Block(3)
    bs.toggle(blk_2)
    assert bs._operation_stack[1] == (OperationType.TOGGLE, blk_2)
    assert len(bs) == 2
    assert bs.is_normalised == False


def test_len_after_normalisation():
    bs = BlockSet()
    bs.add(Block(1, 5))
    bs.add(Block(3, 8))
    assert len(bs) == 2
    assert bs.is_normalised == False
    bs.normalise()
    assert len(bs) == 1
    assert bs.is_normalised == True

    bs = BlockSet()
    bs.add(Block((0, 0), (4, 4)))
    bs.add(Block((2, 2), (6, 6)))
    assert len(bs) == 2
    assert bs.is_normalised == False
    bs.normalise()
    assert len(bs) == 3
    assert bs.is_normalised == True


def test_generators():
    bs = BlockSet()
    assert bs.is_normalised == True
    blk = Block(1)
    blk_2 = Block(3)
    bs.add(blk)
    bs.add(blk_2)
    assert bs.is_normalised == False
    assert set(bs) == {blk, blk_2}
    assert bs.is_normalised == True
