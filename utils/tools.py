import pygame
import random, string, hashlib
from typing import Optional, Union, TypeVar

_T = TypeVar("_T")      # TypeVar
def apply_instance(obj: object, var: Optional[_T] = None) -> Union[_T, object]:

    """
    Applies a default object to a variable when the variable is None.

    If `var` is None, the function returns `obj`; otherwise, it returns
    the value of `var` unchanged.

    Args:
        obj: The default object to apply when `var` is None.
        var: The variable to check. If None, `obj` is returned.

    Returns:
        The value of `var` if it is not None; otherwise, `obj`.

    Example:
        >>> _apply_instance(MyComponent(), component)
        ... component

        >>> _apply_instance(MyComponent(), None)
        ... MyComponent()
    """

    return obj if var is None else var 

def generate_id(length: int, /) -> str:
    """ Generate a long, random ID """ 

    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def hash_id(_id: str, /, a: int = 1, b: int = 51) -> int:
    """ Hash the ID into an integer in the range [a, b) """

    if a >= b:
        raise ValueError(f"a < b")

    hash_bytes = hashlib.sha256(_id.encode("utf-8")).digest()
    hash_int = int.from_bytes(hash_bytes, byteorder="big")

    return a + hash_int % (b - a)

def generate_rgba() -> pygame.Color:
    """ Generate random a RGBA color """

    return (
        random.randint(0, 255),  # R
        random.randint(0, 255),  # G
        random.randint(0, 255),  # B
        random.randint(0, 255)   # A
    )
