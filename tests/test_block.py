"""Tests for the Block class"""

from copy import copy

import pytest

from math import inf
from blocksets.classes.block import Block
from blocksets.classes.exceptions import (
    BlockError,
    DimensionMismatchError,
    NotAUnitError,
    NotFiniteError,
    ValueParsingError,
    ZeroSpaceError,
)


def test_exceptions():
    with pytest.raises(BlockError):
        raise BlockError("A specific unexpected error in Block class")


def test_standard_object():
    """Test standard object behaviour equality and identity"""
    blk = Block(4)
    assert blk
    blk_2 = copy(blk)
    assert blk is not blk_2
    assert id(blk) != id(blk_2)
    assert blk == blk_2
    assert blk_2.is_a_unit

    blk = Block(-1, 3)
    blk_2 = copy(blk)
    assert blk is not blk_2
    assert id(blk) != id(blk_2)
    assert blk == blk_2
    assert not blk_2.is_a_unit


def test_raise_parsing_error():
    """Test we raise errors for unexpected arguments"""
    with pytest.raises(TypeError):
        blk = Block()

    with pytest.raises(ValueParsingError):
        blk = Block(None)

    with pytest.raises(ValueParsingError):
        blk = Block("1")

    with pytest.raises(ValueParsingError):
        blk = Block(1.2)

    with pytest.raises(ValueParsingError):
        blk = Block((1.2,))

    with pytest.raises(ValueParsingError):
        blk = Block((1, 1.2))

    with pytest.raises(ValueParsingError):
        blk = Block((1, None))

    with pytest.raises(ValueParsingError):
        blk = Block((1, 2), (1, 1.2))

    with pytest.raises(ValueParsingError):
        blk = Block((1, 2), (1, None))

    with pytest.raises(ValueParsingError):
        blk = Block((1, 1.2), (1, 1.4))

    with pytest.raises(ValueParsingError):
        blk = Block((1, inf), (1, 1.4))

    with pytest.raises(ValueParsingError):
        blk = Block((1, None), (2, inf))


def test_raise_zero_space_error():
    """Test we raise errors for arguments defining empty space"""

    # 1 Dimension
    with pytest.raises(ZeroSpaceError):
        blk = Block((1,), (1,))

    with pytest.raises(ZeroSpaceError):
        blk = Block((inf,), (inf,))

    with pytest.raises(ZeroSpaceError):
        blk = Block((-inf,), (-inf,))

    # 2 Dimensions
    with pytest.raises(ZeroSpaceError):
        blk = Block((1, 2), (1, 3))

    with pytest.raises(ZeroSpaceError):
        blk = Block((1, 3), (-1, 3))

    with pytest.raises(ZeroSpaceError):
        blk = Block((1, inf), (2, inf))

    with pytest.raises(ZeroSpaceError):
        blk = Block((1, -inf), (2, -inf))

    with pytest.raises(ZeroSpaceError):
        blk = Block((-inf, 2), (-inf, 3))


def test_raise_dimension_mismatch():
    """Test we raise errors for arguments of differing dimension"""

    with pytest.raises(DimensionMismatchError):
        blk = Block((1, 2), (1, 2, 3))

    with pytest.raises(DimensionMismatchError):
        blk = Block((1, 2), (2, inf, 3))


