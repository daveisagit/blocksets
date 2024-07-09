# blocksets

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![PyPI - Version](https://img.shields.io/pypi/v/blocksets)
![Read the Docs](https://img.shields.io/readthedocs/blocksets)
![Codecov](https://img.shields.io/codecov/c/github/daveisagit/blocksets)

Python package for performing set type operations on any layout of discrete
space in any dimension.

- **Block** is an orthogonal clump of units/pixels (_i.e. a line segment,
rectangle, cuboid, hyper... you get the idea_)

- **BlockSet** is a set of blocks that resolves any make-up of blocks to a
  disjoint set in a consistent fashion

## Why?

You might choose to use a `BlockSet` instead of a regular python `set` of
points/pixels because the resolution/granularity is sufficiently high, meaning
the number of pixels/points being modelled due to the expanse of the space
pushes the limits of the available computing power.

## How?

- Create any layout (as a blockset) using a stacked list of block operations
  which `add` `remove` or `toggle` blocks over the current blockset state.
- Perform the usual set arithmetic `union` `intersection` `difference` etc. on
  blockset objects.
- Compare 2 blockset objects using the standard set comparison methods and
  operators `==` `<=` `>=`.
- Results are always consistent regardless of how they were constructed.

## Installation

Requires python 3.11 or higher, there are no dependencies.

`pip install blocksets`

## Usage

Full documentation is available (work in progress) at [readthedocs](https://blocksets.readthedocs.io/)

It's worth reviewing and running the `example_use.py` module via
`python -m blocksets.example_use`

### TL;DR

```python
from blocksets import Block, BlockSet

# A block is defined by the co-ordinates of the opposite corners
big_rubik = Block((0, 0, 0), (99999, 99999, 99999)) 
assert big_rubik.measure == 999970000299999

# A single argument is a unit block
centre_cube = Block((49999, 49999, 49999))
assert centre_cube.measure == 1

# Create a large 3 dimensional cube with the centre missing
bs = BlockSet(3)  
bs.add(big_rubik)
bs.remove(centre_cube)

assert bs.unit_count == 999970000299998
assert bs.block_count == 6

sorted_blocks = sorted(bs, key=lambda x: x.norm)

for blk in sorted_blocks:
    print(f"{blk:50} {blk.measure}")
```

The resulting space is modelled using 6 objects (effectively tuples) instead of 999970000299998

```text
(0, 0, 0)..(49999, 99999, 99999)                   499980000249999
(49999, 0, 0)..(50000, 49999, 99999)               4999850001
(49999, 49999, 0)..(50000, 50000, 49999)           49999
(49999, 49999, 50000)..(50000, 50000, 99999)       49999
(49999, 50000, 0)..(50000, 99999, 99999)           4999850001
(50000, 0, 0)..(99999, 99999, 99999)               499980000249999    
```

## Contribution

At the moment it is early days so whilst the foundations are forming I am only
inviting comments which can be given via [github
issues]([https://](https://github.com/daveisagit/blocksets/issues))
