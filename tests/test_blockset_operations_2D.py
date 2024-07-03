"""Tests for 2 dimensional set operations on the BlockSet class"""

from copy import deepcopy
import pytest

from blocksets.classes.exceptions import DimensionMismatchError, ExpectedBlockSetError


def test_union_2D(d2_A, d2_C, d2_F, d2_empty):
    copy_A = deepcopy(d2_A)
    copy_C = deepcopy(d2_C)

    r1 = d2_A.union(d2_C)
    r2 = d2_C.union(d2_A)
    assert r1 == r2 == d2_F

    r3 = d2_A.union(d2_empty)
    assert r3 == d2_A

    assert d2_A | d2_C == d2_F

    assert d2_A == copy_A
    assert d2_C == copy_C


def test_intersection_2D(d2_B, d2_C, d2_BnC, d2_empty):
    copy_B = deepcopy(d2_B)
    copy_C = deepcopy(d2_C)
    r1 = d2_C.intersection(d2_B)
    r2 = d2_B.intersection(d2_C)
    assert r1 == r2 == d2_BnC

    r3 = d2_B.intersection(d2_empty)
    assert r3 == d2_empty

    assert d2_B & d2_C == d2_BnC

    assert d2_B == copy_B
    assert d2_C == copy_C


def test_difference_2D(d2_A, d2_B, d2_AmB, d2_BnC, d2_empty):
    copy_A = deepcopy(d2_A)
    copy_B = deepcopy(d2_B)
    r1 = d2_A.difference(d2_B)
    r2 = d2_B.difference(d2_A)
    assert r1 == d2_AmB
    assert r2 == d2_BnC

    r3 = d2_A.difference(d2_empty)
    assert r3 == d2_A

    assert d2_A - d2_B == d2_AmB

    assert d2_A == copy_A
    assert d2_B == copy_B


def test_symmetric_difference_2D(d2_A, d2_C, d2_F, d2_empty):
    copy_A = deepcopy(d2_A)
    copy_C = deepcopy(d2_C)
    r1 = d2_A.symmetric_difference(d2_C)
    r2 = d2_C.symmetric_difference(d2_A)
    assert r1 == r2 == d2_F

    r3 = d2_A.symmetric_difference(d2_empty)
    assert r3 == d2_A

    assert d2_A ^ d2_C == d2_F

    assert d2_A == copy_A
    assert d2_C == copy_C


def test_isdisjoint_2D(d2_A, d2_B, d2_C):
    copy_A = deepcopy(d2_A)
    copy_C = deepcopy(d2_C)
    assert d2_A.isdisjoint(d2_C)
    assert d2_C.isdisjoint(d2_A)
    assert d2_A == copy_A
    assert d2_C == copy_C
    assert not d2_A.isdisjoint(d2_B)
