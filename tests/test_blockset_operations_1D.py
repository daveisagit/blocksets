"""Tests for 1 dimensional set operations on the BlockSet class"""

from copy import deepcopy
from math import inf
import pytest

from blocksets.classes.blockset import BlockSet
from blocksets.classes.exceptions import (
    DimensionMismatchError,
    ExpectedBlockSetError,
    ValueParsingError,
)
from block_data import blocksets_1D_all_arrangements_over_4


def test_argument_validation(d1_A, d2_empty):

    with pytest.raises(ExpectedBlockSetError):
        ps = {(1, 3)}
        _ = d1_A.union(ps)

    with pytest.raises(DimensionMismatchError):
        _ = d1_A.union(d2_empty)


def test_union_1D(d1_A, d1_B, d1_AuB, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)

    r1 = d1_A.union(d1_B)
    r2 = d1_B.union(d1_A)
    assert r1 == r2 == d1_AuB

    r3 = d1_A.union(d1_empty)
    assert r3 == d1_A

    assert d1_A | d1_B == d1_AuB

    assert d1_A == copy_A
    assert d1_B == copy_B


def test_intersection_1D(d1_A, d1_B, d1_AnB, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)
    r1 = d1_A.intersection(d1_B)
    r2 = d1_B.intersection(d1_A)
    assert r1 == r2 == d1_AnB

    r3 = d1_A.intersection(d1_empty)
    assert r3 == d1_empty

    assert d1_A & d1_B == d1_AnB

    assert d1_A == copy_A
    assert d1_B == copy_B


def test_difference_1D(d1_A, d1_B, d1_AmB, d1_BmA, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)
    r1 = d1_A.difference(d1_B)
    r2 = d1_B.difference(d1_A)
    assert r1 == d1_AmB
    assert r2 == d1_BmA

    r3 = d1_A.difference(d1_empty)
    assert r3 == d1_A

    assert d1_A - d1_B == d1_AmB

    assert d1_A == copy_A
    assert d1_B == copy_B


def test_symmetric_difference_1D(d1_A, d1_B, d1_AxB, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)
    r1 = d1_A.symmetric_difference(d1_B)
    r2 = d1_B.symmetric_difference(d1_A)
    assert r1 == r2 == d1_AxB

    r3 = d1_A.symmetric_difference(d1_empty)
    assert r3 == d1_A

    assert d1_A ^ d1_B == d1_AxB

    assert d1_A == copy_A
    assert d1_B == copy_B


def test_update_1D(d1_A, d1_B, d1_AuB, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)

    d1_A.update(copy_B)
    d1_B.update(copy_A)
    assert d1_A == d1_B == d1_AuB

    cpy = deepcopy(d1_A)
    d1_A.update(d1_empty)
    assert d1_A == cpy

    copy_A |= copy_B
    assert copy_A == d1_AuB


def test_intersection_update_1D(d1_A, d1_B, d1_AnB, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)

    d1_A.intersection_update(copy_B)
    d1_B.intersection_update(copy_A)
    assert d1_A == d1_A == d1_AnB

    d1_A.intersection_update(d1_empty)
    assert d1_A == d1_empty

    copy_A &= copy_B
    assert copy_A == d1_AnB


def test_difference_update_1D(d1_A, d1_B, d1_AmB, d1_BmA, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)

    d1_A.difference_update(copy_B)
    d1_B.difference_update(copy_A)
    assert d1_A == d1_AmB
    assert d1_B == d1_BmA

    cpy = deepcopy(d1_A)
    d1_A.difference_update(d1_empty)
    assert d1_A == cpy

    copy_A -= copy_B
    assert copy_A == d1_AmB


def test_symmetric_difference_update_1D(d1_A, d1_B, d1_AxB, d1_empty):
    copy_A = deepcopy(d1_A)
    copy_B = deepcopy(d1_B)
    d1_A.symmetric_difference_update(copy_B)
    d1_B.symmetric_difference_update(copy_A)
    assert d1_A == d1_B == d1_AxB

    cpy = deepcopy(d1_A)
    d1_A.symmetric_difference(d1_empty)
    assert d1_A == cpy

    copy_A ^= copy_B
    assert copy_A == d1_AxB


def test_isdisjoint_1D(d1_A, d1_B, d1_C):
    copy_A = deepcopy(d1_A)
    copy_C = deepcopy(d1_C)
    assert d1_A.isdisjoint(d1_C)
    assert d1_C.isdisjoint(d1_A)
    assert d1_A == copy_A
    assert d1_C == copy_C
    assert not d1_A.isdisjoint(d1_B)


def test_issubset_1D(d1_A, d1_C, d1_D):
    copy_C = deepcopy(d1_C)
    copy_D = deepcopy(d1_D)
    assert d1_C.issubset(d1_C)
    assert d1_D.issubset(d1_D)
    assert d1_D.issubset(d1_C)
    assert not d1_C.issubset(d1_A)

    assert d1_D <= d1_C
    assert d1_C <= d1_C
    assert not d1_C <= d1_A

    assert d1_C == copy_C
    assert d1_D == copy_D

    assert d1_D < d1_C
    assert not d1_C < d1_C


