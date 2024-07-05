"""Tests for 1 dimensional set operations on the BlockSet class"""

from copy import deepcopy
from math import inf
import pytest

from blocksets.classes.exceptions import (
    DimensionMismatchError,
    ExpectedBlockSetError,
    ValueParsingError,
)


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
