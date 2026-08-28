import pygame
from pathlib import Path
from typing import Optional

# Engine import
from .transform import Transform
from .sprite import Sprite
from ....utils.tools import apply_instance
class _Animation: 

    """
    Base class for frame-based sprite animations.

    Intended to be subclassed rather than used directly. Holds a
    sequence of texture frames along with transform, visual state,
    and timing settings, and steps through the frames over time to
    produce a simple animation.

    Attributes:
        transform (Transform): The position, scale, and rotation
            applied to every frame of the animation.
        flipx (bool): Whether frames are flipped horizontally.
        flipy (bool): Whether frames are flipped vertically.
        visible (bool): Whether the animation should be rendered.
        layer (int): The render layer/order of the animation, used
            to determine draw order relative to other objects.
        alpha (int): The transparency level of the animation, from 0
            (fully transparent) to 255 (fully opaque).
        loop (bool): Whether the animation restarts from the first
            frame after reaching the last one.
        duration (float): The time (in seconds) each frame is held
            before advancing to the next.
        dt (float): The time increment added each update call,
            simulating elapsed time per frame/tick.
        playing (bool): Whether the animation is currently advancing.
    """

    def __init__(self,
                 tag: str,
                 transform: Optional[Transform] = None,
                 flip: tuple[bool, bool] = (False, False),
                 visible: bool = True,
                 layer: int = 1,
                 alpha: int = 255,
                 loop: bool = True,
                 duration: float = 1.,
                 dt: float = 0.1,
                 playing: bool = True):
        self._tag = tag
        self.transform = apply_instance(Transform(), transform)
        self.flipx, self.flipy = flip
        self.visible = visible
        self.layer = layer
        self.alpha = alpha
        self.loop = loop
        self.duration = duration
        self.dt = dt
        self.playing = playing

        self._elapsed_index: int = 0
        self._elapsed_time: float = 0.

        self._list_frames_original: list[pygame.Surface] = []   # The original list frames
        self._list_frames: list[pygame.Surface] = []            # The copy list frames which uses to apply modifies

    @property
    def tag(self) -> str:
        return self._tag

    def _set_texture(self, texture: pygame.Surface) -> pygame.Surface:

        """
        Applies the animation's transform and visual state to a single frame.

        Delegates to a temporary Sprite to process the given texture
        (scale, flip, rotation, alpha) using the animation's current
        settings.

        Args:
            texture (pygame.Surface): The source frame to process.

        Returns:
            pygame.Surface: The resulting processed frame.
        """

        return Sprite(
            texture=texture,
            transform=self.transform,
            flip=(self.flipx, self.flipy),
            alpha=self.alpha
        ).set_texture()

    def _apply_set_texture(self):

        """
        Processes all original frames and rebuilds the render-ready frame list.

        Applies `_set_texture` to every frame in `_list_frames_original`
        and appends the results to `_list_frames`, which is what
        `update` actually draws from.
        """

        for frame in self._list_frames_original.copy():
            frame = self._set_texture(frame)
            self._list_frames.append(frame)

    def _play(self, speed: float):

        """
        Advances the animation's playback state.

        Increments the elapsed time by `dt * speed`, and once it
        reaches `duration`, moves to the next frame. When the last
        frame is passed, either loops back to the start (if `loop`
        is True) or stops on the final frame (if `loop` is False).

        Args:
            speed (float): A multiplier applied to `dt` to speed up
                or slow down playback.
        """

        if not self._list_frames: return
        if not self.playing: return

        self._elapsed_time += self.dt * speed

        if self._elapsed_time >= self.duration:
            self._elapsed_index += 1
            self._elapsed_time = 0.

            if self._elapsed_index >= len(self._list_frames):
                if self.loop:
                    self._elapsed_index %= len(self._list_frames)
                    self.playing = True
                else:
                    self._elapsed_index = len(self._list_frames) - 1
                    self.playing = False

    def update(self, surface: pygame.Surface, speed: float = 1.):

        """
        Advances and renders the current animation frame.

        Updates the playback state, then blits the current frame
        onto the given surface at the transform's position.

        Args:
            surface (pygame.Surface): The surface to draw the
                current frame onto.
            speed (float): A multiplier applied to playback speed.
                Defaults to 1.0 (normal speed).
        """

        self._play(speed)
        surface.blit(
            self._list_frames[self._elapsed_index],
            self.transform.position
        )

