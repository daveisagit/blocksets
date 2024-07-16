"""All code relating to the Block class"""

from collections.abc import Sequence
from itertools import product
from math import inf, prod
from typing import Self

from blocksets.classes.exceptions import (
    DimensionMismatchError,
    NotAUnitError,
    NotFiniteError,
    ValueParsingError,
    ZeroSpaceError,
)


class Block:
    """
    A Block is an immutable orthogonal clump (a line segment, rectangle, cuboid etc.) of
    discrete space defined by any opposite end/corner points A/B.
    """

    def __init__(self, a, b=None):
        """A block is constructed by supplying the coordinates of the opposite ends/corners A,B

        A,B are tuples in the desired dimensions consisting of integers (or
        `inf`).

        If using just 1 dimension then the wrapping tuple may be omitted.
        For example `Block(3,6)` represents the 1D units `{3, 4, 5}`

        If wishing to express an open interval then make use of `math.inf` (or
        `-math.inf`) which is equivalent to `float("inf")`.

        If the opposite corner B is not supplied, then we use the ordinates from A in each
        corresponding dimension and either

        - add +1 if it's an integer, or
        - assume the opposite end (i.e. the multiplicative inverse) if infinity.

        So if all ordinates in A are `int` then we creating a unit block.

        Raises:
            DimensionMismatchError: If A and B are in different dimensions
            ValueParsingError: When supplied arguments to the constructor do not
            meet expectation, that being integer or float("inf") or a tuple of
            those. ZeroSpaceError: If A and B have same value in any given
            dimensions
        """
        _a = self._validate_argument(a)

        # Default B if not supplied
        if b is None:
            _b = tuple(x + 1 if isinstance(x, int) else -x for x in _a)
        else:
            _b = self._validate_argument(b)

        # Check they are the same dimension
        if len(_a) != len(_b):
            raise DimensionMismatchError()

        # Same value or open interval on any dimension is not allowed
        if any(x == y for x, y in zip(_a, _b)):
            raise ZeroSpaceError()

        # Normalise
        self._normalise(_a, _b)

    @classmethod
    def parse(cls, input) -> Self:
        """By default the input is sent directly to the Block constructor.
        The exception being if the input is a sequence, then either it must be
        a list of arguments or a unit in some dimension.

        We assume it's a list of arguments by default, unless

        - the len > 2 in which case it must be a single unit in some dimension
        - or, len == 1 and this only item is also a sequence we will take it to mean a unit

        Args:
            input: Anything

        Returns:
            Block: The input parsed to a Block object
        """
        if isinstance(input, Block):
            return input

        if isinstance(input, Sequence):
            # assume this an *args list unless
            # the len > 2
            if len(input) > 2:
                return Block(input)

            # or len == 1 and input[0] is a sequence
            if len(input) == 1 and isinstance(input[0], Sequence):
                return Block(input[0])

            # otherwise by default assume the input is a list of arguments
            return Block(*input)

        # by default create the Block from the input
        return Block(input)

    @classmethod
    def parse_to_dimension(cls, dimensions: int, input) -> Self:
        """Same as parse, but with extra validation on the dimension

        Args:
            dimensions (int): The expected dimension of the resulting block
            input (any): Anything

        Raises:
            DimensionMismatchError: If the input does not match the required dimension

        Returns:
            Self: Block
        """
        b = cls.parse(input)
        if dimensions and b.dimensions != dimensions:
            raise DimensionMismatchError()

        return b

    #
    # Properties
    #

    # We ensure the object is kept immutable by accessing the hidden data members via properties

    @property
    def a(self) -> tuple:
        """Point A"""
        return self._a

    @property
    def b(self) -> tuple:
        """Point B"""
        return self._b

    @property
    def dimensions(self) -> int:
        """Property for the number of dimensions of the block

        Returns:
            int: number of dimensions
        """
        return len(self.a)

    @property
    def is_a_unit(self) -> bool:
        """Property set upon creation to flag if the block is a single unit

        Returns:
            bool: True if the block a single unit in any dimension
        """
        return self._is_a_unit

    @property
    def is_finite(self) -> bool:
        """Does the block have any open bounds? If so then the block is considered infinite

        Returns:
            bool: Returns True if the block is finite.
        """
        if any(x in (-inf, inf) for x in self.a):
            return False
        if any(x in (-inf, inf) for x in self.b):
            return False
        return True

    @property
    def manhattan(self) -> int:
        """Property providing the manhattan distance from A -> B

        Returns:
            int: The sum of the sides
        """
        return sum(self.side_lengths)

    @property
    def measure(self) -> int:
        """Property providing the length, area, volume (depending on the dimension)

        Returns:
            int: The measure (i.e. length, area, volume)
        """
        return prod(self.side_lengths)

    @property
    def norm(self) -> tuple:
        """Return the block in its normalised form (A,B)

        Returns:
            tuple: (A,B)
        """
        return (self.a, self.b)

    @property
    def side_lengths(self) -> tuple:
        """Property providing the side lengths

        Returns:
            tuple: The side lengths of each dimension
        """
        return tuple(bi - ai for ai, bi in zip(self.a, self.b))

    #
    # Comparison
    #

    def __contains__(self, item) -> bool:
        item = self._parse_unit_block_arg(item)
        return item <= self

    def __eq__(self, value: object) -> bool:
        value = self.parse_to_dimension(self.dimensions, value)
        return self.norm == value.norm

    def __le__(self, value: object) -> bool:
        value = self.parse_to_dimension(self.dimensions, value)
        i = self._intersection(value)
        if i is not None:
            return self.norm == i.norm
        return False

    def __lt__(self, value: object) -> bool:
        if value == self:
            return False
        return self <= value

    def __ge__(self, value: object) -> bool:
        value = self.parse_to_dimension(self.dimensions, value)
        i = self._intersection(value)
        if i is not None:
            return value.norm == i.norm
        return False

    def __gt__(self, value: object) -> bool:
        if value == self:
            return False
        return self >= value

    def __matmul__(self, other) -> bool:
        # Make use of the @ operator as a shorthand for being in contact with
        return self.in_contact_with(other)

    #
    # Intersection
    #

    def __and__(self, other) -> Self:
        other = self.parse_to_dimension(self.dimensions, other)
        return self._intersection(other)

    #
    # Rep & Render
    #

    def __hash__(self) -> int:
        return hash(self.norm)

    def __repr__(self) -> str:
        return str(self.norm)

    def __str__(self) -> str:
        # Render as the coordinates of the opposite corners or the interval on a line.
        # Either as A -> B or just A if its a single unit

        if self.is_a_unit:
            if self.dimensions == 1:
                return str(self.a[0])
            return str(self.a)

        if self.dimensions == 1:
            return f"{str(self.a[0])}..{str(self.b[0])}"
        return f"{str(self.a)}..{str(self.b)}"

    def __format__(self, format_spec) -> str:
        return format(str(self), format_spec)

    #
    # Existence and Iteration
    #

    def __bool__(self):
        return True

    def __iter__(self):
        for t in self._units():
            yield t

    def __len__(self):
        return self.measure

    #
    # Implementations
    #

    def in_contact_with(self, other: object) -> bool:
        """Return True if this block touches the other in any way (vertex, edge, face etc.)
        or overlaps it.

        Shorthand: `A @ B`

        Args:
            other (Block): Another Block instance for comparison

        Returns:
            bool: True if this block touches the other in any way (vertex, edge, face etc.) or overlaps it
        """
        other = self.parse_to_dimension(self.dimensions, other)
        return self._in_contact_with(other)

    #
    # Private
    #

    @classmethod
    def _validate_ordinate(cls, x):
        """Called by _validate_argument() for checking the validity of a tuple content

        Args:
            x: an ordinate value

        Raises:
            ValueError: For an unexpected value
        """

        if isinstance(x, float):
            if x not in (inf, -inf):
                raise ValueParsingError()
            return
        elif isinstance(x, int):
            return

        raise ValueParsingError()

    @classmethod
    def _validate_argument(cls, x) -> tuple:
        """Called by the constructor to ensure an argument is valid

        Args:
            x: a coordinate

        Raises:
            ValueError: For an unexpected value

        Returns:
            tuple: The input argument is returned as a tuple even if not supplied as one.
        """

        if isinstance(x, float):
            if x not in (inf, -inf):
                raise ValueParsingError()
            return (x,)
        elif isinstance(x, int):
            return (x,)
        elif isinstance(x, Sequence):
            for o in x:
                cls._validate_ordinate(o)
            return x

        raise ValueParsingError()

    def _normalise(self, a: tuple, b: tuple):
        """Normalise the tuple pair of coordinates A,B representing the opposite ends/corners of the block
        We ensure the vector from A -> B is always in a positive direction for any component dimension

        We note if the block is a single unit to save computing it again

        Args:
            a (tuple): Coordinates of A
            b (tuple): Coordinates of B
        """

        na = []
        nb = []
        self._is_a_unit = True
        for i in range(len(a)):
            ai = a[i]
            bi = b[i]
            nai = min(ai, bi)
            nbi = max(ai, bi)
            na.append(nai)
            nb.append(nbi)
            if nbi != nai + 1:
                self._is_a_unit = False

        # finally set the limiting end/corners of the block
        self._a = tuple(na)
        self._b = tuple(nb)

    def _parse_unit_block_arg(self, x) -> Self:
        """For when any tuple is assumed to be a unit"""
        if not isinstance(x, Block):
            x = Block(x)
        if self.dimensions != x.dimensions:
            raise DimensionMismatchError()
        if not x.is_a_unit:
            raise NotAUnitError
        return x

    def _in_contact_with(self, other: Self) -> bool:
        """Return True if this block touches the other in any way (vertex, edge, face etc.)
        or overlaps it.

        Args:
            other (Block): Another Block instance for comparison

        Returns:
            bool: True if this block touches the other in any way (vertex, edge, face etc.) or overlaps it
        """
        return all(
            self.a[i] <= other.a[i] <= self.b[i]
            or other.a[i] <= self.a[i] <= other.b[i]
            for i in range(self.dimensions)
        )

    def _intersection(self, other: Self) -> Self | None:
        """Find the resulting intersection 2 Blocks, using the maximum of the lower limits
        and the minimum of the uppers

        Args:
            other (Block): Another Block instance for comparison

        Returns:
            Block | None: None if they don't overlap
        """
        a = []
        b = []
        for i in range(self.dimensions):
            ai = max(self.a[i], other.a[i])
            bi = min(self.b[i], other.b[i])
            if bi <= ai:
                return None
            a.append(ai)
            b.append(bi)

        return Block(tuple(a), tuple(b))

    def _units(self):
        """A generator for all the unit pixel tuples in the block

        Raises:
            NotFiniteError: if requested on an infinite block

        Yields:
            tuple: The coordinates of an integer tuple unit in the block
        """
        if not self.is_finite:
            raise NotFiniteError()

        dimensions = []
        for d in range(self.dimensions):
            dimensions.append(range(self.a[d], self.b[d]))
        for t in product(*dimensions):
            yield t
