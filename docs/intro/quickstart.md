# Quickstart — Getting Started with PCE

This guide walks you through installing PCE and setting up your first starter project with a basic Scene.

> ℹ️ **Note:** PCE is currently only a **core engine (core)** and does not yet wrap the full Pygame API. You'll still need to install and use **Pygame** alongside PCE in your project.

## Requirements

| Component | Version |
| --- | --- |
| Python | `3.12.3` |
| Pygame | `2.6.1` |

## 1. Installation

Clone the repository:

```bash
git clone https://github.com/MeoMuop3727/pce.git
cd pce
```

Install Pygame (if not already installed):

```bash
pip install pygame==2.6.1
```

## 2. Create a Starter Project

Create a file, e.g. `main.py`, in the root of your project (placed at the same level as the `systems/` folder):

```python
from systems import Scene, ManagerScene, KeyShort, Event

class MyFirstScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.key_short = KeyShort(
            "start-key",
            lambda: print("Scene is running!"),
            Event.K_s
        )

    def update(self, dt):
        self.key_short.active()
    
    def render(self):
        # TODO: add your render / update logic here

manager = ManagerScene()
manager.push_scene(MyFirstScene(manager))
manager.run()
```

## 3. Run It

```bash
python main.py
```

or

```bash
python3 main.py
```

If a Pygame window opens without errors, you've successfully installed PCE and initialized your first Scene! 🎉

## Next Steps

- Explore `systems/scene` to manage multiple Scenes at once.
- Explore `systems/event` and `systems/input` to handle events and key shortcuts.
- Explore `systems/object` to create Components and Game Objects for your Scene.

<!-- TODO: add a link to the example/ directory once available -->

---

<p align="center">Made with ❤️ using Python & Pygame</p>