class AnimationSheet(_Animation):

    """
    Animation built by slicing frames from a single sprite sheet image.

    Loads an image from disk and cuts it horizontally into equal-sized
    frames, which are then used as the animation's frame sequence.

    Attributes:
        (Inherits all attributes from `_Animation`, e.g. transform, flipx, flipy, visible, layer, alpha, loop, duration, dt, playing.)
    Note:
        The `AnimationSheet` only cuts the sheet with one animation, meaning the frames of the animation in one line.
    """

    def __init__(self, 
                 tag: str, 
                 path_sheet: str,
                 size_frame: tuple[int, int] = (32, 32),
                 count: int = 0,
                 transform = None, 
                 flip = (False, False), 
                 visible = True, 
                 layer = 1, 
                 alpha = 255,
                 loop = True,
                 duration = 0.1, 
                 dt = 0.1,
                 playing = True):

        """
        Initializes the animation and immediately slices the sheet into frames.

        Args:
            tag (str): Identifier for this animation.
            path_sheet (str): File path to the sprite sheet image.
            size_frame (tuple[int, int]): The (width, height) of each
                individual frame on the sheet. Defaults to (32, 32).
            count (int): The number of frames to slice from the sheet,
                read left to right starting at the top row. Defaults
                to 0 (no frames).
            transform, flip, visible, layer, alpha, loop, duration,
                dt, playing: See `_Animation.__init__`.
        """

        super().__init__(tag, 
                         transform, 
                         flip, 
                         visible, 
                         layer, 
                         alpha, 
                         loop, 
                         duration, 
                         dt, 
                         playing)
        self._path_sheet = path_sheet
        self._sheet_to_frames(size_frame, count)

    def _sheet_to_frames(self, size_frame: tuple[int, int], count: int = 0):

        """
        Loads the sheet image and slices it into individual frames.

        Reads the image at `self._path_sheet`, cuts out `count` frames
        of size `size_frame` in a single row (left to right), stores
        them as the original frame list, then applies the current
        transform/visual state to build the render-ready frames.

        Args:
            size_frame (tuple[int, int]): The (width, height) of each
                frame to cut from the sheet.
            count (int): The number of frames to cut. Defaults to 0.
        """

        if not Path(self._path_sheet).exists():
            raise FileNotFoundError(f"Cannot find the sheet at: {self._path_sheet!r}")

        w, h = size_frame
        sheet = pygame.image.load(self._path_sheet).convert_alpha()

        for i in range(count):
            surf = pygame.Rect(i * w, 0, w, h)
            frame = sheet.subsurface(surf)
            self._list_frames_original.append(frame)

        self._apply_set_texture()

class AnimationTexture(_Animation):

    """
    Animation built from individually supplied texture frames.

    Unlike `AnimationSheet`, frames are not sliced from a single
    image but added one by one (or in bulk) via `add_texture`.

    Attributes:
        (Inherits all attributes from `_Animation`, e.g. transform,
        flipx, flipy, visible, layer, alpha, loop, duration, dt,
        playing.)
    """

    def __init__(self, 
                 tag: str, 
                 transform = None, 
                 flip = (False, False), 
                 visible = True, 
                 layer = 1, 
                 alpha = 255, 
                 loop = True, 
                 duration = 0.1, 
                 dt = 0.1, 
                 playing = True):

        """
        Initializes the animation with an empty frame list.

        Frames must be added afterwards via `add_texture`.

        Args:
            tag (str): Identifier for this animation.
            transform, flip, visible, layer, alpha, loop, duration,
                dt, playing: See `_Animation.__init__`.
        """

        super().__init__(tag, 
                         transform, 
                         flip, 
                         visible, 
                         layer, 
                         alpha, 
                         loop, 
                         duration, 
                         dt, 
                         playing)

    def add_texture(self, *textures: pygame.Surface):

        """
        Adds one or more frames to the animation.

        Appends each given surface to the original frame list, then
        reapplies the current transform/visual state to rebuild the
        render-ready frame list.

        Args:
            *textures (pygame.Surface): One or more surfaces to add
                as animation frames, in order.
        """

        for index, texture in enumerate(textures):
            if not isinstance(texture, pygame.Surface):
                raise ValueError(f"The texture at {index!r} is not Surface")
            self._list_frames_original.append(texture) 
        self._apply_set_texture()

