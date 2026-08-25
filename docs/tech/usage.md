# Usage — Using PCE

This page covers the main modules in `systems/` and how they combine into a complete Scene, with an overall example followed by a breakdown of each part.

## Overall Example

```python
import pygame
from systems import (
    Scene, ManagerScene,
    KeyShort, Event,
    GameObject, Sprite, Transform
)

class PlayerScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        # A Sprite bound to a Transform (position, scale, rotation)
        texture = pygame.image.load("player.png").convert_alpha()
        self.player = Sprite(
            texture,
            transform=Transform(position=(640, 360))
        )

        # Key shortcut: press I -> print a message
        self.key_short = KeyShort(
            "debug-print",
            lambda: print("Playing PlayerScene"),
            Event.K_i
        )

    def update(self, dt):
        self.key_short.active()

    def render(self):
        self.player.update(self._manager._screen)

manager = ManagerScene(size_screen=(1280, 720), caption="My Game")
manager.push_scene(PlayerScene(manager))
manager.run()
```

Below is a breakdown of each component used in the example above, module by module.

## `systems.scene` — Scene Management

A **Scene** represents a single state/screen of the game (main menu, gameplay, pause screen, etc). `Scene` inherits from `GameObject` and is driven by a `ManagerScene`.

```python
class PlayerScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

    def update(self, dt): ...      # runs every frame — update logic
    def render(self): ...          # runs every frame — draw content
    def events(self, event): ...   # runs for every pygame event
    def on_enter(self): ...        # called when the scene becomes active
    def on_exit(self): ...         # called when the scene is removed from the stack
    def on_pause(self): ...        # called when another scene is pushed on top
    def on_resume(self): ...       # called when the scene above is popped, returning to this one
```

`ManagerScene` manages Scenes as a **stack** and drives the main game loop:

```python
manager = ManagerScene(
    size_screen=(1280, 720),   # window size
    caption="My Game",         # window title
    icon=None,                 # icon file path (optional)
    color_scene=None           # default background color (optional)
)

manager.push_scene(PlayerScene(manager))  # push a new scene on top, calls on_enter()
manager.pop_scene()                       # remove the top scene, calls on_exit()
manager.replace(OtherScene(manager))      # replace the current scene (pop then push)
manager.run(framerate=60)                 # run the main loop (defaults to 60 FPS)
```

> Each frame in `run()`: clears the screen → dispatches events to the active scene → calls `update()` → calls `render()` → `pygame.display.flip()`.

## `systems.object` — Components & Game Object

`GameObject` is the base class that groups components together: audio, animation, colliders, and connections. `Scene` is itself a special kind of `GameObject`.

The main components that can be attached to an object:

| Component | Role |
| --- | --- |
| `Transform` | Position (`position`), scale (`scale`), rotation (`rotation`) |
| `Sprite` | Wraps a Pygame texture, bound to a `Transform`, supports layers, flipping, alpha |
| `AnimationSheet` / `AnimationTexture` | Sprite-sheet based animation system |
| `AudioSFX` / `AudioMusic` | Sound effects / background music |
| `RectCollider` / `CircleCollider` / `PolygonCollider` | Rectangle / circle / polygon collision shapes |
| `Connection` | A link/connection between objects |

Example of creating a standalone `Sprite` with a custom `Transform`:

```python
transform = Transform(position=(400, 300), scale=(2.0, 2.0), rotation=45)
sprite = Sprite(texture, transform=transform, layer=1, alpha=200)

# Call update() every frame to draw the sprite to the screen
sprite.update(screen)
```

## `systems.input` / `systems.event` — Key Shortcuts & Events

`KeyShort` creates a key combination bound to a callback, triggered when all the given keys are pressed together:

```python
from systems import KeyShort, Event

key_short = KeyShort(
    "save-game",                     # identifier id, used for management/removal
    lambda: print("Game saved!"),    # callback triggered when the combo is active
    Event.K_LCTRL, Event.K_s         # key combo: Ctrl + S
)

# Call this in update() every frame to check and trigger the shortcut
key_short.active()
```

`Event` provides both the engine's and Pygame's native key/event codes, used instead of calling `pygame.K_*` directly.

## `systems.file` — File Abstraction

Provides an abstract base for reading/writing files — requires **subclassing and custom implementation** based on your project's needs (e.g. save-game format, config loading).

## `utils` — Additional Utilities

A library of internal helper functions used across the engine (e.g. random ID generation for `GameObject`, shared helpers).

---

<p align="center">Made with ❤️ using Python & Pygame</p>