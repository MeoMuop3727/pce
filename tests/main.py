# from systems import Scene, ManagerScene, KeyShort, Event

# class TestScene(Scene):
#     def __init__(self, manager):
#         super().__init__(manager)

#         self.key_short = KeyShort(
#             "key-short-test",
#             lambda: print("If you pressed, you gay :)))))"),
#             Event.K_i,
#             Event.K_m,
#             Event.K_g
#         )

#     def update(self, dt):
#         self.key_short.active()

# manager = ManagerScene()
# manager.push_scene(TestScene(manager))
# manager.run()


"""
Ví dụ tối thiểu: 1 hình vuông di chuyển được bằng phím mũi tên / WASD,
nhấn ESC để thoát.

Minh hoạ cách phối hợp Scene, ManagerScene, Sprite, Transform,
KeyShort và Event lại với nhau.
"""

import pygame
from systems import Scene, ManagerScene, Sprite, Transform, KeyShort, Event


def make_square_texture(color, size=64):
    """Tạo texture hình vuông đơn giản, không cần file ảnh."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    surf.fill(color)
    return surf


class PlayerScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        # --- Player: 1 Sprite gắn với 1 Transform ---
        self.player_transform = Transform(position=(640, 360))
        self.player_sprite = Sprite(
            make_square_texture((66, 135, 245, 255)),
            transform=self.player_transform
        )
        self.speed = 300  # pixel / giây

        # --- Phím tắt: ESC để thoát game ---
        self.key_quit = KeyShort(
            "quit-game",
            lambda: setattr(self._manager, "running", False),
            Event.K_ESCAPE
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
        caption="PCE Example - Move the Square"
    )
    manager.push_scene(PlayerScene(manager))
    manager.run()