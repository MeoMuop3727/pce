"""
Top-level package containing the core building blocks of the game
engine: game object, input handling, and other systems used to
construct games, UI, and scenes, etc.

Subpackages:
    input: Handles input devices such as keyboard and mouse, exposing
        classes and utilities to read and react to player input.
    object: Provides the game object system used to build UI, scenes,
        and other in-game entities.
"""

from .input import *
from .object import *
from .event import *
