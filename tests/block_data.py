"""
Block arrangements for tests and fixtures
"""

from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet
from util import (
    generate_interval_patterns,
    generate_interval_test_set_1D,
    marker_to_ordinate,
    multiple_of_tuple,
)


def blocks_1D_arbitrary_set_1():
    """
    ----
            ----
                    ----
        ----
          ----
              --------
      --------------
    """
    blocks = []
    blocks.append(Block(0, 4))
    blocks.append(Block(8, 12))
    blocks.append(Block(16, 20))
    blocks.append(Block(4, 8))
    blocks.append(Block(6, 10))
    blocks.append(Block(10, 18))
    blocks.append(Block(2, 16))
    return blocks


def blocks_1D_all_arrangements_of_2(scale=5, points=[4, 7, 12, 16]):
    """Using the points for start/end generate all possible pairs of intervals"""
    arrangements = []
    for test_set in generate_interval_test_set_1D(2):
        if points:
            arrangements.append([Block(points[a], points[b]) for a, b in test_set])
            continue
        arrangements.append([Block(a * scale, b * scale) for a, b in test_set])
    return arrangements


def blocks_1D_all_arrangements_of_3(scale=5):
    """Generate all possible arrangements of 3 intervals over markers 0,5,10,15,...."""
    arrangements = []
    for test_set in generate_interval_test_set_1D(3):
        arrangements.append([Block(a * scale, b * scale) for a, b in test_set])
    return arrangements


def blocks_2D_arbitrary_set_example():
    """4 arbitrary rectangles"""
    blocks = []
    blocks.append(Block((-8, 11), (-3, 15)))
    blocks.append(Block((-5, 8), (1, 16)))
    blocks.append(Block((-1, 2), (6, 18)))
    blocks.append(Block((-9, 6), (8, 9)))
    return blocks


def blocks_2D_all_arrangements_of_2(scale=5):
    """Generate all possible arrangements of a pair of rectangles"""
    arrangements = []
    interval_pairs = generate_interval_test_set_1D(2)
    for x_pair in interval_pairs:
        for y_pair in interval_pairs:

            a = (x_pair[0][0], y_pair[0][0])
            b = (x_pair[0][1], y_pair[0][1])
            a = multiple_of_tuple(a, scale)
            b = multiple_of_tuple(b, scale)
            r1 = Block(a, b)

            a = (x_pair[1][0], y_pair[1][0])
            b = (x_pair[1][1], y_pair[1][1])
            a = multiple_of_tuple(a, scale)
            b = multiple_of_tuple(b, scale)
            r2 = Block(a, b)
            arrangements.append([r1, r2])

    return arrangements


def blocks_3D_all_arrangements_of_2(scale=5, markers=None):
    """Generate all possible arrangements of a pair of cuboids"""
    arrangements = []
    interval_pairs = generate_interval_test_set_1D(2)
    for x_pair in interval_pairs:
        for y_pair in interval_pairs:
            for z_pair in interval_pairs:

                a = (x_pair[0][0], y_pair[0][0], z_pair[0][0])
                b = (x_pair[0][1], y_pair[0][1], z_pair[0][1])
                a = multiple_of_tuple(a, scale)
                b = multiple_of_tuple(b, scale)
                r1 = Block(a, b)

                a = (x_pair[1][0], y_pair[1][0], z_pair[1][0])
                b = (x_pair[1][1], y_pair[1][1], z_pair[1][1])
                a = multiple_of_tuple(a, scale)
                b = multiple_of_tuple(b, scale)
                r2 = Block(a, b)
                arrangements.append([r1, r2])

    return arrangements


def blocksets_1D_all_arrangements_over_4(markers=None):
    """Generate all possible patterns of 4 intervals over the given point markers"""
    patterns = sorted(generate_interval_patterns(4))
    blocksets = []
    for marker_set in patterns:
        bs = BlockSet(1)
        for a, b in marker_set:
            bs.add(
                Block(
                    marker_to_ordinate(a, markers=markers),
                    marker_to_ordinate(b, markers=markers),
                )
            )
        bs.normalise()
        blocksets.append(bs)

    return blocksets


def blocksets_2D_all_arrangements_over_2x2(scale=5, markers=None):
    """Generate all possible patterns of 2x2 intervals over the given point markers"""
    patterns = sorted(generate_interval_patterns(2))
    blocksets = []
    for marker_set_0 in patterns:
        for marker_set_1 in patterns:
            bs = BlockSet(2)
            for a, b in marker_set_0:
                bs.add(
                    Block(
                        (
                            marker_to_ordinate(0, markers=markers[0]),
                            marker_to_ordinate(a, markers=markers[1]),
                        ),
                        (
                            marker_to_ordinate(1, markers=markers[0]),
                            marker_to_ordinate(b, markers=markers[1]),
                        ),
                    )
                )
            for a, b in marker_set_1:
                bs.add(
                    Block(
                        (
                            marker_to_ordinate(1, markers=markers[0]),
                            marker_to_ordinate(a, markers=markers[1]),
                        ),
                        (
                            marker_to_ordinate(2, markers=markers[0]),
                            marker_to_ordinate(b, markers=markers[1]),
                        ),
                    )
                )

            bs.normalise()
            blocksets.append(bs)

    return sorted(blocksets, key=lambda x: x.unit_count)
