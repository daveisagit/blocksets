# Thoughts

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

## Local Grid System

The universe is made up of galaxies and changes within themselves do not affect
other galaxies.

If we consider connected Blocks as a local system then we can optimise the
computation when Blocks are added and removed, in that we only need to consider
refreshing the representation of the local system.

> This concept may introduce an unnecessary overhead when identifying the local
systems and so we will not consider this for v1. We may look at again if there
are meaningful use cases for it.

## Optimisation

Clearly this approach is only useful if there is a significant saving on
modelling the granular space. For example if all the normalised disjoint blocks
are unit blocks then we would be better off using a set of tuples regardless.

### Complexity

N = Number of block operation layers to normalise

- Establish the grid markers in each dimension and map their ordinates to
  markers using a binary search. NLog(N)
- Create a cross section for each marker in each dimension. (2N^2)^d at worse

### Memory

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

Install `pytest` and for a coverage report run

`pytest --cov=blocksets tests/ --cov-report term-missing`

## Ideas

Currently, we are effectively modelling boolean values at specific points. We
could extend the notion of a Block Operation (i.e. layer) by say adding _value_
which may introduce more arithmetic functions like say `.sub()`  (and
`.remove()` meaning zeroise) etc.

For suggesting further ideas please create a github issue as per the
contribution guidelines

## To Do

- Test cases for set operations in 3D
- Some performance tests on large operation stacks
- Maybe a [Manim]([https://](https://docs.manim.community/en/stable/index.html))
  style video explainer?
