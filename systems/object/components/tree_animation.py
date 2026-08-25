import pygame
from typing import Optional

# Engine import 
from .animation import _Animation
from ...input import KeyShort

class TreeAnimation:

    """
    Manages a collection of named animations and switches between them.

    Acts as a state machine over multiple `_Animation` instances
    (e.g. `AnimationSheet`, `AnimationTexture`), rendering only the
    currently active one onto a given surface each frame. Useful for
    objects with multiple animation states, such as "idle", "walk",
    "attack", etc.

    Attributes:
        surface (pygame.Surface): The surface the active animation is
            drawn onto.
        current_name_animation (str): The tag of the animation
            currently active and being rendered.
    """

    def __init__(self, 
                 surface: pygame.Surface, 
                 init_name: str, 
                 /, 
                 *animations: _Animation):
        self.surface = surface
        self.current_name_animation = init_name
        self._list_animation: dict[str, _Animation] = {}
        self.register(*animations)

    def register(self, *animations: _Animation):

        """
        Adds one or more animations to the collection.

        Args:
            *animations (_Animation): One or more animation instances
                to register, keyed internally by their `tag`.
        """

        for index, animation in enumerate(animations):
            if not isinstance(animation, _Animation):
                raise ValueError(f"The animation at {index!r} is not an _Animation/AnimationSheet/AnimationTexture")

            if animation.tag in self._list_animation:
                raise KeyError(f"The {animation.tag!r} existed")

            self._list_animation[animation.tag] = animation

    def unregister(self, *animations: _Animation):

        """
        Removes one or more animations from the collection.

        Args:
            *animations (_Animation): One or more animation instances
                to remove, matched by their `tag`.
        """

        for index, animation in enumerate(animations):
            if not isinstance(animation, _Animation):
                raise ValueError(f"The animation at {index!r} is not an _Animation/AnimationSheet/AnimationTexture")

            if animation.tag not in self._list_animation:
                raise KeyError(f"The {animation.tag!r} is not existed")

            self._list_animation.pop(animation.tag)

    def switch(self, name_animation: str, event: Optional[KeyShort] = None):

        """
        Switches the currently active animation.

        If no event is given, switches immediately. If an event is
        given, the switch only happens when the event is triggered
        (`event.is_call()` returns True).

        Args:
            name_animation (str): The tag of the animation to switch to.
            event (Optional[KeyShort]): An optional input event that
                gates when the switch occurs. Defaults to None
                (switch immediately).
        """

        if name_animation not in self._list_animation:
            raise KeyError(f"The {name_animation!r} is not existed")

        if event is None:
            self.current_name_animation = name_animation
        else:
            if event.is_call():
                self.current_name_animation = name_animation 

    def update(self, speed: float = 1.):

        """
        Updates and renders the currently active animation.

        Does nothing if no animations are registered.

        Args:
            speed (float): A multiplier applied to the active
                animation's playback speed. Defaults to 1.0.
        """

        if not self._list_animation: return
        self._list_animation[self.current_name_animation].update(self.surface, speed) 
    

