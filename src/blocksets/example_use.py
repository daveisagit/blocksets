from blocksets import Block, BlockSet

#
# Make a face, something visual to get the idea
#


def draw_layout(bs: BlockSet):
    """Some simple code to visualise a small blockset in a 10x10 grid"""
    tuples = set()
    for b in bs:
        tuples.update(set(b))

    print()
    print(bs)
    for row in range(9, -1, -1):
        line = ""
        for col in range(10):
            ch = " "
            if (col, row) in tuples:
                ch = "#"
            line += ch
        print(line)


print()
print("=====================================================================")
print(" Example 1 - Compose a face of component parts using set operations")
print("=====================================================================")
print()

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
print("==================================================================")
print(" Example 2 - Large cube with small hole in the middle")
print("==================================================================")
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

print(f"Total volume less 1 central cube: {bs.unit_count}")
print(f"Number of Blocks: {bs.block_count}")
print(bs)
print("Block make-up")

sorted_blocks = sorted(bs, key=lambda x: x.norm)
for blk in sorted_blocks:
    print(f"{blk:50} {blk.measure}")

#
# Example of testing for equality (with attention to details)
#
print()
print("==================================================================")
print(" Example 3 - Crafting space in different ways")
print("==================================================================")
print()
print("Compare 2 equal blocks sets arrived at in different ways")
print("Two versions of a chunky table:")
print("- One made of wood assembled as components of a surface and 4 legs")
print("- One made of stone carving out the underneath")
print()

surface = Block((0, 0, 950), (1000, 1000, 1000))
leg1 = Block((0, 0, 0), (50, 50, 1000))
leg2 = Block((0, 950, 0), (50, 1000, 1000))
leg3 = Block((950, 0, 0), (1000, 50, 1000))
leg4 = Block((950, 950, 0), (1000, 1000, 1000))
wooden = BlockSet(3)
wooden.add(surface)
wooden.add(leg1)
wooden.add(leg2)
wooden.add(leg3)
wooden.add(leg4)

cube = Block((0, 0, 0), (1000, 1000, 1000))
carve1 = Block((50, 0, 0), (950, 1000, 950))
carve2 = Block((0, 50, 0), (1000, 950, 950))
stone = BlockSet(3)
stone.add(cube)
stone.remove(carve1)
stone.remove(carve2)

assert wooden == stone
print(f"Wood : {wooden}")
print(f"Stone: {stone}")
print(f"Tables equal: {wooden == stone}")
print()
print("Both makers apply their trademark")
print("- Carpenter adds a (+) cross in a 3x3")
print("- Mason removes chunk of 3x3")

carpenter = BlockSet()
carpenter.add(Block((2, 1, 1000), (3, 4, 1001)))
carpenter.add(Block((1, 2, 1000), (4, 3, 1001)))
wooden |= carpenter

mason = BlockSet()
mason.add((Block((1, 1, 999), (4, 4, 1000))))
stone -= mason

assert wooden != stone
print(f"Wood : {wooden}")
print(f"Stone: {stone}")
print(f"Tables equal: {wooden == stone}")

print()
print("They agree to apply each others mark to their own work")
wooden -= mason
stone |= carpenter
assert wooden == stone
print(f"Wood : {wooden}")
print(f"Stone: {stone}")
print(f"Tables equal: {wooden == stone}")
