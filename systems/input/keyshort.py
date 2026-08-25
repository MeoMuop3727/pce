import pygame
from typing import Callable, Optional

class KeyShort:

    """
    Represents a keyboard shortcut combination associated with a 
    callback function that is invoked when that combination is pressed.
    """

    def __init__(self,
                 tag: str,
                 event: Optional[Callable[[], None]] = None,
                 /,
                 *keys: int):
        self.tag = tag
        self.event = event
        self._keys = keys 

    def is_call(self) -> bool:

        """
        Check whether all keys in the combination are currently being pressed.
        """

        if not self._keys: return

        pressed = pygame.key.get_pressed()
        return all([pressed[key] for key in self._keys])

    def active(self):

        """
        Call the callback if the key combination is being pressed.
        """

        if self.event is None: return
        if self.is_call(): self.event()
