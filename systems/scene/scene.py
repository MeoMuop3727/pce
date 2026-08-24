from __future__ import annotations

import pygame

from typing import TYPE_CHECKING

# Engine import
if TYPE_CHECKING:
    from .manager import ManagerScene

class Scene:
    """
    Base class for a single screen/state of the game.

    Intended to be subclassed rather than used directly. A `Scene`
    represents one self-contained state of the game (e.g. main menu,
    gameplay, pause screen), and is driven by a `ManagerScene` which
    controls scene transitions and lifecycle calls. Subclasses
    override the relevant methods to implement their own logic,
    rendering, input handling, and lifecycle behavior.

    Attributes:
        (No public attributes; the owning manager is accessible via
        `self._manager`.)
    """

    def __init__(self, manager: ManagerScene):
        """
        Initializes the scene with a reference to its managing scene manager.

        Args:
            manager (ManagerScene): The manager responsible for this
                scene's lifecycle and transitions to/from other scenes.
        """
        self._manager = manager

    def update(self, dt: float):
        """
        Updates the scene's logic for the current frame.

        Called once per frame while the scene is active. Does
        nothing in the base class; subclasses override this to
        implement gameplay/UI logic.

        Args:
            dt (float): The elapsed time since the last frame, in
                seconds.
        """
        pass

    def render(self):
        """
        Renders the scene's visuals for the current frame.

        Called once per frame while the scene is active. Does
        nothing in the base class; subclasses override this to draw
        their content.
        """
        pass

    def events(self, event: pygame.event.Event):
        """
        Handles a single input/system event.

        Called for each pygame event while the scene is active. Does
        nothing in the base class; subclasses override this to react
        to input or other events.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        pass

    def on_enter(self):
        """
        Called when the scene becomes active.

        Invoked when the manager switches to this scene, before
        `update`/`render` begin being called. Does nothing in the
        base class; subclasses override this to set up state.
        """
        pass

    def on_exit(self):
        """
        Called when the scene stops being active.

        Invoked when the manager switches away from this scene.
        Does nothing in the base class; subclasses override this to
        tear down or clean up state.
        """
        pass

    def on_pause(self):
        """
        Called when the scene is paused but remains loaded.

        Invoked when another scene is pushed on top of this one
        (e.g. a pause menu), without fully exiting it. Does nothing
        in the base class; subclasses override this as needed.
        """
        pass

    def on_resume(self):
        """
        Called when the scene resumes after being paused.

        Invoked when the scene becomes active again after a scene
        that was on top of it is popped/removed. Does nothing in the
        base class; subclasses override this as needed.
        """
        pass