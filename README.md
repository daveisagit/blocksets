# Project Description

![PyPI - Version](https://img.shields.io/pypi/v/blocksets)
![Codecov](https://img.shields.io/codecov/c/github/daveisagit/blocksets)

Python library for efficiently modelling blocks of discrete space.

Discrete space being made up of integer amounts of unit space i.e. unit segment
in 1D or a pixel in 2D (or a _voxel_ in 3D - new term for me)

Largely inspired by advent of code puzzles that involve solving problems on
integer grids in 2 or 3 dimensions and where modelling the data as sets of
tuples is not practical because of the volume (i.e. lots of points over a large
amount of space).

## For Example

Say we would like to model a set of pixels in a 2D grid as a union of several rectangles.

<img
src="https://raw.githubusercontent.com/daveisagit/blocksets/main/example_2d.png"
width="300" height="250" alt="2D example">

Sure, at this scale we can simply model it as a set of point tuples to represent
each pixel, but as the resolution increases with respect to the rectangle sizes
we start to encounter computational limits on memory and search times.

The aim of **blocksets** is to group members (i.e the discrete space) into lines
/ rectangles / cuboids etc. to reduce memory & search times whilst still
allowing the usual set operations to be performed.

We define a _block_ to be a discrete space that can be defined by opposite
ends/corners such as a line segment / rectangle / cuboid etc. and we are aim to
model any layout as a set of _blocks_ instead of _tuples_.

## Notions, Goals, Ideals & Constraints

- Aim for a multidimensional solution from the start, rather than building
  separate solutions/models.
- Allow for the expression of _Open_ intervals (to infinity).
- Mirror methods (and operators) of built-in Python **sets**.
- Set members are always blocks of the same dimension and member blocks are
  always disjoint from each other.
- Aim to be able to compare 2 sets. This maybe too hard if we don't have a
  consistent way to divide a subset up, i.e. there a multiple ways to partition
  the same 2D space into rectangles.
- Iteration over a block set yields blocks.
- Iteration over a finite block yields tuples.

_Let the exploration begin ..._

## Installation

`pip install blocksets`

There are no dependent packages

## Example Use

It's worth reviewing and running the `example_use.py` module via
`python -m blocksets.example_use`
here's a taste snippet for reading purposes

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

assert bs.point_count == 999970000299998
assert bs.block_count == 6

sorted_blocks = sorted(bs.blocks(), key=lambda x: x.norm)

for blk in sorted_blocks:
    print(f"{blk:50} {blk.measure}")
```

## Classes

To begin with I have decided to model the block and the set of blocks as classes
**Block** and **BlockSet**.

Because of

- the multi-dimensional ambition
- multiple ways to represent a block
- option of _Open_ limits

it seems sensible to keep these concerns separate from the main task in hand and
allow us to make valid assumptions about how the blocks are expressed.

### Block

A **Block** is an orthogonal clump (_a line segment, rectangle, cuboid, hyper...
you get the idea_) of discrete space defined by opposite end/corner points $A,B$.

- Decimal precision can always be achieved using some desired scaling, so
  coordinates of the space are always specified as `int` _(unless specifying an
  open interval, see below)_
- The only exception being that the `float("inf")` value can be used to
  represent no limit (i.e. an open interval to infinity be it +/- in any of the
  component dimensions)
- Internally the block will always be **normalised** such that $A \lt B$ in all
  component dimensions.

#### Normalised Form

Opposite corners will always be normalised internally so that ordinates $a_i \lt
b_i$ i.e. the vector $\vec{AB}$ is always positive in every component dimension.

The **Block** constructor handles various argument formats and resolves them to
this normalised representation after passing the following validations:

- Arguments must be either `int`, `+/- float("inf")` or a tuple of these.
- The Dimension of the 2 end/corner points must match.
- Ordinates in corresponding dimensions can not be the same value _(as that
  would imply a block of zero space)_.

#### Single Argument to the Constructor

If the second argument (for the opposite end/corner) is not supplied then it is
defaulted as follows for each ordinate in turn:

- For finite values we add +1 thus modelling a unit value
- For infinite values we assume the opposite end (i.e. the multiplicative inverse)

_So for example if all values are finite then it is a single point (or unit
block)._

Expressing them in a normalised form like this means we can easily _hash_ and
compare for equality using just the pair of coordinate tuples.

#### Block Operations

Find the overlapping intersection of 2 blocks `c = a & b` seems reasonable.
Union & Minus make no sense as there is no guarantee you end up with a single
block as a result.

We can easily support subset and superset operations too

- `a <= b`
- `a => b`
- `in`

Generally, we will assume any arguments being supplied to a **BlockSet** method
are attempting to express a **Block** (casting inline for ease of use).

For the `in` operator however, we will make an exception and assume any `tuple`
arguments are expressing a _point_ as opposed to a dereferenced list of
arguments for the Block() constructor.

> This exception may just be a matter of personal taste, but is in keeping with
> the strict notion of membership (∈) as different to subset (⊆).

### BlockSet

A **BlockSet** is an attempt to mirror python sets where members are strictly
**Block**s.

However, unlike a python set we will constrain and validate on the type of member
in that we only want **Block**s as members and they must be consistent with each
other in dimension.

In order to write nice code using methods of a **BlockSet** we will convert
non-**Block** arguments into **Block** types inline via a parsing method in the
**Block** class.

The **BlockSet** class itself offers methods and behaviour similar to that of a set.

However, the actual construction of the set using **Block**s happens via an
operation stack which gets resolved during a _normalisation_ process in which
the stacked operations `add` `remove` `toggle` are resolved to purely add
operations of disjoint spaces.

The normalisation process resolves any overlapping and redundancy such that any 2
sets of equal content (i.e. the same set of points) will have the same
representation in terms of the **Block**s used to represent the space.

Methods and operators mirror those of the native set class

- Content modifiers (add, remove, toggle)
- Set comparisons (equality, subset, superset, disjoint)
- Set operations (intersection, union, difference, symmetric_difference)
- In place set operations (intersection_update, update, difference_update, symmetric_difference_update)
- Use of the `in` operator will apply to a single **Block** object

#### Normalisation

This is main concern of the class, taking the operation stack and resolving it
to a resulting set of disjoint blocks in a consistent manner that also removes
redundancy (this being where 2 adjacent blocks could have been expressed as 1 in
the same consistent manner).

Normalisation is required and important (for accurate comparisons) but also
costly. We only want to perform it when its absolutely necessary and so clients
are advised to group together modification calls as much as possible in order to
minimise the amount of normalising required and especially so if performance is
of a significant concern.

## Design Approach

Since _Normalisation_ is more optimal when batched it makes sense to stack the
blocks being added or removed as layers so we only normalise the set when required.

This also gives us options for potentially giving blocks a value and performing
some other arithmetic (other than boolean) with them.

The main idea is to create a grid specific to the set based on only the relevant
ordinates and then recursively (by dimension) look for changes in cross-sections
at those relevant points.

Each recursive call returns a normalised set of blocks for the lower cross-section
dimension. This allows for the detection of changes and removal of redundant blocks
in a consistent fashion.

### Local Grid System

The universe is made up of galaxies and changes within themselves do not affect
other galaxies.

If we consider connected Blocks as a local system then we can optimise the
computation when Blocks are added and removed, in that we only need to consider
refreshing the representation of the local system.

> This concept may introduce an unnecessary overhead when identifying the local
systems and so we will not consider this for v1. We may look at again if there
are meaningful use cases for it.

### Optimisation

Clearly this approach is only useful if there is a significant saving on
modelling the granular space. For example if all the normalised disjoint blocks
are unit blocks then we would be better off using a set of tuples regardless.

#### Complexity

N = Number of block operation layers to normalise

- Establish the grid markers in each dimension and map their ordinates to
  markers using a binary search. NLog(N)
- Create a cross section for each marker in each dimension. (2N^2)^d at worse

#### Memory

Storing block data as a Block object has an overhead of 472 bytes per block
object (for garbage collection). Although it is unlikely to impact we may be
inclined to prefer a simple tuple to a block when it comes to modelling any
transient structures.

## Testing Strategy

- Have a small number of Block fixtures covering the various possibilities
- 3 block operations seems like a good balance (between cognition and coverage)
- Apply all possible combinations of order and operation for a group of 3 using
  some base set
- Duplicate the test cases using sets of tuple points. Since we are confident
  they produce the correct result we can compare them to the results obtained by
  the BlockSet methods.
- Testing cases with _Open_ intervals will require manually crafted tests as we
  won't be able to generate an equivalent set of tuple points

### Running Tests

Install `pytest` if not already

For a coverage report

`pytest --cov=blocksets tests/ --cov-report term-missing`

## Ideas

Currently, we are effectively modelling boolean values at specific points. We
could extend the notion of a Block Operation (i.e. layer) by say adding _value_
which may introduce more arithmetic functions like say `.sub()`  (and
`.remove()` meaning zeroise) etc.

For suggesting further ideas please create a github issue as per the
contribution guidelines

## Contribution

- At the moment it is early days so whilst the foundations are forming I am only
  inviting comments which can be given via [github issues]([https://](https://github.com/daveisagit/blocksets/issues))

## TODO - Reminders

- [ ] Test cases for normalisation using _Open_ intervals
- [ ] Test cases for set operations using _Open_ intervals
- [ ] Test cases for set operations in 3D
- [ ] More systematic test case coverage for set operations
- [ ] Some performance tests on large operation stacks
- [ ] Maybe a
  [Manim]([https://](https://docs.manim.community/en/stable/index.html)) style
  video explainer?
