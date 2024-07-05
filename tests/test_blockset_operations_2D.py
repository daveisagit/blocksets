"""Tests for 2 dimensional set operations on the BlockSet class"""

from copy import deepcopy
from math import inf
import pytest

from blocksets.classes.exceptions import (
    DimensionMismatchError,
    ExpectedBlockSetError,
    ValueParsingError,
)


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


def test_in_operator_2D(
    d2_A,
    d2_B,
    d2_quad_pp,
    d2_quad_np,
    d2_quad_pn,
    d2_quad_nn,
    d2_empty,
    empty_block_set,
):

    with pytest.raises(DimensionMismatchError):
        assert not 1 in d2_empty

    with pytest.raises(ValueParsingError):
        assert d2_A not in d2_B

    assert ((1, 2), (3, 4)) not in d2_empty
    assert ((1, 2), (3, 4)) not in empty_block_set

    assert ((1, 1), (2, 4)) in d2_B
    assert ((1, 2), (3, 4)) not in d2_B

    assert ((0, 0), (1, 1)) not in d2_quad_pp
    assert ((0, 0), (1, 1)) not in d2_quad_pn
    assert ((0, 0), (1, 1)) not in d2_quad_np
    assert ((0, 0), (1, 1)) not in d2_quad_nn

    assert ((0, -inf), (1, inf)) not in d2_quad_nn
    assert ((0, -inf), (1, inf)) not in d2_quad_pn
    assert ((0, -inf), (1, inf)) not in d2_quad_np
    assert ((0, -inf), (1, inf)) not in d2_quad_nn

    AuB = d2_A | d2_B
    assert ((0, 0), (4, 5)) in AuB
    assert ((2, 2), (5, 4)) not in AuB
