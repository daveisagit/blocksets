"""All code relating to the Blockset class"""

from bisect import bisect_left
from enum import Enum
from blocksets.classes.block import Block
from blocksets.classes.exceptions import (
    InvalidDimensionsError,
)


class OperationType(Enum):
    ADD = "+"
    REMOVE = "-"
    TOGGLE = "~"


class BlockSet:
    """A set of Blocks which are of the same dimension.

    Although the class offers methods and behaviour similar to that of a set,
    the actual construction of the set using Blocks happens via an operation stack which gets
    resolved during a normalisation process.

    In normalized form all the resulting blocks are disjoint.

    The normalisation process resolves overlapping and redundancy such that
    any 2 sets of equal content (i.e. the same set of points) will have the same
    representation in terms of the blocks used to represent the space.

    Methods and operators mirror those of the native set class
    - Modify the content (add, remove, toggle)
    - Compare (equality, subset, superset)
    - Compare operations (intersection, union, difference)

    There is some extra validation some methods to ensure
    the supplied arguments are, or can be interpreted as a Block/BlockSet
    and match the dimension of the current content.

    Normalisation is required and important (for accurate comparisons) but also costly.
    We only want to perform it when its absolutely necessary and so clients are advised
    to group together modification calls as much as possible in order to minimise the amount
    of normalising required and especially so if performance is of a significant concern.

    """

    def __init__(self, dimensions: int | None = None) -> None:
        """Create a Blockset, optionally provide the dimensions for more strict and performant use

        Args:
            dimensions (int | None, optional): Specify the dimensions if you like. Defaults to None.

        Raises:
            InvalidDimensionsError: If not an integer or < 1
        """
        self.clear()
        if dimensions is not None:
            if not isinstance(dimensions, int):
                raise InvalidDimensionsError()
            if dimensions < 1:
                raise InvalidDimensionsError()
        self._dimensions = dimensions
        self._marker_ordinates = []
        self._marker_stack = []

    @property
    def dimensions(self) -> int:
        """Returns the dimensions of the points/blocks contained within which if not given upon
        construction are inferred by the content.

        Returns:
            int: The dimensions of the points/blocks contained within
        """
        if self._dimensions:
            return self._dimensions

        if self._operation_stack:
            _, block = self._operation_stack[0]
            if isinstance(block, Block):
                return block.dimensions
            return len(block[0])

        return None

    @property
    def normalised(self) -> bool:
        """Return the normalisation state

        Returns:
            bool: True if the BlockSet is in a Normalised state
        """
        return self._normalised

    def add(self, blk: Block):
        """Append an add block operation to the stack

        Args:
            blk (Block): A block
        """
        blk = Block.parse_to_dimension(self.dimensions, blk)
        self._operation_stack.append((OperationType.ADD, blk))
        self._normalised = False

    def remove(self, blk: Block):
        """Append a remove block operation to the stack

        Args:
            blk (Block): A block
        """

        blk = Block.parse_to_dimension(self.dimensions, blk)
        self._operation_stack.append((OperationType.REMOVE, blk))
        self._normalised = False

    def toggle(self, blk: Block):
        """Append a toggle block operation to the stack

        Args:
            blk (Block): A block
        """
        blk = Block.parse_to_dimension(self.dimensions, blk)
        self._operation_stack.append((OperationType.TOGGLE, blk))
        self._normalised = False

    def clear(self):
        """Clear the BlockSet operation stack"""
        self._normalised = True
        self._operation_stack = []

    def normalise(self):
        """Normalise the BlockSet
        Analyse all the stacked operations and resolve to a disjoint set of add operations
        removing redundancy
        """

        def markers_to_ordinates(marker_tuple):
            return tuple(
                self._marker_ordinates[d][m] for d, m in enumerate(marker_tuple)
            )

        if self._normalised:
            return

        self._refresh_marker_ordinates()
        self._refresh_marker_stack()

        normalised_markers = self._normalise_recursively(self._marker_stack)

        # replace the operation stack with ADD operations for the normalised result
        self._operation_stack = [
            (OperationType.ADD, (markers_to_ordinates(a), (markers_to_ordinates(b))))
            for a, b in normalised_markers
        ]

        self._normalised = True

    def blocks(self):
        """Generator for all the disjoint blocks after normalising

        Yields:
           Block: a block object
        """
        self.normalise()

        # after normalisation we have only add operations on disjoint blocks
        for _, blk in self._operation_stack:
            yield Block(*blk)

    def block_tuples(self):
        """Generator for all the disjoint blocks after normalising

        Yields:
           Tuple: a block expressed as a tuple pair of ends/corners
        """
        self.normalise()

        # after normalisation we have only add operations on disjoint blocks
        for _, blk in self._operation_stack:
            yield blk

    def _refresh_marker_ordinates(self):
        """Refreshes _marker_ordinates which stores actual ordinate values of
        the grid markers"""

        self._marker_ordinates.clear()
        for d in range(self.dimensions):
            markers = set()
            for _, blk in self._operation_stack:
                markers.add(blk.a[d])
                markers.add(blk.b[d])
            markers = list(sorted(markers))
            self._marker_ordinates.append(markers)

    def _refresh_marker_stack(self):
        """Refreshes _marker_stack which is equivalent to _operation_stack but
        expressed as grid markers instead of the block ordinates"""

        self._marker_stack.clear()
        for op, blk in self._operation_stack:
            a = []
            b = []
            for d in range(self.dimensions):
                markers = self._marker_ordinates[d]
                a.append(bisect_left(markers, blk.a[d]))
                b.append(bisect_left(markers, blk.b[d]))
            entry = (op, (tuple(a), tuple(b)))
            self._marker_stack.append(entry)

    def _normalise_recursively(self, marker_stack: list, dimension: int = 0) -> set:
        """Return a normalised set of block markers

        Args:
            marker_stack (list): The marker stack to resolve
        """

        def cross_section_changed():
            """Whenever a cross section changes we need to construct
            blocks that reflect the previous cross section for this marker and
            add them to our normalised set in this dimension.

            This could happen called during the iteration over the grid markers
            or after leaving that loop, so we scope to a function for dryness"""

            if change_marker is not None:
                if last_dimension and prev_normalised_x_sec:
                    normalised_blocks.add(((change_marker,), (m,)))
                if not last_dimension:
                    for x in prev_normalised_x_sec:
                        a = (change_marker,) + x[0]
                        b = (m,) + x[1]
                        normalised_blocks.add((a, b))

        # Being in the last dimension is a special case so we note it up front
        last_dimension = False
        if self.dimensions == dimension + 1:
            last_dimension = True

        # Final result set
        normalised_blocks = set()

        # Used to handle the changes found in cross sections as scan through
        prev_normalised_x_sec = set()
        change_marker = None

        # For each marker in this dimension we get the cross section of
        # normalised blocks of the lower dimension.

        # If there is a change in the normalised blocks between cross sections
        # then this indicates we should create blocks in this dimension and add
        # them to our result set.

        for m in range(len(self._marker_ordinates[dimension])):

            # Get the operation stack for the lower dimension at this marker
            # If this is the last dimension then only the operation makes sense
            cross_section = [
                (op, None if last_dimension else (blk[0][1:], blk[1][1:]))
                for op, blk in marker_stack
                if blk[0][0] <= m < blk[1][0]
            ]

            if last_dimension:
                # If we are resolving the last dimension then we just need to
                # resolve the operations in reverse order (i.e. stack pop)
                # for this marker point.
                state = False
                for op, _ in cross_section[::-1]:
                    if op == OperationType.ADD:
                        state = not state
                        break
                    if op == OperationType.REMOVE:
                        break
                    if op == OperationType.TOGGLE:
                        state = not state

                # If the point should be present (i.e. True) then we represent that
                # as the set {True}, if not then the empty set.
                # This allows us to compare 2 cross sections as sets
                # in a consistent manner for all dimensions
                normalised_x_sec = set()
                if state:
                    normalised_x_sec = {True}

            else:
                # Get the normalised representation of this cross section
                # using recursion
                normalised_x_sec = self._normalise_recursively(
                    cross_section, dimension + 1
                )

            # By only adding blocks when there are cross section changes
            # we should hopefully remove redundant blocks
            if normalised_x_sec != prev_normalised_x_sec:
                cross_section_changed()
                change_marker = m
                prev_normalised_x_sec = normalised_x_sec

        if normalised_x_sec != prev_normalised_x_sec:
            cross_section_changed()

        return normalised_blocks
