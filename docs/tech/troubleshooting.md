# Troubleshooting

This document provides guidance for diagnosing common problems when working with PCE.

PCE is currently under active development, so some APIs and recommended workflows may change over time. When troubleshooting an issue, always check the current implementation and documentation before assuming that behavior is a bug.

---

## 1. Environment

### Python Version

The current development environment uses:

```text
Python 3.12
```

Using another Python version may work, but it is not currently the primary development target.

If you encounter unexpected behavior, first verify the Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

### Pygame Version

PCE currently uses:

```text
pygame 2.6.1
```

Check the installed version with:

```bash
python -m pip show pygame
```

If multiple Python installations exist on your system, make sure Pygame is installed for the same Python interpreter that runs your project.

You can also check directly:

```bash
python -c "import pygame; print(pygame.version.ver)"
```

---

## 2. Installing PCE

PCE is currently intended to be used by cloning the repository into the project.

A typical project may look like:

```text
my_game/
├── pce/
├── game/
├── assets/
└── ...
```

After cloning PCE, install the required dependencies using the project's `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

The installation workflow may change in the future as PCE moves toward a more formal package/distribution system.

If you encounter import errors after cloning the repository, first verify that:

1. The PCE source directory is actually inside the project.
2. The Python interpreter is running from the expected project environment.
3. `requirements.txt` has been installed.
4. The import path matches the current repository structure.

---

# 3. `ManagerScene` Problems

## Only Use One `ManagerScene`

PCE is designed around a single `ManagerScene` controlling the game.

Although multiple managers may be technically possible in some situations, using multiple managers can lead to unexpected behavior because `ManagerScene` is responsible for:

* Pygame initialization
* The game window
* The main game loop
* Scene management
* Event dispatching

The recommended pattern is:

```python
manager = ManagerScene(...)

manager.push_scene(MainScene(manager))
manager.run()
```

Avoid creating independent managers for individual scenes.

---

## Do Not Reinitialize Pygame Manually

`pygame.init()` is already called when `ManagerScene` is defined.

Therefore, application code normally does not need to initialize Pygame again.

Prefer:

```python
manager = ManagerScene(...)
```

instead of repeatedly initializing Pygame throughout the application.

Keeping Pygame initialization under the manager also makes the engine lifecycle easier to control.

---

## The Game Window Exists but Does Not Respond

If the window appears but no interaction works, check the scene stack first.

A particularly important case is an empty scene stack.

---

# 4. Scene Stack Problems

## The Scene Stops Updating

If a scene appears to stop responding, check whether another scene has been placed above it.

PCE uses a scene stack.

Conceptually:

```text
Scene Stack
───────────────
GameplayScene
PauseScene       ← Active
```

The scene at the top of the stack is the active scene.

If an empty or transparent scene is pushed above the current scene, the underlying scene may appear to be frozen or paused.

For example:

```text
Scene Stack
───────────────
GameplayScene
EmptyScene       ← Active
```

If `EmptyScene` does not render anything, the user may see the previous frame of `GameplayScene` while being unable to interact with it.

### What to check

Check calls such as:

```python
manager.push_scene(...)
```

and verify which scene is currently active.

If a scene should no longer be active, consider:

```python
manager.pop_scene()
```

or:

```python
manager.replace(...)
```

depending on the desired behavior.

---

## The Window Shows the Last Frame but Nothing Responds

One possible cause is that the scene stack has become empty.

For example:

```text
Scene Stack
───────────────
(empty)
```

If the last scene has been removed, there is no active scene left to update or render.

The existing frame may remain visually present in the window even though no active scene is processing input or rendering new frames.

### What to check

Review scene removal logic:

```python
manager.pop_scene()
```

Make sure the application does not accidentally remove the final active scene.

If the game is expected to continue running after removing a scene, another scene should normally exist underneath it.

---

# 5. Nothing Is Being Rendered

If the game window appears correctly but the expected object is not visible, first check the scene's `render()` method.

