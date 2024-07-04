from blocksets import Block, BlockSet


def draw_layout(bs: BlockSet):
    """Some simple code to visualise a small blockset in a 10x10 grid"""
    points = set()
    for b in bs.blocks():
        points.update(b.lattice())

    print()
    print(f"Blocks: {bs.block_count}")
    print(f"Points: {bs.point_count}")
    for row in range(9, -1, -1):
        line = ""
        for col in range(10):
            ch = " "
            if (col, row) in points:
                ch = "#"
            line += ch
        print(line)


# BlockSet content is constructed by adding layers of instructions
# to either add / remove / toggle a piece of space defined by a block
eyes = BlockSet(2)
eyes.add(Block((2, 6), (4, 8)))
eyes.add(Block((6, 6), (8, 8)))

mouth = BlockSet(2)
mouth.add(Block((2, 2), (8, 4)))
mouth.remove(Block((3, 3), (7, 4)))
mouth.remove(Block((2, 2)))
mouth.remove(Block((7, 2)))

# BlockSets can be compared / created / updated in the same way as python sets

assert eyes.isdisjoint(mouth)

features = eyes | mouth  # union
draw_layout(features)

head = BlockSet(2)
head.add(Block((0, 0), (10, 10)))
head.remove(Block((0, 0), (2, 2)))
head.remove(Block((8, 0), (10, 2)))
head.add(Block((1, 1)))
head.add(Block((8, 1)))
head.toggle(Block((0, 9)))
head.toggle(Block((9, 9)))
draw_layout(head)

face = head - features  # difference
draw_layout(face)

assert face <= head  # subset

#
# Example of efficiently modelling a large volume with a single exception
#

print()
print("Efficiently modelling a large volume with a single exception")
print("e.g. Rubik on rails (99999 x 99999 x 99999)")
print()
big_rubik = Block((0, 0, 0), (99999, 99999, 99999))
centre_cube = Block((49999, 49999, 49999))
print(f"Total volume: {big_rubik.measure}")
bs = BlockSet(3)  # Creates a 3 dimensional blockset
bs.add(big_rubik)
bs.remove(centre_cube)

print(f"Total volume less 1 central cube: {bs.point_count}")
print(f"Number of Blocks: {bs.block_count}")
print(bs)
print("Block make-up")

sorted_blocks = sorted(bs.blocks(), key=lambda x: x.norm)

for blk in sorted_blocks:
    print(f"{blk:50} {blk.measure}")
