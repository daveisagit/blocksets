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

    return sorted(blocksets, key=lambda x: x.measure)


def d2_random_blocksets():
    """4 random blocks sets covering 100x100 space"""
    random_list = [
        [
            [[0, 37], [14, 92]],
            [[94, 32], [98, 63]],
            [[56, 77], [65, 100]],
            [[43, 32], [56, 63]],
            [[14, 37], [41, 92]],
            [[56, 32], [65, 67]],
            [[72, 32], [88, 63]],
            [[56, 2], [65, 30]],
            [[65, 77], [72, 100]],
            [[14, 2], [41, 30]],
            [[41, 32], [43, 92]],
            [[72, 77], [88, 100]],
            [[98, 32], [99, 63]],
            [[41, 2], [43, 30]],
            [[43, 2], [56, 30]],
            [[94, 77], [98, 100]],
            [[88, 77], [94, 100]],
            [[43, 77], [56, 100]],
            [[65, 32], [72, 67]],
            [[88, 8], [94, 63]],
        ],
        [
            [[46, 23], [49, 35]],
            [[42, 59], [46, 69]],
            [[84, 59], [91, 69]],
            [[40, 74], [42, 97]],
            [[49, 23], [54, 35]],
            [[54, 23], [64, 35]],
            [[64, 59], [66, 69]],
            [[49, 59], [54, 69]],
            [[54, 59], [64, 69]],
            [[66, 16], [68, 69]],
            [[54, 75], [64, 100]],
            [[84, 75], [91, 97]],
            [[68, 16], [84, 69]],
            [[91, 75], [97, 97]],
            [[64, 75], [66, 100]],
            [[46, 59], [49, 69]],
            [[42, 23], [46, 35]],
            [[40, 59], [42, 69]],
            [[42, 74], [46, 97]],
            [[49, 76], [54, 100]],
            [[66, 75], [68, 100]],
            [[24, 5], [40, 54]],
            [[24, 74], [40, 97]],
            [[40, 5], [42, 54]],
            [[11, 5], [24, 54]],
            [[46, 95], [49, 100]],
            [[97, 75], [99, 95]],
            [[68, 75], [84, 97]],
        ],
        [
            [[93, 91], [98, 96]],
            [[69, 91], [81, 96]],
            [[27, 83], [28, 97]],
            [[5, 47], [7, 76]],
            [[35, 35], [53, 45]],
            [[87, 5], [89, 33]],
            [[89, 91], [93, 96]],
            [[86, 5], [87, 33]],
            [[87, 42], [89, 88]],
            [[89, 60], [93, 88]],
            [[86, 91], [87, 96]],
            [[16, 83], [23, 97]],
            [[60, 5], [69, 33]],
            [[7, 26], [16, 76]],
            [[81, 42], [86, 65]],
            [[28, 35], [35, 45]],
            [[16, 26], [23, 76]],
            [[23, 83], [27, 97]],
            [[87, 91], [89, 96]],
            [[81, 5], [86, 33]],
            [[28, 83], [35, 97]],
            [[69, 2], [81, 33]],
            [[23, 47], [27, 76]],
            [[93, 5], [98, 33]],
            [[86, 42], [87, 67]],
            [[89, 5], [93, 33]],
            [[81, 91], [86, 96]],
            [[69, 42], [81, 65]],
            [[60, 91], [69, 96]],
            [[93, 62], [98, 67]],
        ],
        [
            [[85, 73], [91, 84]],
            [[25, 23], [43, 29]],
            [[82, 73], [85, 84]],
            [[67, 27], [73, 68]],
            [[52, 44], [57, 73]],
            [[4, 33], [24, 89]],
            [[43, 81], [47, 97]],
            [[25, 33], [43, 97]],
            [[24, 23], [25, 29]],
            [[80, 81], [81, 97]],
            [[48, 23], [52, 29]],
            [[48, 44], [52, 73]],
            [[67, 81], [73, 97]],
            [[57, 81], [67, 97]],
            [[73, 44], [80, 68]],
            [[91, 73], [98, 84]],
            [[47, 81], [48, 97]],
            [[52, 81], [57, 97]],
            [[48, 81], [52, 97]],
            [[43, 23], [47, 29]],
            [[47, 23], [48, 29]],
            [[85, 30], [91, 54]],
            [[73, 81], [80, 97]],
            [[47, 66], [48, 73]],
            [[24, 33], [25, 89]],
            [[57, 44], [67, 68]],
        ],
    ]

    blocksets = []
    for lst in random_list:
        bs = BlockSet(2)
        for blk_coordinates in lst:
            blk = Block.parse(blk_coordinates)
            bs.add(blk)
        bs.normalise()
        blocksets.append(bs)

    return blocksets
