import pygame, math
from typing import Optional

# Engine import
from ....utils.tools import apply_instance

class _Collider:

    """
    Base class for collision shapes.

    Intended to be subclassed rather than used directly. Provides
    shared position/size state, an axis-aligned bounding rect for
    collision checks, and helper methods for distance and collision
    detection between colliders and against the mouse. Subclasses
    are responsible for implementing `draw_collider` to render their
    specific shape.

    Attributes:
        position (tuple[int, int]): The top-left position of the
            collider's bounding area.
        size_collider (tuple[int, int]): The (width, height) of the
            collider's bounding area.
        color (pygame.Color): The color used when drawing the
            collider. Defaults to a tomato-red color if not given.
        enable (bool): Whether the collider participates in
            collision checks.
        visible (bool): Whether the collider is drawn to screen.
    """

    def __init__(self,
                 tag: str,
                 position: tuple[int, int] = (0, 0),
                 size_collider: tuple[int, int] = (32, 32),
                 color: Optional[pygame.Color] = None,
                 enable: bool = True,
                 visible: bool = True):
        self._tag = tag
        self.position = position
        self.size_collider = size_collider
        self.color = apply_instance(pygame.Color(255, 99, 71, 255), color)
        self.enable = enable        # Check whether the collider exists
        self.visible = visible      # Check whether the collider draws

        self._surf = pygame.Surface(self.size_collider, pygame.SRCALPHA)
        self._rect = pygame.Rect(self.position, self.size_collider)

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def tag(self) -> str:
        return self._tag

    def get_center_points(self) -> tuple[int, int]:
        x, y = self.position
        w, h = self.size_collider

        return (x + w / 2, y + h / 2)

    def distance(self, other: "_Collider") -> float:

        """
        Calculates the distance between this collider and another.

        Args:
            other (_Collider): The other collider to measure distance to.

        Returns:
            float: The Euclidean distance between the center points
                of the two colliders.
        """

        cx, cy = self.get_center_points()   # Center point of collider
        ox, oy = other.get_center_points()  # Center point of other collider

        return math.sqrt(
            pow(cx - ox, 2)
            +
            pow(cy - oy, 2)
        )

    def is_collider_with(self, other: "_Collider") -> bool:

        """
        Checks whether this collider overlaps another collider.

        Args:
            other (_Collider): The other collider to check against.

        Returns:
            bool: True if both colliders are enabled and their
                bounding rects overlap, False otherwise.
        """

        if not self.enable or not other.enable: return False
        return self._rect.colliderect(other.rect)

    def is_collider_with_mouse(self, mouse_pos: tuple[int, int]) -> bool:

        """
        Checks whether a point (typically the mouse position) is inside the collider.

        Args:
            mouse_pos (tuple[int, int]): The (x, y) point to check,
                usually the current mouse position.

        Returns:
            bool: True if the collider is enabled and the point lies
                within its bounding rect, False otherwise.
        """

        if not self.enable: return False
        return self._rect.collidepoint(mouse_pos)

    def draw_collider(self, surface: pygame.Surface):

        """
        Draws the collider's shape onto the given surface.

        Does nothing in the base class; subclasses override this to
        render their specific shape (rectangle, circle, polygon, etc.).

        Args:
            surface (pygame.Surface): The surface to draw onto.
        """

        pass

class RectCollider(_Collider):

    """
    A rectangular collision shape.
    Draws its bounding area as a filled rectangle.
    """

    def __init__(self, 
                 tag: str, 
                 position = (0, 0), 
                 size_collider = (32, 32), 
                 color = None, 
                 enable = True,
                 visible = True):
        super().__init__(tag, 
                         position, 
                         size_collider, 
                         color,
                         enable, 
                         visible)

    def draw_collider(self, surface):
        if not self.visible: return 
        pygame.draw.rect(self._surf, self.color, self._surf.get_rect())
        surface.blit(self._surf, self._rect.topleft)

class CircleCollider(_Collider):

    """
    A circular collision shape.

    Collision detection still relies on the inherited rectangular
    bounding box (`rect`); `radius` only affects how the shape is
    drawn.

    Attributes:
        radius (float): The radius of the circle drawn for this
            collider.
    """

    def __init__(self, 
                 tag: str, 
                 radius: float = 16.,
                 position = (0, 0), 
                 size_collider = (32, 32), 
                 color = None, 
                 enable = True, 
                 visible = True):
        super().__init__(tag, 
                         position, 
                         size_collider, 
                         color, 
                         enable, 
                         visible)
        self.radius = radius

    def draw_collider(self, surface):
        if not self.visible: return
        pygame.draw.circle(self._surf, self.color, self.get_center_points(), self.radius)
        surface.blit(self._surf, self._rect.topleft)

class PolygonCollider(_Collider):

    """
    A polygonal collision shape.

    Collision detection still relies on the inherited rectangular
    bounding box (`rect`); `points` only affects how the shape is
    drawn.

    Attributes:
        points (list[tuple[int, int]]): The vertices of the polygon,
            in local coordinates relative to the collider's surface.
    """

    def __init__(self, 
                 tag: str, 
                 points: list[tuple[int, int]] = [
                     (0, 0),
                     (50, 0),
                     (50, 50),
                     (0, 50)
                 ],
                 position: tuple[int, int] = (0, 0),
                 size_collider = (32, 32), 
                 color = None, 
                 enable = True, 
                 visible = True):
        super().__init__(tag, 
                         position, 
                         size_collider, 
                         color, 
                         enable, 
                         visible)
        self.points = points

    def draw_collider(self, surface):
        if not self.visible: return
        pygame.draw.polygon(self._surf, self.color, self.points)
        surface.blit(self._surf, self._rect.topleft)