def test_issuperset_1D(d1_A, d1_C, d1_D):
    copy_C = deepcopy(d1_C)
    copy_D = deepcopy(d1_D)
    assert d1_C.issuperset(d1_C)
    assert d1_D.issuperset(d1_D)
    assert d1_C.issuperset(d1_D)
    assert not d1_C.issubset(d1_A)

    assert d1_C >= d1_D
    assert d1_C >= d1_C
    assert not d1_C >= d1_A

    assert d1_C == copy_C
    assert d1_D == copy_D

    assert d1_C > d1_D
    assert not d1_C > d1_C


def test_in_operator_1D(
    d1_B, d1_negatives, d1_positives, d1_empty, d2_origin, empty_block_set
):

    with pytest.raises(DimensionMismatchError):
        assert not d2_origin in d1_empty

    with pytest.raises(ValueParsingError):
        assert d1_B in d1_positives

    assert not 1 in d1_empty
    assert not 1 in empty_block_set

    assert 5 in d1_B
    assert 7 not in d1_B
    assert inf not in d1_B
    assert (2, 6) in d1_B
    assert (1, 6) not in d1_B

    assert (1000, 2000) in d1_positives
    assert -5000 in d1_negatives
    assert (5, inf) in d1_positives
    assert (-inf, -5) in d1_negatives

    assert -inf not in d1_positives
    assert inf not in d1_negatives
    assert inf not in d1_positives
    assert -inf not in d1_negatives

    assert 0 not in d1_negatives
    assert 0 not in d1_positives


#
# Here we are testing a group of 16 blocksets which are all the possible
# layouts on a set of 4 intervals and we test each against the other (16x16)
# for all the operations and comparison methods
#


def blockset_ids(blockset):
    """We constructed the blocks so that each case will have a unique number of units"""
    blockset_id = ", ".join(str(b) for b in sorted(blockset, key=lambda x: x.norm))
    blockset_id = " {" + blockset_id + "} "
    blockset_id = f" {blockset.unit_count:03} {blockset_id} "
    return blockset_id


@pytest.mark.parametrize(
    "blockset_a",
    blocksets_1D_all_arrangements_over_4(markers=[-10, -2, 0, 4, 20]),
    ids=blockset_ids,
)
@pytest.mark.parametrize(
    "blockset_b",
    blocksets_1D_all_arrangements_over_4(markers=[-30, -3, 0, 9, 90]),
    ids=blockset_ids,
)
def test_all_patterns_all_operations_1D(blockset_a: BlockSet, blockset_b: BlockSet):
    tuples_a = set(blockset_a.units())
    tuples_b = set(blockset_b.units())

    assert set((blockset_a & blockset_b).units()) == tuples_a & tuples_b
    assert set((blockset_a | blockset_b).units()) == tuples_a | tuples_b
    assert set((blockset_a - blockset_b).units()) == tuples_a - tuples_b
    assert set((blockset_a ^ blockset_b).units()) == tuples_a ^ tuples_b

    assert blockset_a.isdisjoint(blockset_b) == tuples_a.isdisjoint(tuples_b)
    assert blockset_a.issubset(blockset_b) == tuples_a.issubset(tuples_b)
    assert blockset_a.issuperset(blockset_b) == tuples_a.issuperset(tuples_b)

    assert (blockset_a == blockset_b) == (tuples_a == tuples_b)
    assert (blockset_a <= blockset_b) == (tuples_a <= tuples_b)
    assert (blockset_a >= blockset_b) == (tuples_a >= tuples_b)
    assert (blockset_a < blockset_b) == (tuples_a < tuples_b)
    assert (blockset_a > blockset_b) == (tuples_a > tuples_b)

    assert ((0,) in blockset_a) == ((0,) in tuples_a)
    assert blockset_a.unit_count == len(tuples_a)

    copy_blockset_a = deepcopy(blockset_a)
    copy_tuples_a = deepcopy(tuples_a)
    copy_blockset_a &= blockset_b
    copy_tuples_a &= tuples_b
    assert set(copy_blockset_a.units()) == copy_tuples_a
    assert set(blockset_a.units()) == tuples_a
    assert set(blockset_b.units()) == tuples_b

    copy_blockset_a = deepcopy(blockset_a)
    copy_tuples_a = deepcopy(tuples_a)
    copy_blockset_a |= blockset_b
    copy_tuples_a |= tuples_b
    assert set(copy_blockset_a.units()) == copy_tuples_a
    assert set(blockset_a.units()) == tuples_a
    assert set(blockset_b.units()) == tuples_b

    copy_blockset_a = deepcopy(blockset_a)
    copy_tuples_a = deepcopy(tuples_a)
    copy_blockset_a -= blockset_b
    copy_tuples_a -= tuples_b
    assert set(copy_blockset_a.units()) == copy_tuples_a
    assert set(blockset_a.units()) == tuples_a
    assert set(blockset_b.units()) == tuples_b

    copy_blockset_a = deepcopy(blockset_a)
    copy_tuples_a = deepcopy(tuples_a)
    copy_blockset_a ^= blockset_b
    copy_tuples_a ^= tuples_b
    assert set(copy_blockset_a.units()) == copy_tuples_a
    assert set(blockset_a.units()) == tuples_a
    assert set(blockset_b.units()) == tuples_b


def test_set_operations_on_open_intervals(d1_positives, d1_negatives, d1_all, d1_zero):
    s = d1_positives | d1_negatives
    assert len(s) == 2
    assert d1_zero not in s
    s.toggle(d1_all)
    assert set(s) == {d1_zero}