def test_parsing():
    """Test we parse correctly"""

    # assume a unit from non-sequence argument
    b = Block.parse(1)
    assert b.is_a_unit
    assert b.dimensions == 1
    assert b == ((1,), (2,))

    # assume a unit from sequence > 2
    b = Block.parse([1, 6, 4])
    assert b.is_a_unit
    assert b.dimensions == 3
    assert b == ((1, 6, 4), (2, 7, 5))

    # assume a unit from sequence of one item - 2D
    b = Block.parse(((1, 6),))
    assert b.is_a_unit
    assert b.dimensions == 2
    assert b == ((1, 6), (2, 7))

    # assume a unit from sequence of one item - 3D
    b = Block.parse(((1, 6, 4),))
    assert b.is_a_unit
    assert b.dimensions == 3
    assert b == ((1, 6, 4), (2, 7, 5))

    # check zero length sequence raise TypeError
    with pytest.raises(TypeError):
        b = Block.parse([])

    # assume seq of 2 are the end/corner arguments
    b = Block.parse([1, 6])
    assert b.dimensions == 1
    assert b.measure == 5

    # assume seq of 2 are the end/corner arguments
    b = Block.parse([[1], [6]])
    assert b.dimensions == 1
    assert b.measure == 5

    # assume seq of 2 are the end/corner arguments
    b = Block.parse([[1, 8], [6, 4]])
    assert b.dimensions == 2
    assert b == ((1, 4), (6, 8))

    # check dimension matching
    b = Block.parse_to_dimension(1, 2)
    with pytest.raises(DimensionMismatchError):
        b = Block.parse_to_dimension(2, 2)

    # exceptions raised
    with pytest.raises(ZeroSpaceError):
        b = Block.parse([[1, 4], [1, 5]])

    with pytest.raises(ValueParsingError):
        b = Block.parse("block")


def test_instantiation_1D():
    """Test 1 dimensional instantiation"""
    blk = Block(1)
    assert blk == ((1,), (2,))
    assert blk.a == (1,)
    assert blk.b == (2,)
    assert str(blk) == "1"
    assert blk.is_a_unit
    assert blk.dimensions == 1
    assert blk.is_finite
    assert blk.side_lengths == (1,)
    assert blk.measure == 1
    assert blk.manhattan == 1
    assert blk != 2

    blk = Block(inf)
    assert blk == ((-inf,), (inf,))
    assert blk.a == (-inf,)
    assert blk.b == (inf,)
    assert str(blk) == "-inf..inf"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(-inf)
    assert blk == ((-inf,), (inf,))
    assert blk.a == (-inf,)
    assert blk.b == (inf,)
    assert str(blk) == "-inf..inf"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    assert Block(-inf) == Block(inf)

    blk = Block(1, inf)
    assert blk == ((1,), (inf,))
    assert blk.a == (1,)
    assert blk.b == (inf,)
    assert str(blk) == "1..inf"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(1, -inf)
    assert blk == ((-inf,), (1,))
    assert blk.a == (-inf,)
    assert blk.b == (1,)
    assert str(blk) == "-inf..1"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(-2, -inf)
    assert blk == ((-inf,), (-2,))
    assert blk.a == (-inf,)
    assert blk.b == (-2,)
    assert str(blk) == "-inf..-2"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(-inf, inf)
    assert blk == ((-inf,), (inf,))
    assert blk.a == (-inf,)
    assert blk.b == (inf,)
    assert str(blk) == "-inf..inf"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(inf, -inf)
    assert blk == ((-inf,), (inf,))
    assert blk.a == (-inf,)
    assert blk.b == (inf,)
    assert str(blk) == "-inf..inf"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert not blk.is_finite
    assert blk.side_lengths == (inf,)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(2, 3)
    assert blk == ((2,), (3,))
    assert blk.a == (2,)
    assert blk.b == (3,)
    assert str(blk) == "2"
    assert blk.is_a_unit
    assert blk.dimensions == 1
    assert blk.is_finite
    assert blk.side_lengths == (1,)
    assert blk.measure == 1
    assert blk.manhattan == 1

    blk = Block(3, 2)
    assert blk == ((2,), (3,))
    assert blk.a == (2,)
    assert blk.b == (3,)
    assert str(blk) == "2"
    assert blk.is_a_unit
    assert blk.dimensions == 1
    assert blk.is_finite
    assert blk.side_lengths == (1,)
    assert blk.measure == 1
    assert blk.manhattan == 1

    blk = Block(-5, 5)
    assert blk == ((-5,), (5,))
    assert blk.a == (-5,)
    assert blk.b == (5,)
    assert str(blk) == "-5..5"
    assert not blk.is_a_unit
    assert blk.dimensions == 1
    assert blk.is_finite
    assert blk.side_lengths == (10,)
    assert blk.measure == 10
    assert blk.manhattan == 10
    assert repr(blk) == "((-5,), (5,))"


