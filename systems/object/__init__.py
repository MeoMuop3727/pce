"""
Provides the game object system, the foundation used to construct
UI elements, scenes, and other in-game entities.

Contains the core object classes/components (e.g. identification,
transform, sprites, colliders, animations) that combine to define
the behavior and appearance of anything placed in a scene.
"""

from .identify import Identify
from .components import *