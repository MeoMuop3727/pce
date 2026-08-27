"""
Public entry point for the engine's scene system.

Provides the building blocks for organizing a game into discrete
screens/states (menus, gameplay, pause screens, etc.):

    Scene: Base class representing a single screen/state of the
        game. Subclassed by users to implement their own scenes,
        overriding lifecycle hooks (`on_enter`, `on_exit`, `on_pause`,
        `on_resume`) and per-frame behavior (`update`, `render`,
        `events`).
    ManagerScene: Owns the game window and drives the main game loop,
        managing a stack of `Scene` instances via `push_scene`,
        `pop_scene`, and `replace`.

Typical usage is to create one `ManagerScene`, push an initial
`Scene` onto it, then call `ManagerScene.run()` to start the game
loop.
"""

from .manager import ManagerScene
from .scene import Scene

__all__ = ["Scene", "ManagerScene"]