def test_instantiation_2D():
    """Test 2 dimensional instantiation"""

    a = (-1, 3)
    b = (4, 2)
    c = (inf, 5)  # line y=5
    d = (6, -inf)  # line x=6

    blk = Block(a)
    assert blk == ((-1, 3), (0, 4))
    assert str(blk) == "(-1, 3)"
    assert blk.is_a_unit
    assert blk.dimensions == 2
    assert blk.is_finite
    assert blk.side_lengths == (1, 1)
    assert blk.measure == 1
    assert blk.manhattan == 2

    blk = Block(b)
    assert blk == ((4, 2), (5, 3))
    assert str(blk) == "(4, 2)"
    assert blk.is_a_unit
    assert blk.dimensions == 2
    assert blk.is_finite
    assert blk.side_lengths == (1, 1)
    assert blk.measure == 1
    assert blk.manhattan == 2

    blk = Block(c)
    assert blk == ((-inf, 5), (inf, 6))
    assert str(blk) == "(-inf, 5)..(inf, 6)"
    assert not blk.is_a_unit
    assert blk.dimensions == 2
    assert not blk.is_finite
    assert blk.side_lengths == (inf, 1)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(d)
    assert blk == ((6, -inf), (7, inf))
    assert str(blk) == "(6, -inf)..(7, inf)"
    assert not blk.is_a_unit
    assert blk.dimensions == 2
    assert not blk.is_finite
    assert blk.side_lengths == (1, inf)
    assert blk.measure == inf
    assert blk.manhattan == inf

    assert Block(a) != Block(b) != Block(c) != Block(d)
    assert Block(a, c) != Block(a, d)

    assert Block(a, b) == Block(b, a)
    assert Block(c, d) == Block(d, c)
    assert Block(a, d) == Block(d, a)
    assert Block(a, c) == Block(c, a)

    blk = Block(a, b)
    assert blk == ((-1, 2), (4, 3))
    assert str(blk) == "(-1, 2)..(4, 3)"
    assert not blk.is_a_unit
    assert blk.dimensions == 2
    assert blk.is_finite
    assert blk.side_lengths == (5, 1)
    assert blk.measure == 5
    assert blk.manhattan == 6

    blk = Block(c, b)
    assert blk == ((4, 2), (inf, 5))
    assert str(blk) == "(4, 2)..(inf, 5)"
    assert not blk.is_a_unit
    assert blk.dimensions == 2
    assert not blk.is_finite
    assert blk.side_lengths == (inf, 3)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(d, b)
    assert blk == ((4, -inf), (6, 2))
    assert str(blk) == "(4, -inf)..(6, 2)"
    assert not blk.is_a_unit
    assert blk.dimensions == 2
    assert not blk.is_finite
    assert blk.side_lengths == (2, inf)
    assert blk.measure == inf
    assert blk.manhattan == inf

    blk = Block(c, d)
    assert blk == ((6, -inf), (inf, 5))
    assert str(blk) == "(6, -inf)..(inf, 5)"
    assert not blk.is_a_unit
    assert blk.dimensions == 2
    assert not blk.is_finite
    assert blk.side_lengths == (inf, inf)
    assert blk.measure == inf
    assert blk.manhattan == inf


def test_intersection_1D():
    b1 = Block(1)
    b2 = Block(1)
    assert b1 & b2 == b1 == b2
    assert b1 & 1 == b1
    assert b1 @ b2

    b2 = Block(2)
    assert b1 & b2 is None

    b2 = Block(-1, 5)
    assert b1 @ b2
    assert b1 & b2 == b1 != b2

    b2 = Block(inf)
    assert b1 & b2 == b1 != b2

    b1 = Block(-inf)
    b2 = Block(inf)
    assert b1 == b2
    assert b1 & b2 == b1 == b2

    b1 = Block(4, 10)
    b2 = Block(inf)
    assert b1 & b2 == b1 != b2
    b2 = Block(-inf, 8)
    assert b1 & b2 == Block(4, 8)
    b2 = Block((2,), (8,))
    assert b1 & b2 == Block(4, 8)
    b2 = Block(8, inf)
    assert b1 & b2 == Block(8, 10)
    b2 = Block(8, 20)
    assert b1 & b2 == Block(8, 10)

    b2 = Block(2, 20)
    assert b1 & b2 == b1

    b1 = Block(-inf, 0)
    b2 = Block(inf, 0)
    assert b1 & b2 is None

    b1 = Block(-inf, 1)
    b2 = Block(inf, -1)
    assert b1 & b2 == Block(-1, 1)

    b1 = Block(1)
    b2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        assert b1 & b2 is None


