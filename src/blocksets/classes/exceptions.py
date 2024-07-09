"""Custom exceptions"""


class BlockError(Exception):
    default_message = "Unexpected error in Block class."

    def __init__(self, *args, **kwargs):
        if args:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(self.default_message, **kwargs)


class DimensionMismatchError(BlockError):
    default_message = "Block arguments must be of same dimension."


class ExpectedBlockSetError(BlockError):
    default_message = "Expected a BlockSet argument."


class InvalidDimensionsError(BlockError):
    default_message = "Dimensions must be an integer >= 1."


class NotFiniteError(BlockError):
    default_message = (
        "You can not perform this operation on an infinite block or blockset."
    )


class NotAUnitError(BlockError):
    default_message = "A block expressing a single unit was expected."


class ValueParsingError(BlockError):
    default_message = "Can not interpret the given values as a Block. Expecting tuple or int values or +/- float('inf')."


class ZeroSpaceError(BlockError):
    default_message = "You can not create a block of zero space (opposite corners having the same value in one or more dimensions)."
