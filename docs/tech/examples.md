# Examples

This page contains small, practical examples demonstrating how the current PCE systems can be used together.

The examples focus on the core systems currently available in PCE, especially:

* `ManagerScene`
* `Scene`
* `GameObject`
* `Transform`
* `Sprite`
* `KeyShort`
* `Event`

The goal is to show how these systems fit together rather than hide the engine behind additional abstractions.

---

## Minimal Example: Moving a Square

This example creates a simple Pygame window containing a blue square.

The square can be moved using:

* Arrow keys
* WASD

Press **ESC** to stop the game.

The example demonstrates the basic relationship between a scene, a transform, a sprite, keyboard input, and the scene manager.

### Complete Example

```python
"""
Minimal example: a movable square controlled by the arrow keys / WASD.

Press ESC to stop the game.

This example demonstrates how Scene, ManagerScene, Sprite,
Transform, KeyShort, and Event work together.
"""

import pygame

from systems import (
    Scene,
    ManagerScene,
    Sprite,
    Transform,
    KeyShort,
    Event,
)


def make_square_texture(color, size=64):
    """Create a simple square texture without requiring an image file."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(color)
    return surface


class PlayerScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        # Create the player's transform.
        self.player_transform = Transform(
            position=(640, 360)
        )

        # Create a sprite using the player's transform.
        self.player_sprite = Sprite(
            make_square_texture((66, 135, 245, 255)),
            transform=self.player_transform,
        )

        # Movement speed in pixels per second.
        self.speed = 300

        # Create a keyboard shortcut for quitting the game.
        self.key_quit = KeyShort(
            "quit-game",
            lambda: setattr(self._manager, "running", False),
            Event.K_ESCAPE,
        )

    def update(self, dt):
        self.key_quit.active()

        keys = pygame.key.get_pressed()

        x, y = self.player_transform.position

        if keys[Event.K_LEFT] or keys[Event.K_a]:
            x -= self.speed * dt

        if keys[Event.K_RIGHT] or keys[Event.K_d]:
            x += self.speed * dt

        if keys[Event.K_UP] or keys[Event.K_w]:
            y -= self.speed * dt

        if keys[Event.K_DOWN] or keys[Event.K_s]:
            y += self.speed * dt

        self.player_transform.position = (x, y)

    def render(self):
        self.player_sprite.update(self._manager._screen)


if __name__ == "__main__":
    manager = ManagerScene(
        size_screen=(1280, 720),
        caption="PCE Example - Move the Square",
    )

    manager.push_scene(PlayerScene(manager))
    manager.run()
```

---

## 1. Creating the Scene Manager

Every PCE application starts by creating a `ManagerScene`.

```python
manager = ManagerScene(
    size_screen=(1280, 720),
    caption="PCE Example - Move the Square",
)
```

`ManagerScene` initializes Pygame, creates the display surface, maintains the scene stack, and owns the main game loop.

The current implementation also accepts optional parameters such as:

* `size_screen`
* `caption`
* `icon`
* `color_scene`

The default target framerate of `run()` is 60 FPS.

A single `ManagerScene` should normally be used for a game because it owns the Pygame initialization and display.

---

## 2. Creating a Scene

Game logic is normally implemented by subclassing `Scene`.

```python
class PlayerScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
```

A `Scene` represents one game state or screen.

For example, a project can have scenes such as:

```text
MainMenuScene
GameplayScene
PauseScene
SettingsScene
```

The base `Scene` provides several lifecycle methods:

```python
update(dt)
render()
events(event)
on_enter()
on_exit()
on_pause()
on_resume()
```

These methods are intentionally empty in the base class and are meant to be overridden by subclasses.

---

## 3. Creating a Transform

The player's spatial state is represented by a `Transform`.

```python
self.player_transform = Transform(
    position=(640, 360)
)
```

The current `Transform` component stores three values:

```text
position
scale
rotation
```

For example:

```python
Transform(
    position=(640, 360),
    scale=(1.0, 1.0),
    rotation=0.0,
)
```

The defaults are:

```text
position = (0, 0)
scale    = (1.0, 1.0)
rotation = 0.0
```

`rotation` is expressed in degrees.

---

## 4. Creating a Sprite

A `Sprite` wraps a Pygame `Surface` and uses a `Transform` to determine how the texture is rendered.

```python
self.player_sprite = Sprite(
    make_square_texture((66, 135, 245, 255)),
    transform=self.player_transform,
)
```

The important relationship is:

```text
Transform
    │
    ├── position
    ├── scale
    └── rotation
          │
          ▼
       Sprite
          │
          ▼
       Texture
```

The sprite uses the transform's position as the **center** of the rendered texture.

The sprite also currently supports properties such as:

* `layer`
* `flip`
* `visible`
* `alpha`
* `texture`

For example:

```python
sprite = Sprite(
    texture,
    transform=Transform(position=(400, 300)),
    layer=2,
    flip=(True, False),
    visible=True,
    alpha=255,
)
```