def test_intersection_2D():
    """Test intersection operator in 2 dimensions"""
    core = Block((-10, -10), (11, 11))
    inner = Block((-2, -2), (2, 2))
    outer = Block((-18, -18), (18, 18))
    all = Block((-inf, -inf), (inf, inf))

    assert core & core == core
    assert core & inner == inner
    assert inner & core == inner
    assert core & outer == core
    assert outer & core == core

    assert all & all == all
    assert outer & all == outer
    assert inner & all == inner

    v_strip = Block((-5, -inf), (5, inf))
    assert core & v_strip == ((-5, -10), (5, 11))
    assert v_strip & core == ((-5, -10), (5, 11))
    assert v_strip & inner == inner
    assert inner & v_strip == inner

    h_strip = Block((-inf, -5), (inf, 5))
    assert core & h_strip == ((-10, -5), (11, 5))
    assert h_strip & core == ((-10, -5), (11, 5))
    assert h_strip & inner == inner
    assert inner & h_strip == inner

    assert v_strip & h_strip == ((-5, -5), (5, 5))
    assert h_strip & v_strip == ((-5, -5), (5, 5))

    offset = Block((-5, -5), (16, 16))
    assert core & offset == ((-5, -5), (11, 11))

    offset = Block((-25, 2), (25, 20))
    assert core & offset == ((-10, 2), (11, 11))

    offset = Block((-25, 2), (25, 4))
    assert core & offset == ((-10, 2), (11, 4))

    disjoint = Block((100, 100), (110, 110))
    assert core & disjoint is None

    disjoint = Block((-inf, 12), (inf, 14))
    assert core & disjoint is None

    disjoint = Block((-inf, -14), (inf, -12))
    assert core & disjoint is None

    h_strip_1 = Block((-inf, -5), (inf, 5))
    h_strip_2 = Block((-inf, -1), (inf, 7))
    assert h_strip_1 & h_strip_2 == ((-inf, -1), (inf, 5))
    h_strip_2 = Block((-inf, -8), (inf, 0))
    assert h_strip_1 & h_strip_2 == ((-inf, -5), (inf, 0))


def test_in_contact_with_1D():
    b1 = Block(1)
    b2 = Block(2)
    b3 = Block(3)
    assert b1 @ b2
    assert not b1 @ b3
    assert Block(-5, 1) @ b1
    assert b1 @ Block(-5, 1)

    b2 = Block((3, 4))
    with pytest.raises(DimensionMismatchError):
        assert b1 & b2 is None


def test_in_contact_with_2D():
    b11 = Block((1, 1))
    b12 = Block((1, 2))
    b13 = Block((1, 3))
    b22 = Block((2, 2))
    b31 = Block((3, 1))
    b33 = Block((3, 3))
    assert b11 @ b12
    assert b11 @ b22
    assert b13 @ b22
    assert b31 @ b22
    assert not b11 @ b33
    assert not b11 @ b13

    core = Block((-10, -10), (11, 11))
    offset = Block((-5, -5), (16, 16))
    inner = Block((-2, -2), (2, 2))
    all = Block((-inf, -inf), (inf, inf))

    assert core @ offset
    assert all @ core
    assert core @ inner


