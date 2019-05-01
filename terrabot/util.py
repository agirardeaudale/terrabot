from random import sample
from itertools import chain

def shuffled(seq):
    return sample(seq, k=len(seq))

#def flatten(nested_iterable: Iterable[Iterable[Any]]):
#    """Flatten a nested Iterable.
#
#    Example:
#        >>> nested_iterable = ((1, 2), (3, 4))
#        >>> flatten(nested_iterable)
#        (1, 2, 3, 4)
#
#    This is faster than sum(nested_iterable, ()) for large sequences.
#    """
#    return (x for x in chain.from_iterable(nested_iterable))
#
#def coerce_to_iterable(
#        input: Any,
#        none_result: Any,
#        treat_str_as_noniterable: bool = False,
#        verify_type: type: None) -> Iterable[Any]:
#    """Return an input wrapped in a single item Iterable if it is not an Iterable, otherwise
#    return the argument as-is. If the input is None, return a default value specified by the caller.
#
#    Args:
#        input - The input to coerce into an Iterable.
#        none_result - What to return if input is None.
#        treat_str_as_noniterable - If true, treat a str as a single item (instead of an Iterable of
#            characters) and wrap it in an Iterable if it is the only item provided.
#        verify_type: If provided, verify that each item of the input is of the specified type.
#    """
#    if input is None:
#        coerced_input = default
#    elif treat_str_as_noniterable and isinstance(input, str):
#        return tuple(input)
#    elif isinstance(input, Iterable):
#        return input
#    else:
#        return tuple(input)
#
#    if verify_type is not None:
#        unrecognized_types = (type(x) for x in input if not isinstance(x, verify_type))
#        if any(unrecognized_types):
#            expected_type_name = verify_type.__name__
#            actual_type_name = type(unrecognized_types[0]).__name__
#            raise TypeError(f"Unrecognized argument type {actual_type_name}. "
#                    + f"Expected {expected_type_name} or Iterator[{expected_type_name}])