A common mistake is forgetting to update the renderable object from `render()`.

For example:

```python
class GameScene(Scene):

    def render(self):
        self.player_sprite.update(self._manager._screen)
```

If the sprite is created but its rendering method is never called, the sprite will not appear.

---

## Rendering Checklist

If an object is not visible, check the following:

### 1. Does the scene implement `render()`?

```python
def render(self):
    ...
```

### 2. Is the sprite or animation updated inside `render()`?

For example:

```python
self.player_sprite.update(self._manager._screen)
```

### 3. Is the object visible?

Check the object's visibility state.

### 4. Is the transform positioned inside the visible screen?

For example:

```python
Transform(position=(640, 360))
```

for a `1280x720` window places the transform at the center of the screen.

### 5. Is the texture valid?

Make sure the texture/surface passed to the renderable object is valid.

---

# 6. Understanding `Transform` Position

PCE uses different positional conventions depending on the component.

`Transform` uses **top-left coordinates**.

However, `Sprite` and `Animation` use the transform position as their **center position** when rendering.

Conceptually:

```text
Transform
    position
       │
       ▼
  top-left reference


Sprite / Animation
       │
       ▼
  center reference
```

Therefore, the same transform position can produce different visual results depending on which component consumes it.

When debugging positioning problems, first identify whether you are reasoning about:

* the transform itself, or
* the rendered sprite/animation.

---

# 7. Transform Changes Do Not Automatically Update Existing Objects

One important behavior to understand is that replacing or changing the transform relationship is not equivalent to mutating the existing transform object.

If an object needs a new transform configuration, create a new `Transform` and assign it to the relevant object.

For example:

```python
new_transform = Transform(
    position=(400, 300)
)

sprite.transform = new_transform
```

The important point is that the object must reference the new `Transform`.

If you expect an object to automatically switch to a completely new transform without replacing its reference, the visual result may not be what you expect.

---

# 8. Keyboard Input Problems

## `KeyShort` Does Not Trigger

`KeyShort` is intended to be activated from the scene's `update()` method.

Recommended:

```python
def update(self, dt):
    self.key_short.active()
```

Do not move the call to an unrelated part of the application.

The shortcut is evaluated when `active()` is called.

---

## Multiple Keys Must Be Pressed Together

A `KeyShort` containing multiple keys represents a key combination.

For example:

```python
KeyShort(
    "save",
    save_game,
    Event.K_LCTRL,
    Event.K_s,
)
```

requires the configured keys to be pressed at the same time.

The order does not matter.

Conceptually:

```text
CTRL + S
```

and:

```text
S + CTRL
```

represent the same combination.

However:

```text
CTRL
```

alone is not enough.

Likewise:

```text
S
```

alone is not enough.

---

# 9. `Scene.events()` Problems

PCE's `ManagerScene` automatically dispatches Pygame events to the active scene.

Application code does not normally need to manually call:

```python
scene.events(event)
```

The manager handles this part of the game loop.

A scene can override:

```python
def events(self, event):
    ...
```

to process Pygame events.

For example:

```python
def events(self, event):
    if event.type == Event.KEYDOWN:
        if event.key == Event.K_ESCAPE:
            self._manager.running = False
```

---

## `Scene.events()` Is for Pygame Events

`Scene.events()` is intended for processing Pygame's event system.

Common examples include:

```python
Event.QUIT
Event.KEYDOWN
Event.KEYUP
```

The event type can be checked through:

```python
event.type
```

For example:

```python
if event.type == Event.KEYDOWN:
    ...
```

The actual event attributes depend on the Pygame event being processed.

---

# 10. `Event` Problems

PCE provides the `Event` interface so application code can access event constants through the engine.

For example:

```python
Event.KEYDOWN
Event.KEYUP
Event.QUIT
```

and keyboard constants such as:

```python
Event.K_ESCAPE
Event.K_LEFT
Event.K_RIGHT
```

When debugging an event-related issue, first check:

1. Whether the event is generated by Pygame.
2. Whether the event is being received by the active scene.
3. Whether `event.type` matches the expected event.
4. Whether the event-specific attributes are correct.

---

# 11. Animation Problems

PCE previously encountered an `IndexError` related to animation handling.

That issue has been fixed.

If an animation-related `IndexError` appears again, do not assume that the previous bug is still present.

Instead, check:

1. The current PCE version/commit.
2. The animation configuration.
3. The provided frames.
4. The traceback.
5. Whether the issue can be reproduced with a minimal example.

Animation behavior may continue to evolve as the engine develops.

---

# 12. File System

## File System Is Not a Complete Game Save System

The file-related code in PCE should not currently be treated as a complete, predefined save/load framework.

PCE is intended to provide foundational components that can be used to build a game-specific file system.

The actual data format and organization are left to the user or the game/framework built on top of PCE.

---

## There Is No Official File Format Yet

PCE does not currently require a single official data format.

A project may choose to use:

```text
JSON
YAML
TOML
Binary
Custom formats
```

depending on its requirements.

The exact format should be defined by the application or higher-level framework.

---

## The File Directory Must Be Defined by the User

The file system is intentionally not responsible for deciding the complete structure of a game's data directory.

The project should define its own structure.

For example:

```text
game/
├── assets/
├── data/
├── saves/
├── config/
└── ...
```

The exact structure depends on the application.

If a required directory does not exist, the user should first verify that the project has created it.

---

# 13. General Debugging Workflow

PCE currently does not have a dedicated debugging or logging system.

Until one is introduced, the recommended approach is to follow the normal Python debugging workflow.

---

## Step 1 — Read the Traceback

Do not skip the traceback.

Start from the bottom of the error and identify:

```text
Exception Type
Error Message
File
Line Number
```

For example:

```text
File "scene.py", line 42
    ...
IndexError: ...
```

The traceback usually provides the first concrete location where the failure occurred.

---

## Step 2 — Identify the PCE System

Determine which subsystem is involved.

For example:

```text
Scene
ManagerScene
Input
Event
Sprite
Transform
Animation
File
```

This significantly reduces the search area.

---

## Step 3 — Check the Scene Stack

If the game appears frozen, check:

```text
Is there an active scene?
Is another scene above the expected scene?
Was the last scene removed?
Is the active scene empty?
```

Scene-stack problems can look like rendering or input problems.

---

## Step 4 — Check `update()`

If input or game logic does not work, verify that the active scene's:

```python
update(dt)
```

is being executed.

For example:

```python
def update(self, dt):
    print("update")
```

If the message never appears, the problem is likely above the scene's own logic.

---

## Step 5 — Check `render()`

If the game logic works but nothing appears, verify:

```python
def render(self):
    ...
```

and confirm that the renderable object is actually updated/rendered.

For example:

```python
def render(self):
    self.sprite.update(self._manager._screen)
```

---

## Step 6 — Check Input

For keyboard problems, determine which input mechanism is being used:

```text
pygame.key.get_pressed()
        │
        └── Continuous input

KeyShort
        │
        └── Keyboard shortcuts

Scene.events()
        │
        └── Pygame events
```

Do not troubleshoot all three mechanisms as if they were the same system.

---

## Step 7 — Reduce the Problem

If the cause is unclear, remove unrelated systems.

For example, instead of debugging:

```text
Scene
+ GameObject
+ Animation
+ Audio
+ Input
+ File System
+ Multiple Scenes
```

reduce the problem to:

```text
ManagerScene
+ One Scene
+ One Sprite
```

Then gradually add systems back until the problem reappears.

This makes it much easier to identify the failing component.

---

# 14. Minimal Debugging Example

A minimal scene can be useful when determining whether the manager and scene loop are working correctly.

```python
from systems import Scene, ManagerScene


class DebugScene(Scene):

    def update(self, dt):
        print("Scene update:", dt)

    def render(self):
        pass


manager = ManagerScene()
manager.push_scene(DebugScene(manager))
manager.run()
```