---

## 5. Creating a Texture Without an Image File

For a minimal example, an external image file is unnecessary.

Pygame can create a surface directly:

```python
def make_square_texture(color, size=64):
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    surface.fill(color)
    return surface
```

The result can then be passed directly to `Sprite`.

This is useful for testing the engine because the example does not depend on an asset directory.

---

## 6. Handling Keyboard Shortcuts with `KeyShort`

PCE provides `KeyShort` for simple keyboard combinations.

```python
self.key_quit = KeyShort(
    "quit-game",
    lambda: setattr(self._manager, "running", False),
    Event.K_ESCAPE,
)
```

The constructor has the following general structure:

```python
KeyShort(
    tag,
    callback,
    *keys,
)
```

`KeyShort` checks whether all specified keys are currently pressed.

For example:

```python
jump = KeyShort(
    "jump",
    jump_player,
    Event.K_SPACE,
)
```

A multi-key combination can also be defined:

```python
shortcut = KeyShort(
    "special-action",
    perform_action,
    Event.K_LCTRL,
    Event.K_s,
)
```

The callback is executed when the complete key combination is active.

---

## 7. Using `Event`

PCE's `Event` class provides access to engine-registered events and falls back to Pygame event attributes.

For keyboard constants, the example can use:

```python
Event.K_LEFT
Event.K_RIGHT
Event.K_UP
Event.K_DOWN

Event.K_w
Event.K_a
Event.K_s
Event.K_d
```

The event system is implemented through a metaclass and an event registry. If an attribute is not found in the engine registry, PCE attempts to resolve it from Pygame.

This allows application code to use `Event` as a common event/key interface instead of accessing Pygame constants everywhere.

---

## 8. Updating the Player

The `Scene.update()` method receives `dt`, the elapsed time since the previous frame.

```python
def update(self, dt):
    ...
```

The player's position is updated using:

```python
self.speed * dt
```

For example:

```python
if keys[Event.K_RIGHT]:
    x += self.speed * dt
```

If:

```text
speed = 300 pixels/second
dt    = 0.016 seconds
```

the movement for that frame is approximately:

```text
300 × 0.016 = 4.8 pixels
```

Using `dt` makes movement based on elapsed time rather than directly on the number of rendered frames.

---

## 9. Rendering the Sprite

The scene's `render()` method calls the sprite:

```python
def render(self):
    self.player_sprite.update(self._manager._screen)
```

`Sprite.update()`:

1. Checks whether the sprite is visible.
2. Applies alpha.
3. Applies scale.
4. Applies flipping.
5. Applies rotation.
6. Positions the resulting surface using the transform's position.
7. Blits it onto the target surface.

The scene therefore does not need to manually calculate the sprite's rectangle.

---

## 10. Adding a Scene to the Manager

A scene is added using:

```python
manager.push_scene(PlayerScene(manager))
```

`ManagerScene` stores scenes in a stack.

When a scene is pushed:

```text
Scene Stack
───────────
PlayerScene  ← Active
```

The new scene becomes the active scene and its `on_enter()` method is called.

This stack-based design allows multiple game states to coexist.

For example:

```text
GameplayScene
     │
     ▼
PauseScene
```

The pause scene can be pushed above the gameplay scene.

---

## 11. Scene Stack Operations

The current `ManagerScene` provides three primary scene-stack operations.

### Push

```python
manager.push_scene(scene)
```

Adds a new scene to the top of the stack.

The new scene becomes active and receives `on_enter()`.

### Pop

```python
manager.pop_scene()
```

Removes the active scene.

The removed scene receives `on_exit()`, and the scene underneath becomes active again.

### Replace

```python
manager.replace(scene)
```

Replaces the current scene with another scene.

Conceptually:

```text
Before:

GameplayScene
PauseScene  ← Active


After replace:

GameplayScene
SettingsScene  ← Active
```

`replace()` is implemented as a pop followed by a push.

---

## 12. The Scene Lifecycle

PCE provides lifecycle hooks that can be overridden when a scene needs setup or cleanup logic.

```text
              push_scene()
                   │
                   ▼
              on_enter()
                   │
                   ▼
            ┌─────────────┐
            │   Active    │
            │    Scene    │
            └─────────────┘
              │         │
          update()    render()
              │
              ▼
         push another
            scene
              │
              ▼
          on_pause()
              │
              ▼
       Scene remains loaded
              │
              ▼
        pop upper scene
              │
              ▼
          on_resume()
```

When a scene is completely removed:

```text
Active Scene
     │
     ▼
  on_exit()
     │
     ▼
Removed
```

These lifecycle methods are part of the current `Scene` API.

---

## 13. The Main Game Loop

Calling:

```python
manager.run()
```

starts the PCE game loop.

The current implementation follows this general sequence:

