"""
Handles input devices for the game, including keyboard and mouse.

Provides classes and utilities to detect key presses, mouse clicks,
mouse position, and other forms of player input, used throughout the
engine to drive gameplay, UI interaction, and scene logic.
"""

from .keyshort import KeyShort
from .manager import ManagerKeyShort

__all__ = ["KeyShort", "ManagerKeyShort"]