If `Scene update:` is continuously printed, the scene is being updated.

If it is not printed, investigate:

* `ManagerScene`
* scene stack state
* whether the scene was successfully pushed
* whether the game loop is running

---

# 15. Known Issues

PCE is actively developed, and known issues may be fixed or changed between versions.

### Animation `IndexError`

A previous `IndexError` related to animation handling has been fixed.

If a similar error appears in a newer version, reproduce it and inspect the current traceback rather than relying on the previous issue.

### Multiple `ManagerScene` Instances

Using multiple `ManagerScene` instances is discouraged.

The recommended architecture is one manager controlling the entire game.

### Formal Installation Workflow

PCE currently does not provide a finalized installation/package workflow.

The current development workflow is based on cloning the repository and installing dependencies from `requirements.txt`.

A formal installation process may be introduced later.

### Dedicated Debug/Logging System

PCE does not currently provide a dedicated debugging or logging system.

A dedicated system may be introduced in a future version.

---

# 16. When Reporting a Bug

If the problem cannot be resolved using this guide, provide enough information to reproduce it.

A useful bug report should include:

```text
PCE version / commit:
Python version:
Pygame version:
Operating system:

Affected system:
Scene / Input / Event / Object / File / etc.

Expected behavior:
Actual behavior:

Traceback:
...

Minimal reproduction:
...
```

A minimal reproduction is strongly preferred over an entire game project.

For example:

```python
from systems import Scene, ManagerScene


class TestScene(Scene):

    def update(self, dt):
        # Reproduce the issue here.
        pass

    def render(self):
        pass


manager = ManagerScene()
manager.push_scene(TestScene(manager))
manager.run()
```

Reducing a problem to the smallest possible example makes debugging significantly easier.

---

# 17. Quick Troubleshooting Checklist

When something does not work as expected, check these items in order:

* [ ] Confirm Python is version 3.12.
* [ ] Confirm Pygame is version 2.6.1.
* [ ] Confirm dependencies from `requirements.txt` are installed.
* [ ] Confirm the PCE source is correctly included in the project.
* [ ] Confirm the game uses a single `ManagerScene`.
* [ ] Confirm `ManagerScene.run()` is running.
* [ ] Confirm the expected scene exists in the scene stack.
* [ ] Confirm the scene has not been accidentally paused or covered by another scene.
* [ ] Confirm the scene stack is not empty.
* [ ] Confirm `update(dt)` is being executed.
* [ ] Confirm `render()` is being executed.
* [ ] Confirm sprites/animations are updated from `render()`.
* [ ] Confirm input is being handled through the appropriate mechanism.
* [ ] Confirm `KeyShort.active()` is called from `update()`.
* [ ] Confirm multi-key shortcuts have all required keys pressed simultaneously.
* [ ] Confirm `Scene.events()` is being used for Pygame events.
* [ ] Confirm `Transform` and renderable-object positioning are understood correctly.
* [ ] Read the complete Python traceback before changing code.

---

# 18. Final Debugging Principle

When debugging PCE, start from the engine lifecycle and move downward:

```text
ManagerScene
     │
     ▼
Scene Stack
     │
     ▼
Active Scene
     │
     ├──────────────┐
     ▼              ▼
  update()       render()
     │              │
     ▼              ▼
 Input/Event      Sprite
     │              │
     ▼              ▼
 Game Logic      Transform
```

If a higher-level stage is not working, debugging lower-level components first may lead to incorrect conclusions.

For example, if `Sprite` does not render, first verify that:

1. The manager is running.
2. The scene is active.
3. `render()` is being called.
4. The sprite is updated from `render()`.
5. The transform and texture are valid.

Only after these are confirmed should the investigation move deeper into the rendering component.

As PCE develops, this document should be updated whenever a new subsystem, installation workflow, debugging system, or known issue is introduced.

---

<p align="center">Made with ❤️ using Python & Pygame</p>