```text
ManagerScene.run()
       │
       ▼
Calculate dt
       │
       ▼
Clear screen
       │
       ▼
Get active scene
       │
       ▼
Read pygame events
       │
       ▼
Scene.events(event)
       │
       ▼
Check pygame.QUIT
       │
       ▼
Scene.update(dt)
       │
       ▼
Scene.render()
       │
       ▼
Display frame
       │
       ▼
Repeat
```

The loop uses `pygame.time.Clock()` to calculate `dt` and cap the target framerate. The default framerate is 60 FPS.

---

## 14. Using `Scene.events()`

The current PCE scene API includes an `events()` method:

```python
def events(self, event):
    ...
```

`ManagerScene.run()` forwards each Pygame event to the active scene:

```python
current_scene.events(event)
```

This makes `Scene.events()` the appropriate place for event-based input handling.

For example:

```python
def events(self, event):
    if event.type == Event.KEYDOWN:
        if event.key == Event.K_ESCAPE:
            self._manager.running = False
```

This is different from `KeyShort`.

Use `Scene.events()` when the application needs to react to individual Pygame events.

Use `KeyShort` when the application needs a simple "while these keys are pressed" shortcut.

---

## 15. `KeyShort` vs `Scene.events()`

These two mechanisms serve different purposes.

| Mechanism                  | Best suited for                         |
| -------------------------- | --------------------------------------- |
| `KeyShort`                 | Keyboard shortcuts and key combinations |
| `Scene.events()`           | Individual Pygame events                |
| `pygame.key.get_pressed()` | Continuous movement/input state         |

For example:

### Continuous movement

```python
keys = pygame.key.get_pressed()

if keys[Event.K_RIGHT]:
    x += speed * dt
```

### Shortcut

```python
save_shortcut = KeyShort(
    "save",
    save_game,
    Event.K_LCTRL,
    Event.K_s,
)
```

### Event handling

```python
def events(self, event):
    if event.type == Event.KEYDOWN:
        ...
```

Keeping these responsibilities separate makes scene code easier to organize.

---

## 16. Example: Scene Lifecycle

The following example demonstrates the lifecycle hooks without introducing additional engine systems.

```python
from systems import Scene, ManagerScene


class ExampleScene(Scene):
    def on_enter(self):
        print("Scene entered")

    def update(self, dt):
        pass

    def render(self):
        pass

    def on_exit(self):
        print("Scene exited")


manager = ManagerScene()
manager.push_scene(ExampleScene(manager))
manager.run()
```

When the scene is pushed, `on_enter()` is called automatically.

When the scene is popped or replaced, `on_exit()` is called.

---

## 17. Example: Two Scenes

The scene stack can be used to separate different game states.

```python
from systems import Scene, ManagerScene


class MenuScene(Scene):
    def update(self, dt):
        pass

    def render(self):
        pass


class GameScene(Scene):
    def update(self, dt):
        pass

    def render(self):
        pass


manager = ManagerScene()

menu = MenuScene(manager)
game = GameScene(manager)

manager.push_scene(menu)

# Later:
manager.replace(game)

manager.run()
```

A typical application structure can therefore look like:

```text
ManagerScene
     │
     └── Scene Stack
           │
           ├── MainMenuScene
           │
           ├── GameplayScene
           │
           └── PauseScene
```

The exact scene structure is application-dependent.

---

## 18. Current Core Building Blocks

The current `systems` package is organized around several focused areas.

```text
systems/
├── event/
├── file/
├── input/
├── object/
│   └── components/
└── scene/
```

The object components currently include:

```text
Animation
Audio
Collider
ColliderGroup
Connection
ConnectionGroup
Sprite
Transform
TreeAnimation
TreeAudio
```

These are the building blocks that can be used by higher-level game systems.

---

## Next Steps

After understanding the minimal example, the most useful next examples should follow the systems that already exist in PCE.

### Recommended Example Order

1. **Scene lifecycle**

   * `on_enter()`
   * `on_exit()`
   * `on_pause()`
   * `on_resume()`

2. **Scene stack**

   * `push_scene()`
   * `pop_scene()`
   * `replace()`

3. **Event handling**

   * `Scene.events()`
   * `Event`
   * Pygame event dispatch

4. **Keyboard input**

   * `KeyShort`
   * `ManagerKeyShort`
   * key combinations

5. **Object components**

   * `Transform`
   * `Sprite`
   * sprite visibility
   * alpha
   * scale
   * rotation
   * flipping

6. **Object composition**

   * `GameObject`
   * component groups
   * object IDs

7. **File system**

   * file creation
   * reading
   * writing
   * modification
   * deletion
   * data persistence

8. **Event registration**

   * engine events
   * custom event registration
   * event registry

These examples should be added as the corresponding APIs become stable enough to document.

---

## Related Documentation

For a deeper explanation of the current API, see:

* `docs/tech/usage.md` — common usage patterns
* `docs/tech/api.md` — API reference
* `docs/tech/faq.md` — frequently asked questions
* `docs/tech/troubleshooting.md` — common problems and solutions
* `docs/contributor/architecture.md` — internal architecture

---

<p align="center">Made with ❤️ using Python & Pygame</p>