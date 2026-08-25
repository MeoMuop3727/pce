# API Reference

API reference for every module in `systems/` and `utils/`. For detailed usage examples, see [`usage.md`](../tech/usage_EN.md).

> A class whose name starts with `_` (e.g. `_Animation`, `_Audio`, `_Collider`) is an **internal base class** and is not meant to be used directly — use its subclasses instead.

---

## `systems.scene`

### `ManagerScene` — main class

Owns the game window and manages the scene stack, driving the main game loop.

```python
ManagerScene(
    size_screen: tuple[int, int] = (1280, 720),
    caption: Optional[str] = None,
    icon: Optional[str] = None,
    color_scene: Optional[pygame.Color] = None
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `size_screen` | `tuple[int, int]` | `(1280, 720)` | Window size `(width, height)` |
| `caption` | `Optional[str]` | `"My Game"` | Window title |
| `icon` | `Optional[str]` | `None` | File path to the window icon |
| `color_scene` | `Optional[pygame.Color]` | opaque white | Default background color used to clear the screen each frame |

**Attributes:** `color_scene: pygame.Color`, `running: bool`

**Methods:**

| Method | Description |
| --- | --- |
| `push_scene(scene: Scene)` | Pushes a new scene onto the top of the stack, calls `on_enter()` |
| `pop_scene()` | Removes the top scene from the stack, calls `on_exit()` |
| `replace(scene: Scene)` | Replaces the current scene (pop then push) |
| `run(framerate: int = 60)` | Runs the main loop until `running` is `False` |

### `Scene` — main class

```python
Scene(manager: ManagerScene, /, audios: Optional[TreeAudio] = None)
```

Inherits from `GameObject`. Represents a single state/screen of the game, driven by a `ManagerScene`'s lifecycle calls.

| Method (lifecycle) | Called when |
| --- | --- |
| `update(dt: float)` | Every frame, while the scene is active |
| `render()` | Every frame, after `update()` |
| `events(event: pygame.event.Event)` | For every pygame event, while the scene is active |
| `on_enter()` | When the scene is pushed via `push_scene` |
| `on_exit()` | When the scene is removed via `pop_scene` |
| `on_pause()` | When another scene is pushed on top of it |
| `on_resume()` | When the scene above it is popped, returning to this one |

---

## `systems.object`

### `GameObject` — main class

The base class for every entity in the game (including `Scene`), grouping components together.

```python
GameObject(
    surface: Optional[pygame.Surface] = None,
    audios: Optional[TreeAudio] = None,
    animations: Optional[TreeAnimation] = None,
    colliders: Optional[ColliderGroup] = None,
    connections: Optional[ConnectionGroup] = None
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `surface` | `Optional[pygame.Surface]` | `None` | The surface bound to this object |
| `audios` | `Optional[TreeAudio]` | empty `TreeAudio` | The object's audio group |
| `animations` | `Optional[TreeAnimation]` | empty `TreeAnimation` | The object's animation group |
| `colliders` | `Optional[ColliderGroup]` | empty `ColliderGroup` | The object's collider group |
| `connections` | `Optional[ConnectionGroup]` | empty `ConnectionGroup` | The object's connection group |

**Method:** `get_id() -> str` — returns the object's identifier ID.

### Secondary classes (components)

```python
Identify(_id: str, name: str)
# property: id (get/set)

Transform(
    position: tuple[int, int] = (0, 0),
    scale: tuple[float, float] = (1.0, 1.0),
    rotation: float = 0.0
)

Sprite(
    texture: pygame.Surface,
    transform: Optional[Transform] = None,
    layer: int = 1,
    flip: tuple[bool, bool] = (False, False),
    visible: bool = True,
    alpha: int = 255
)
# method: set_texture() -> pygame.Surface
# method: update(screen: pygame.Surface)
# property: texture (get/set)

AnimationSheet(
    tag: str,
    path_sheet: str,
    size_frame: tuple[int, int] = (32, 32),
    count: int = 0,
    transform: Optional[Transform] = None,
    flip: tuple[bool, bool] = (False, False),
    visible: bool = True,
    layer: int = 1,
    alpha: int = 255,
    loop: bool = True,
    duration: float = 0.1,
    dt: float = 0.1,
    playing: bool = True
)
# Cuts frames from a single sprite sheet (in a single row)

AnimationTexture(
    tag: str,
    transform: Optional[Transform] = None,
    flip: tuple[bool, bool] = (False, False),
    visible: bool = True,
    layer: int = 1,
    alpha: int = 255,
    loop: bool = True,
    duration: float = 0.1,
    dt: float = 0.1,
    playing: bool = True
)
# method: add_texture(*textures: pygame.Surface)

# Both AnimationSheet/AnimationTexture also have:
# method: update(surface: pygame.Surface, speed: float = 1.)
# property: tag

AudioSFX(tag: str, path: str, volume: float = 1., loop: bool = False)
# method: play(), stop(), set_volume(new_volume, /), fadeout(ms, /)

AudioMusic(tag: str, path: str, volume: float = 1., loop: bool = False)
# method: play(), stop(), pause(), unpause(), set_volume(new_volume, /), fadeout(ms, /)

RectCollider(
    tag: str,
    position: tuple[int, int] = (0, 0),
    size_collider: tuple[int, int] = (32, 32),
    color: Optional[pygame.Color] = None,
    enable: bool = True,
    visible: bool = True
)

CircleCollider(
    tag: str,
    radius: float = 16.,
    position: tuple[int, int] = (0, 0),
    size_collider: tuple[int, int] = (32, 32),
    color: Optional[pygame.Color] = None,
    enable: bool = True,
    visible: bool = True
)

PolygonCollider(
    tag: str,
    points: list[tuple[int, int]] = [(0, 0), (50, 0), (50, 50), (0, 50)],
    position: tuple[int, int] = (0, 0),
    size_collider: tuple[int, int] = (32, 32),
    color: Optional[pygame.Color] = None,
    enable: bool = True,
    visible: bool = True
)

# All 3 Collider classes also have:
# method: distance(other), is_collider_with(other) -> bool,
#         is_collider_with_mouse(mouse_pos) -> bool, draw_collider(surface)
# property: rect, tag

Connection(
    target: Optional[Identify] = None,
    event: Optional[int] = None,
    action: Optional[Callable[[], None]] = None
)

ColliderGroup(surface: pygame.Surface, init_name: str, /, *colliders: _Collider)
# method: register(*colliders), unregister(*colliders),
#         switch(name_collider, event=None), update()

TreeAnimation(surface: pygame.Surface, init_name: str, /, *animations: _Animation)
# method: register(*animations), unregister(*animations),
#         switch(name_animation, event=None), update(speed=1.)

TreeAudio(init_name: str, /, *audios: _Audio)
# method: register(*audios), unregister(*audios),
#         switch(name_audio, event=None, ms=1.), play(), pause(),
#         unpause(), stop(), set_volume(new_volume)

ConnectionGroup(*connections: Connection)
# method: register(*connections), unregister(*connections),
#         get(target) -> Connection, active_action(target)
```

---

## `systems.input`

### `KeyShort` — main class

```python
KeyShort(
    tag: str,
    event: Optional[Callable[[], None]] = None,
    /,
    *keys: int
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `tag` | `str` | — | Identifier for this key combination |
| `event` | `Optional[Callable[[], None]]` | `None` | Callback triggered when the combination is active |
| `*keys` | `int` | — | The key codes (`Event.K_*`) that make up the combination |

**Methods:**

| Method | Description |
| --- | --- |
| `is_call() -> bool` | Checks whether every key in the combination is currently pressed |
| `active()` | Calls `event` if `is_call()` returns `True` |

### Secondary class

```python
ManagerKeyShort()
# method: register(*keys_short), unregister(*keys_short),
#         get_keys_short() -> dict[str, KeyShort],
#         get(name) -> KeyShort, update()
```

---

## `systems.event`

`Event` is a class **generated automatically** at import time, combining every native Pygame event constant (e.g. `Event.QUIT`, `Event.KEYDOWN`, `Event.K_i`) together with the engine's own custom events (e.g. `Event.HOVER`) into a single interface.

```python
from systems import Event

Event.K_i        # equivalent to pygame.K_i
Event.QUIT        # equivalent to pygame.QUIT
Event.HOVER       # the engine's own custom event
```

> `EventRegistry` is an internal API used to allocate IDs for custom events — not intended for direct use.

---

## `systems.file`

Both classes are **abstract base classes**, requiring subclassing and a full implementation of every abstract method.

```python
class FileSystem(ABC):
    def exists(self, path: str) -> bool: ...
    def read(self, path: str) -> Any: ...
    def write(self, path: str, data: Any) -> None: ...
    def update(self, path: str, data: Any) -> None: ...
    def delete(self, path: str) -> None: ...
    def create(self, path: str, data: Any) -> None: ...

class Serializer(ABC):
    def encode(self, data: Any) -> bytes: ...
    def decode(self, data: bytes) -> Any: ...
```

---

## `utils`

Internal helper functions used across the engine, importable directly from `utils.tools`.

```python
apply_instance(obj: _T, var: Optional[_T] = None) -> Union[_T, object]
# Returns obj if var is None, otherwise returns var

generate_id(length: int, /) -> str
# Generates a random alphanumeric ID of the given length

hash_id(_id: str, /, a: int = 1, b: int = 51) -> int
# Hashes _id into an integer within the range [a, b)

generate_rgba() -> pygame.Color
# Generates a random RGBA color
```

---

<p align="center">Made with ❤️ using Python & Pygame</p>