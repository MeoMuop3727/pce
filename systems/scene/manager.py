import pygame, sys
from pathlib import Path
from typing import Optional

# Engine import
from .scene import Scene

class ManagerScene:

    """
    Owns the game window and manages the stack of active scenes.

    Initializes pygame and the display window once, then drives the
    main game loop: handling events, updating, and rendering the
    currently active scene each frame. Scenes are stored as a stack,
    so pushing a new scene layers it on top of the current one (e.g.
    a pause menu over gameplay), while popping removes the top scene
    and returns to the one beneath it.

    Attributes:
        color_scene (pygame.Color): The default background color
            used to clear the screen each frame before rendering the
            active scene.
        running (bool): Whether the main game loop should continue
            running.
    Example:
    >>> class TestScene(Scene):
            def __init__(self, manager):
                super().__init__(manager)
        manager = ManagerScene()
        manager.push_scene(TestScene(manager))
        manager.run()
    """

    def __init__(self,
                 size_screen: tuple[int, int] = (1280, 720),
                 caption: Optional[str] = None,
                 icon: Optional[str] = None,
                 color_scene: Optional[pygame.Color] = None):

        """
        Initializes pygame and creates the game window.

        This should only be instantiated once per game, as it calls
        `pygame.init()` and sets up the display.

        Args:
            size_screen (tuple[int, int]): The (width, height) of the
                game window. Defaults to (1280, 720).
            caption (Optional[str]): The window title. Defaults to
                "My Game" if not given.
            icon (Optional[str]): File path to an image used as the
                window icon. Defaults to None (no custom icon).
            color_scene (Optional[pygame.Color]): The default
                background color to clear the screen with. Defaults
                to opaque white if not given.
        """

        pygame.init()   # Init all in ManageScene
                        # Only using one manage in during the game

        self._screen = pygame.display.set_mode(size_screen, pygame.SRCALPHA)

        pygame.display.set_caption("My Game" if caption is None else caption)
        if icon is not None:
            if not Path(icon).exists():
                raise FileNotFoundError(f"Cannot find the file icon at: {icon!r}")
            else:
                pygame.display.set_icon(pygame.image.load(icon).convert_alpha())

        # The color default to draw onto the screen when nothing on the screen
        self.color_scene = pygame.Color(255, 255, 255, 255) if color_scene is None else color_scene

        # Using list (like stack object) to store all scene of game
        # Using push to add new scene, new scene will be played (or replaced) the current scene
        # Using pop to remove a top scene, the next scene will be played
        self._list_scene: list[Scene] = []

        # FPS of game
        self._clock = pygame.time.Clock()

        # Running game
        self.running = True

    def push_scene(self, scene: Scene):

        """
        Pushes a new scene onto the top of the scene stack.

        The new scene becomes the active scene, layered on top of
        any existing scenes, and its `on_enter` callback is invoked.

        Args:
            scene (Scene): The scene to push.
        """

        if not isinstance(scene, Scene):
            raise TypeError(f"The value must be a 'Scene', not {type(scene)!r}")
        self._list_scene.append(scene)
        scene.on_enter()

    def pop_scene(self):

        """
        Removes the top scene from the scene stack.

        Invokes the removed scene's `on_exit` callback. Does nothing
        if the stack is empty. After popping, the scene beneath (if
        any) becomes active again.
        """

        if not self._list_scene: return
        scene = self._list_scene.pop() 
        scene.on_exit()

    def replace(self, scene: Scene):

        """
        Replaces the current top scene with a new one.

        Equivalent to popping the current top scene and pushing the
        given scene.

        Args:
            scene (Scene): The scene to replace the current one with.
        """

        if not isinstance(scene, Scene):
            raise TypeError(f"The value must be a 'Scene', not {type(scene).__name__!r}")
        self.pop_scene()
        self.push_scene(scene)

    def run(self, framerate: int = 60):

        """
        Runs the main game loop until `running` is set to False.

        Each frame: clears the screen with `color_scene`, dispatches
        pygame events to the active (topmost) scene, checks for the
        quit event, then updates and renders the active scene before
        flipping the display. Calls `pygame.quit()` and exits the
        process once the loop ends.

        Args:
            framerate (int): The target frames per second to cap the
                loop at. Defaults to 60.
        """

        while self.running:
            dt = self._clock.tick(framerate) / 1e3

            self._screen.fill(self.color_scene)

            if not self._list_scene: continue
            current_scene = self._list_scene[-1]

            for event in pygame.event.get():
                current_scene.events(event)

                # Quit game
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.running: break

            current_scene.update(dt)
            current_scene.render()
                    
            pygame.display.flip()

        pygame.quit()
        sys.exit()