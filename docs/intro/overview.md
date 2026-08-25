# PCE — Python Core Engine

![Version](https://img.shields.io/badge/version-0.0.0-orange)
![License](https://img.shields.io/badge/license-GPLv3-blue)
![Status](https://img.shields.io/badge/status-open--source%20%7C%20in%20development-yellow)

> ⚠️ **Note:** PCE is currently at an experimental **0.0.0** version — still under active development, but already usable.

## Overview

**PCE (Python Core Engine)** is an open-source game engine core written entirely in **Python**, built on top of the **Pygame** framework.

PCE provides a general set of system components for building a basic Game Engine, designed for developing games in the following genres:

- 🎭 **Visual Novel**
- ⚔️ **RPG**

## Directory Structure

```
PCE/
├── docs/              # Documentation and API references
├── systems/           # Core engine systems
│   ├── event/         # Event system (Engine + Pygame events)
│   ├── file/          # File abstraction layer (requires subclassing & customization)
│   ├── input/         # Keyboard shortcut / input syntax management
│   ├── object/        # Component & Game Object system
│   └── scene/         # Scene creation and management
└── utils/             # Additional utility library
```

## Usage Example

```python
from systems import Scene, ManagerScene, KeyShort, Event

class TestScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.key_short = KeyShort(
            "key-short-test",
            lambda: print("If you pressed, you gay :)))))"),
            Event.K_i,
            Event.K_m,
            Event.K_g
        )

    def update(self, dt):
        self.key_short.active()

manager = ManagerScene()
manager.push_scene(TestScene(manager))
manager.run()
```

## Installation

> The project is currently **open-source** and under active development.

```bash
git clone https://github.com/MeoMuop3727/pce.git
cd pce
pip install -r requirements.txt
```

## License

This project is released under the **[GNU General Public License v3.0 (GPLv3)](https://github.com/MeoMuop3727/pce/blob/main/LICENSE)**.

## Documentation

📖 [PCE Documentation](#)

<!-- TODO: update with the real documentation link once available -->

---

<p align="center">Made with ❤️ using Python & Pygame</p>