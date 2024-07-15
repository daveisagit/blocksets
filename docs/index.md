# blocksets

![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)
![PyPI - Version](https://img.shields.io/pypi/v/blocksets)
![Codecov](https://img.shields.io/codecov/c/github/daveisagit/blocksets)

A python package for performing set operations on layouts of _discrete
space_ in any dimension.

_Discrete space_ meaning integer amounts of unit space i.e. unit segment
in 1D or a pixel in 2D (or a _voxel_ in 3D - new term for me)

## Why?

Largely inspired by [advent of code](https://adventofcode.com)
puzzles that involve solving problems on integer grids in 2 or 3 dimensions and
where modelling the data as sets of tuples is not practical because of the
volume (i.e. lots of points over a large amount of space).

You might choose to use a `BlockSet` object instead of a python `set` of tuples
because of a need for high resolution/granularity pushing the limits of the
available computing power.

For example, say we would like to model a set of pixels in a 2D grid as a union
of several rectangles.

<img
src="https://raw.githubusercontent.com/daveisagit/blocksets/main/assets/example_2d.png"
width="300" height="250" alt="2D example">

Sure, at this scale we can simply model it as a set of tuples to represent each
pixel, but as the resolution increases with respect to the rectangle sizes we
start to encounter computational limits on memory and search times.

The aim of **blocksets** is to divide any layout into easily defined chunks
(i.e. lines / rectangles / cuboids etc.) in order to reduce the memory required
whilst still allowing the usual set operations to be performed.

We define a _block_ to mean a discrete space that can be defined by opposite
ends/corners such as a line segment / rectangle / cuboid etc. and we aim to
model any layout as a disjoint set of _blocks_ instead of _tuples_.

## Features & Highlights

- Multidimensional
- Support for open intervals (to infinity).
- Mirrors methods (and operators) of built-in Python **sets**.
- Set comparison is consistent regardless of derivation
- Iteration over a block set yields blocks.
- Iteration over a finite block yields tuples.
- Modelling of intervals/ranges is the same as a python range in that the lower
  limit is inclusive and the upper exclusive e.g. 1..4 = {1,2,3}

## Visualisation

An example of 2D set operations on some randomly generated block sets A, B and
drawn using `matplotlib`.

<img
src="https://raw.githubusercontent.com/daveisagit/blocksets/main/assets/example_2d_all_set_operations.png"
width="800" height="400" alt="2D - All Set Operations Example">
