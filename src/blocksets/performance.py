"""How does it perform ?"""

from collections import namedtuple
from itertools import product
import random
from time import time

from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet


DIMENSIONS = 3
GRID_SIZE = 100
BLOCKS = 50
BLOCK_SIDE_RANGE = 0.05, 0.6
SAMPLE_SIZE = 10

Stat = namedtuple(
    "Stat",
    ["step", "method", "id", "time"],
)

METHOD_BLOCK_SET = "BlockSet"
METHOD_TUPLE_SET = "TupleSet"


def random_block(
    dimensions=DIMENSIONS,
    grid_size=GRID_SIZE,
    block_side_range=BLOCK_SIDE_RANGE,
) -> tuple:
    """Return a random block, defined as a tuple pair
    describing the coordinates of the opposite corners/end"""

    min_side = int(block_side_range[0] * grid_size)
    max_side = int(block_side_range[1] * grid_size)
    a = []
    b = []
    for _ in range(dimensions):
        p = random.randint(0, grid_size - min_side)
        l = random.randint(min_side, min(max_side, grid_size - p))
        a.append(p)
        b.append(p + l)

    return tuple(a), tuple(b)


def create_blockset(block_data) -> BlockSet:
    bs = BlockSet()
    for a, b in block_data:
        bs.add(Block(a, b))
    bs.normalise()
    return bs


def generate_tuple_units(a, b):
    dimension_ranges = [range(ord_a, ord_b) for ord_a, ord_b in zip(a, b)]
    for t in product(*dimension_ranges):
        yield t


def create_tuple_set(block_data) -> set:
    """This is slightly faster than building sets of blocks to then update
    e.g. this example is slightly slower
    for a, b in block_data:
        ts.update(set(generate_tuple_units(a, b)))
    """
    ts = set()
    for a, b in block_data:
        for t in generate_tuple_units(a, b):
            ts.add(t)
    return ts


def step_create(sample_size=SAMPLE_SIZE):
    block_sets = []
    tuple_sets = []
    stats = []
    for id in range(sample_size):
        block_data = [random_block() for _ in range(BLOCKS)]

        start = time()
        bs = create_blockset(block_data)
        end = time()
        block_sets.append(bs)
        stats.append(Stat("create", METHOD_BLOCK_SET, id, end - start))

        start = time()
        ts = create_tuple_set(block_data)
        end = time()
        tuple_sets.append(ts)
        stats.append(Stat("create", METHOD_TUPLE_SET, id, end - start))

    return stats, block_sets, tuple_sets


stats, block_sets, tuple_sets = step_create()
av_bs = (
    sum(stat.time for stat in stats if stat.method == METHOD_BLOCK_SET) / SAMPLE_SIZE
)
av_ts = (
    sum(stat.time for stat in stats if stat.method == METHOD_TUPLE_SET) / SAMPLE_SIZE
)
print(av_bs, av_ts)
