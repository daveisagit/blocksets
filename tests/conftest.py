"""Fixtures"""

from math import inf
import pytest
from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet


@pytest.fixture()
def empty_block_set():
    bs = BlockSet()
    assert bs.is_empty
    return bs


#
# 1 - Dimensional Block Set Fixtures
#


"""
A    ----      ------
B      ----  ----  ----
C         -----      ---       
D         ----        --

AuB  ------  ----------
AnB    --      --  -- 
A-B  --          --
B-A      --  --      --
AxB  --  --  --  --  -- (symmetric difference i.e. xor)

"""


@pytest.fixture()
def d1_empty():
    bs = BlockSet(1)
    assert bs.is_empty
    return bs


@pytest.fixture()
def d1_A():
    bs = BlockSet(1)
    bs.add(Block(0, 16))
    bs.remove(Block(4, 10))
    return bs


@pytest.fixture()
def d1_B():
    bs = BlockSet(1)
    bs.add(Block(2, 18))
    bs.remove(Block(6, 8))
    bs.remove(Block(12, 14))
    return bs


@pytest.fixture()
def d1_C():
    bs = BlockSet(1)
    bs.add(Block(5, 10))
    bs.add(Block(16, 19))
    return bs


@pytest.fixture()
def d1_D():
    bs = BlockSet(1)
    bs.add(Block(5, 9))
    bs.add(Block(17, 19))
    return bs


@pytest.fixture()
def d1_AuB():
    bs = BlockSet(1)
    bs.add(Block(0, 18))
    bs.remove(Block(6, 8))
    bs.normalise()
    return bs


@pytest.fixture()
def d1_AnB():
    bs = BlockSet(1)
    bs.add(Block(2, 4))
    bs.add(Block(10, 12))
    bs.add(Block(14, 16))
    bs.normalise()
    return bs


@pytest.fixture()
def d1_AmB():
    bs = BlockSet(1)
    bs.add(Block(0, 2))
    bs.add(Block(12, 14))
    bs.normalise()
    return bs


@pytest.fixture()
def d1_BmA():
    bs = BlockSet(1)
    bs.add(Block(4, 6))
    bs.add(Block(8, 10))
    bs.add(Block(16, 18))
    bs.normalise()
    return bs


@pytest.fixture()
def d1_AxB():
    bs = BlockSet(1)
    bs.add(Block(0, 2))
    bs.add(Block(4, 6))
    bs.add(Block(8, 10))
    bs.add(Block(12, 14))
    bs.add(Block(16, 18))
    bs.normalise()
    return bs


@pytest.fixture()
def d1_negatives():
    bs = BlockSet(1)
    bs.add(Block(-inf, 0))
    return bs


@pytest.fixture()
def d1_positives():
    bs = BlockSet(1)
    bs.add(Block(1, inf))
    return bs


@pytest.fixture()
def d1_all():
    return Block(inf)


@pytest.fixture()
def d1_zero():
    return Block(0)


#
# 2 - Dimensional Block Set Fixtures
#


@pytest.fixture()
def d2_empty():
    bs = BlockSet(2)
    assert bs.is_empty
    return bs


"""
Various patterns over 10 x 5

A                B             C 
---------------------------------------------------------
xxxxxxxxxx       xxxxxxxxxx
xxxxxxxxxx       xxxxxxxxxx
  xx  xx         xx            xx  xx  xx
  xx  xx         xx            xx  xx  xx
  xx  xx         xx            xx  xx  xx

F = Full (10x5) fill

AuC = F
BnC = (0,0)..(2,3)
A-B = (2,0)..(4,3) & (6,0)..(8,3)
B-A = (0,0)..(2,3) = BnC
AxC = F

"""


@pytest.fixture()
def d2_A():
    bs = BlockSet(2)
    bs.add(Block((0, 3), (10, 5)))
    bs.add(Block((2, 0), (4, 5)))
    bs.add(Block((6, 0), (8, 5)))
    return bs


@pytest.fixture()
def d2_B():
    bs = BlockSet(2)
    bs.add(Block((0, 0), (10, 5)))
    bs.remove(Block((2, 0), (10, 3)))
    return bs


@pytest.fixture()
def d2_C():
    bs = BlockSet(2)
    bs.add(Block((0, 0), (2, 3)))
    bs.add(Block((4, 0), (6, 3)))
    bs.add(Block((8, 0), (10, 3)))
    return bs


@pytest.fixture()
def d2_F():
    bs = BlockSet(2)
    bs.add(Block((0, 0), (10, 5)))
    return bs


@pytest.fixture()
def d2_BnC():
    bs = BlockSet(2)
    bs.add(Block((0, 0), (2, 3)))
    return bs


@pytest.fixture()
def d2_AmB():
    bs = BlockSet(2)
    bs.add(Block((2, 0), (4, 3)))
    bs.add(Block((6, 0), (8, 3)))
    return bs


# 4 quadrants excluding zeros (i.e. the axes)


@pytest.fixture()
def d2_quad_pp():
    bs = BlockSet(2)
    bs.add(Block((1, 1), (inf, inf)))
    return bs


@pytest.fixture()
def d2_quad_np():
    bs = BlockSet(2)
    bs.add(Block((-inf, 1), (0, inf)))
    return bs


@pytest.fixture()
def d2_quad_nn():
    bs = BlockSet(2)
    bs.add(Block((-inf, -inf), (0, 0)))
    return bs


@pytest.fixture()
def d2_quad_pn():
    bs = BlockSet(2)
    bs.add(Block((1, -inf), (inf, 0)))
    return bs


@pytest.fixture()
def d2_origin():
    return Block((0, 0))
