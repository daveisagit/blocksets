# blocksets

Python library for efficiently modelling blocks of discrete space.

Discrete space being made up of integer amounts of unit space i.e. unit segment
in 1D or a pixel in 2D (or a _voxel_ in 3D - new term for me)

Largely inspired by advent of code puzzles that involve solving problems on
integer grids in 2 or 3 dimensions and where modelling the data as sets of
tuples is not practical because of the volume (i.e. lots of points over a large
amount of space).

## Examples

Imagine a 2D grid of lattice points. We would like to model a subset of pixels
in the grid in an efficient way.

For example, the union of several rectangles.

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

##### Single Argument to the Constructor

If the second argument (for the opposite end/corner) is not supplied then it is
defaulted as follows for each ordinate in turn:

- For finite values we add +1 thus modelling a unit value
- For infinite values we assume the opposite end (i.e. the multiplicative inverse)

_So for example if all values are finite then it is a single point (or unit
block)._

Having it a normalised form we can easily _hash_ and compare for equality using
a pair of coordinate tuples.

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

- Modify the content (add, remove, toggle)
- Compare (equality, subset, superset)
- Compare operations (intersection, union, difference)

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

## The Grid

The concept under pinning the optimisation is to create a grid specific to the
set that is defined by when cross-sections change on a given dimension.

### Global vs Local

Global is useful for quickly finding all the blocks another block is touching or
intersecting but may mean that a large isolated block is divided up when it
could be left as is. Local would optimize the lesser number of blocks if they
are isolated but may introduce complexity and potentially an inconsistency in
representation

### Optimisation

Considerations

- Aim to sort the grid markers in every dimension and search them in a binary
  fashion for log(N) complexity.

### Local Grid System

The universe is made up of galaxies and changes within themselves do not affect
other galaxies.

If we consider connected Blocks as a local system then we can optimise the
computation when Blocks are added and removed, in that we only need to consider
refreshing the representation of the local system.

> This concept may introduce an unnecessary overhead when identifying the local
systems and so we will not consider this for v1. We may look at again if there
are meaningful use cases for it.

#### Storage

Storing block data as a Block object has an overhead of 472 bytes for garbage
collection. Within a LGS object block we have the option of storing the
definition as the normalised tuple if we wish to save on that. However, we may
want to store the reference to a block against a grid marker in which the object
reference is better suited.

## TODO - Reminders

- [x] Normalisation
- [x] 3D tests
- [ ] BlockSet operations Union / Intersection / Difference
- [ ] PyPI registration

## Testing Strategy

- Have a small number of Block fixtures covering overlap possibilities
- 3 block operations seems like a good balance (between cognition and coverage)
- Apply all possible combinations of order and operation for a group of 3 using
  some base set
- Compare to result as obtained by similar set operations on tuples from the
  lattice

## More Ideas

Currently we are effectively modelling boolean value on any given point.
We could extend the notion of a layer to having value introducing more
arithmetical type functions like say `.sub()` , remove meaning zeroise.

## Contribution

- No third party packages are required (hence no requirements.txt) except pytest
  for testing
- Install pytest into your venv using `pip install pytest`
