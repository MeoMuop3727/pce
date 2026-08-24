import pygame
from typing import Optional

# Engine import
from utils.tools import apply_instance
from .transform import Transform

class Sprite:

    """
    Represents a 2D renderable object wrapping a pygame texture.

    A Sprite holds a texture along with the transform (position,
    scale, rotation), render layer, flip state, visibility, and
    alpha transparency needed to draw it onto a pygame screen. Each
    frame, `update` applies the current transform and visual state
    to the texture and blits the result onto the given surface.

    Attributes:
        transform (Transform): The position, scale, and rotation
            applied to the sprite.
        layer (int): The render layer/order of the sprite, used to
            determine draw order relative to other sprites.
        flipx (bool): Whether the texture is flipped horizontally.
        flipy (bool): Whether the texture is flipped vertically.
        visible (bool): Whether the sprite should be rendered.
        alpha (int): The transparency level of the sprite, from 0
            (fully transparent) to 255 (fully opaque).
    """

    def __init__(self,
                 texture: pygame.Surface,
                 transform: Optional[Transform] = None,
                 layer: int = 1,
                 flip: tuple[bool, bool] = (False, False),
                 visible: bool = True,
                 alpha: int = 255):
        self._texture_orginal = texture                 # The original texture
        self._texture = self._texture_orginal.copy()    # The copy texture, use to apply modifies

        self.transform = apply_instance(Transform(), transform)
        self.layer = layer
        self.flipx, self.flipy = flip
        self.visible = visible
        self.alpha = max(0, min(alpha, 255))

    # Properties
    @property
    def texture(self) -> pygame.Surface:
        return self._texture

    @texture.setter
    def texture(self, new_texture: pygame.Surface):
        self._texture_orginal = new_texture
        self._texture = self._texture_orginal.copy()

    def set_texture(self) -> pygame.Surface:

        """
        Applies the sprite's current transform and visual state to a texture.

        Processes the given surface by applying, in order: alpha
        transparency, scaling, flipping, and rotation, based on the
        sprite's current attributes.

        Returns:
            pygame.Surface: The resulting surface after all
                transformations have been applied.
        """

        # Alpha
        self._texture.set_alpha(self.alpha)

        # Resize 
        scalex, scaley = self.transform.scale
        w = int(self._texture.get_width() * scalex)
        h = int(self._texture.get_height() * scaley)
        self._texture = pygame.transform.scale(self._texture, (w, h))

        # Flip 
        self._texture = pygame.transform.flip(self._texture, self.flipx, self.flipy)

        # Rotate 
        self._texture = pygame.transform.rotate(self._texture, self.transform.rotation)
        self._rotated_pos = self._texture.get_offset()

        return self._texture

    def _get_surface_rendered(self) -> Optional[pygame.Surface]:

        """
        Builds the final surface to be rendered this frame.

        Returns:
            Optional[pygame.Surface]: The transformed surface ready
                for blitting, or None if the sprite is not visible.
        """

        if not self.visible: return None
        return self.set_texture() 

    def update(self, screen: pygame.Surface):

        """
        Renders the sprite onto the given screen surface.

        Computes the transformed surface (if visible), positions it
        based on the sprite's transform position (used as the center),
        and blits it onto the target screen.

        Args:
            screen (pygame.Surface): The surface to draw the sprite onto.
        """

        surf = self._get_surface_rendered()

        if surf is None: return

        rect = surf.get_rect(center=self.transform.position)
        screen.blit(surf, rect)