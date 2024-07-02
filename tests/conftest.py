"""Fixtures"""

import pytest
from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet

#
# 1 - Dimensional Block Set Fixtures
#


"""
A    ----      ------
B      ----  ----  ----

AuB  ------  ----------
AnB    --      --  -- 
A-B  --          --
B-A      --  --      --
AxB  --  --  --  --  -- (symmetric difference i.e. xor)
"""


@pytest.fixture()
def d1_empty():
    bs = BlockSet(1)
    assert bs.empty
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


#
# 2 - Dimensional Block Set Fixtures
#


@pytest.fixture()
def d2_empty():
    bs = BlockSet(2)
    assert bs.empty
    return bs
