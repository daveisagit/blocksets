# Classes

The concerns of a **Block** are quite separate from that of a **BlockSet** and
are mainly to do with the construction of a **Block** object. Parsing and
validation need to pay attention to

- handling the parsing of multi-dimensional data
- multiple ways to represent a block (i.e. any set of opposite corner points
  could be used)
- handling open limits to infinity
- handling the expression of a unit as single corner

## Block

A **Block** is an orthogonal clump (_a line segment, rectangle, cuboid, hyper...
you get the idea_) of discrete space defined by any opposite end/corner points
A,B.

- Decimal precision can always be achieved using some desired scaling, so
  coordinates of the space are always specified as `int` _(unless specifying an
  open interval, see below)_
- The only exception being that the `float("inf")` value can be used to
  represent no limit (i.e. an open interval to infinity be it +/- in any of the
  component dimensions)
- Any pair of opposite corners can be used and in any order.
- Internally the block will always be **normalised** such that A<B in all
  component dimensions.

### Normalised Form

Opposite corners will always be normalised internally so that he vector _AB_ is
always positive in every component dimension.

For example

<img
src="https://raw.githubusercontent.com/daveisagit/blocksets/main/assets/block_3D.png"
width="300" height="240" alt="3D Block">

```python
A = (5, 0, 0)
B = (0, 4, 3)
block = Block(A, B)
```

would construct a block with opposite corners defined as (0,0,0) and (5,4,3)

### Parsing & Validation

The **Block** constructor handles various argument formats and resolves them to
this normalised representation if passing the following validations:

- Arguments must be either `int`, `+/- float("inf")` or a tuple of these.
- The Dimension of the 2 end/corner points must match.
- Ordinates in corresponding dimensions can not be the same value _(as that
  would imply a block of zero space)_.

### Constructor

The constructor expects 1 or 2 arguments which express the opposite corners A,B.

If the second argument (for the opposite end/corner) is not supplied then it is
defaulted as follows for each ordinate in turn:

- For finite values we add +1 thus modelling a unit value
- For infinite values we assume the opposite end (i.e. the multiplicative inverse)

So if all values are finite then it is expressing a unit block.

### Parsing

There are 2 class methods also available `parse()` and `parse_to_dimension()` which
are primarily used by the `BlockSet` class to handle the parsing of arguments
inline.

### Operations

Finding the overlapping intersection of 2 blocks `c = a & b` seems reasonable.
However, union and difference make no sense as there is no guarantee you end up
with a single block as a result.

subset, superset and membership operations are also supported.

- `a <= b`
- `a => b`
- `unit in a` 

Generally, we assume that any arguments being supplied to a **Block** operation
are attempting to express a **Block**.

For the `in` operator however, we will make an exception and assume any `tuple`
arguments are expressing a _unit_ as opposed to a dereferenced list of
arguments for the `Block()` constructor.

This exception is in keeping with the strict notion of membership (∈) as
different to subset (⊆).

## BlockSet

A `BlockSet` is a container class for blocks mirroring the same behaviour as a
`set`.

However, (unlike a python set) we constrain and validate on the type of
member, we only want `Block` objects and they must be in the same dimension.

In order to facilitate _duck typing_ we will convert arguments inline via parsing
methods in the `Block` class.

The actual construction of the set using `Block` objects happens via an
operation stack which gets resolved during the _normalisation_ process in which
the stacked operations `add`, `remove` & `toggle` are resolved to purely add
operations of disjoint spaces.

The normalisation process resolves any overlapping and redundancy such that sets
of equal content (i.e. the same layout of units) will have the same
representation in terms of the disjoint `Block` objects used to represent the space.

Methods and operators mirror those of the native set class

- Content modifiers (add, remove, toggle)
- Set comparisons (equality, subset, superset, disjoint)
- Set operations (intersection, union, difference, symmetric_difference)
- In place set operations (intersection_update, update, difference_update, symmetric_difference_update)
- Use of the `in` operator will apply to a single `Block` object

### Normalisation

This is main concern of the class, taking the operation stack and resolving it
to a resulting set of disjoint blocks in a consistent manner that also removes
redundancy (this being where 2 adjacent blocks could have been expressed as 1 in
the same consistent manner).

Normalisation is required and important (for accurate comparisons) but also
costly. We only want to perform it when its absolutely necessary and so clients
are advised to group together modification calls as much as possible in order to
minimise the amount of normalising required and especially so if performance is
of a significant concern.
