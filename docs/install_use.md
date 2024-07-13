# Installation & Usage

## Installation

blocksets is [available on pypi.org](https://pypi.org/project/blocksets/) and
can be installed using pip:

`pip install blocksets`

There are no dependent packages

## Example Usage

It's worth reviewing and running the `example_use.py` module via
`python -m blocksets.example_use`

Essentially you create layouts by adding and subtracting blocks from the space
which you can then treat like a set.

Here is a sample of that to give you an idea of how using blocksets optimises
the memory used to model a cube with a hole in the middle.

```python
from blocksets import Block, BlockSet

big_rubik = Block((0, 0, 0), (99999, 99999, 99999))
assert big_rubik.measure == 999970000299999
centre_cube = Block((49999, 49999, 49999))
assert centre_cube.measure == 1

# Creates a large 3 dimensional cube with the centre missing
bs = BlockSet(3)  
bs.add(big_rubik)
bs.remove(centre_cube)

assert bs.measure == 999970000299998
assert len(bs) == 6

sorted_blocks = sorted(bs, key=lambda x: x.norm)

for blk in sorted_blocks:
    print(f"{blk:50} {blk.measure}")
```

printed output

```text
(0, 0, 0)..(49999, 99999, 99999)                   499980000249999
(49999, 0, 0)..(50000, 49999, 99999)               4999850001
(49999, 49999, 0)..(50000, 50000, 49999)           49999
(49999, 49999, 50000)..(50000, 50000, 99999)       49999
(49999, 50000, 0)..(50000, 99999, 99999)           4999850001
(50000, 0, 0)..(99999, 99999, 99999)               499980000249999    
```
