"""Tests for the BlockSet class with a focus on the set operations"""

from copy import deepcopy
import pytest

from blocksets.classes.exceptions import DimensionMismatchError, ExpectedBlockSetError


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
