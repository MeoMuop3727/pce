import pygame
from typing import Optional

# Engine import
from .collider import _Collider
from ...input import KeyShort

class ColliderGroup:

    """
    Manages a collection of named colliders and switches between them.

    Acts as a state machine over multiple `_Collider` instances (e.g.
    `RectCollider`, `CircleCollider`, `PolygonCollider`), rendering
    only the currently active one onto a given surface each frame.
    Useful for objects whose collision shape changes depending on
    state (e.g. crouching vs standing).

    Attributes:
        surface (pygame.Surface): The surface the active collider is
            drawn onto.
        current_name_collider (str): The tag of the collider currently
            active and rendered by `update`.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 init_name: str,
                 /,
                 *colliders: _Collider):
        self.surface = surface
        self.current_name_collider = init_name
        self._list_colliders: dict[str, _Collider] = {}
        self.register(*colliders)

    def register(self, *colliders: _Collider):

        """
        Adds one or more colliders to the collection.

        Args:
            *colliders (_Collider): One or more collider instances to
                register, keyed internally by their `tag`.
        """

        for index, collider in enumerate(colliders):
            if not isinstance(collider, _Collider):
                raise ValueError(f"The collider at {index!r} is not an _Collider/RectCollider/CircleCollider/PolygonCollider")

            if collider.tag in self._list_colliders:
                raise KeyError(f"The {collider.tag!r} existed")

            self._list_colliders[collider.tag] = collider

    def unregister(self, *colliders: _Collider):

        """
        Removes one or more colliders from the collection.

        Args:
            *colliders (_Collider): One or more collider instances to
                remove, matched by their `tag`.
        """

        for index, collider in enumerate(colliders):
            if not isinstance(collider, _Collider):
                raise ValueError(f"The collider at {index!r} is not an _Collider/RectCollider/CircleCollider/PolygonCollider")

            if collider.tag not in self._list_colliders:
                raise KeyError(f"The {collider.tag!r} is not existed")

            self._list_colliders.pop(collider.tag)

    def switch(self, name_collider: str, event: Optional[KeyShort] = None):

        """
        Switches the currently active collider.

        If no event is given, switches immediately. If an event is
        given, the switch only happens when the event is triggered
        (`event.is_call()` returns True).

        Args:
            name_collider (str): The tag of the collider to switch to.
            event (Optional[KeyShort]): An optional input event that
                gates when the switch occurs. Defaults to None
                (switch immediately).
        """

        if name_collider not in self._list_colliders:
            raise KeyError(f"The {name_collider!r} is not existed")

        if event is None:
            self.current_name_collider = name_collider
        else:
            if event.is_call():
                self.current_name_collider = name_collider

    def update(self):

        """
        Draws the currently active collider onto the given surface.
        Does nothing if no colliders are registered.

        Args:
            surface (pygame.Surface): The surface to draw the active
                collider onto.
        """

        if not self._list_colliders: return
        self._list_colliders[self.current_name_collider].draw_collider(self.surface)