def test_subsets_1D():
    """Test subsets in 1 dimension"""
    b1 = Block(1)
    b2 = Block(1)
    assert b1 <= b2
    assert b1 >= b2
    assert b1 in b2
    assert b2 in b1
    assert not b1 < b2
    assert not b1 > b2

    b1 = Block(-inf)
    b2 = Block(inf)
    assert b1 <= b2
    assert b1 >= b2

    b1 = Block(1, 10)
    b2 = Block(1, 10)
    assert b1 <= b2
    assert b1 >= b2

    b2 = Block(1, inf)
    assert b1 <= b2
    assert not b2 <= b1
    assert not b1 >= b2
    assert b2 >= b1
    assert b2 > b1

    b2 = Block(1, 11)
    assert b1 <= b2
    assert not b1 >= b2
    assert not b1 >= b2
    assert b2 >= b1
    assert b2 > b1

    b2 = Block(0, 10)
    assert b1 <= b2
    assert not b1 >= b2
    assert not b1 >= b2
    assert b2 >= b1
    assert b2 > b1

    b2 = Block(-3, 12)
    assert b1 <= b2
    assert not b1 >= b2
    assert not b1 >= b2
    assert b2 >= b1
    assert b2 > b1

    b2 = Block(-inf, 10)
    assert b1 <= b2
    assert not b1 >= b2
    assert not b1 >= b2
    assert b2 >= b1
    assert b2 > b1

    b2 = Block(2, 11)
    assert not b1 <= b2
    assert not b1 >= b2


def test_subsets_2D():
    """Test subsets in 2 dimensions"""
    core = Block((-10, -10), (11, 11))
    close = Block((-10, -10), (10, 10))
    inner = Block((-2, -2), (2, 2))
    outer = Block((-18, -18), (18, 18))
    all = Block((-inf, -inf), (inf, inf))
    v_strip = Block((-5, -inf), (5, inf))
    h_strip = Block((-inf, -5), (inf, 5))
    offset = Block((-5, -5), (16, 16))
    disjoint = Block((1000, 1000), (1005, 1005))

    assert core >= core
    assert core <= core
    assert not core > core
    assert not core < core
    assert all >= all
    assert all <= all
    assert not all > all
    assert not all < all

    assert inner <= core
    assert inner < core
    assert not inner >= core
    assert not inner > core
    assert not core <= inner
    assert not core < inner
    assert core >= inner
    assert core > inner
    assert core >= close
    assert core > close

    assert outer <= all
    assert not outer >= all
    assert not all <= outer
    assert all >= outer

    assert all >= outer >= core >= inner
    assert inner <= core <= outer <= all

    assert v_strip <= all
    assert all >= v_strip

    assert not offset <= core
    assert not core <= offset
    assert not offset >= core
    assert not core >= offset

    assert not v_strip <= h_strip
    assert not h_strip <= v_strip
    assert not v_strip >= h_strip
    assert not h_strip >= v_strip

    assert inner < core < outer
    assert outer > core > inner

    assert not core >= disjoint
    assert not disjoint >= core


def test_contains_operator():

    # 1 dimension
    b1 = Block(1, 10)
    b2 = Block(2, 11)
    with pytest.raises(NotAUnitError):
        assert b1 in b2

    assert 6 in b2
    assert 13 not in b2

    # 2 dimensions
    core = Block((-10, -10), (11, 11))
    inner = Block((-2, -2), (2, 2))
    with pytest.raises(NotAUnitError):
        assert core in core

    assert (0, 0) in core
    assert (1000, 1000) not in core

    with pytest.raises(DimensionMismatchError):
        assert 0 in core


def test_iterator():
    b1 = Block(3, 7)
    assert set(b1) == {(3,), (4,), (5,), (6,)}
    b2 = Block((3, 7), (5, 8))
    assert set(b2) == {(3, 7), (4, 7)}
    b3 = Block((0, 0, 0), (3, 4, 5))
    assert len(set(b3)) == b3.measure == len(b3)
    b3 = Block((1, 1, 1), (3, 4, 5))
    assert len(set(b3)) == 24 == len(b3)

    bi = Block(inf)
    with pytest.raises(NotFiniteError):
        assert len(set(bi)) == 0

    assert len(set((bi & b1))) == b1.measure

    with pytest.raises(DimensionMismatchError):
        assert len(set((bi & b3))) == b3.measure
