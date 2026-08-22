from dataclasses import dataclass

@dataclass(slots=True)
class Transform:

    """
    Represents a 2D spatial transformation of an object,
    including position, scale, and rotation.

    Attributes:
        position (tuple[int, int]): The (x, y) coordinates of the
            object in space. Defaults to (0, 0), the origin.
        scale (tuple[float, float]): The scale factors along the
            (x, y) axes. Defaults to (1.0, 1.0), i.e. no scaling.
        rotation (float): The rotation angle of the object, in
            degrees. Defaults to 0.0 (no rotation).
    """

    position: tuple[int, int] = (0, 0)
    scale: tuple[float, float] = (1., 1.)
    rotation: float = 0.