"""
Top-level package of the game engine, built on top of pygame.

This package brings together the core building blocks needed to
build a game from start to finish: reading player input, defining
and composing game objects (transforms, sprites, colliders,
animations, audio), handling both pygame's built-in events and the
engine's own custom events, and organizing the game into scenes with
their own lifecycle and update/render loop.

Rather than working with pygame's lower-level primitives directly,
this package wraps them into a more structured, reusable set of
classes and utilities, so that games, UI, and scenes can be composed
consistently on top of a common foundation.
"""

from .input import *
from .object import *
from .event import *
from .scene import *
