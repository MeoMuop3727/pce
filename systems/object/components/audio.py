import pygame
from pathlib import Path
from typing import Optional

class _Audio:
    def __init__(self,
                 tag: str,
                 path: str,
                 volume: float = 1.,
                 loop: bool = False):
        self._tag = tag
        self.path = path
        self.volume = volume
        self.loop = loop

    @property
    def tag(self) -> str:
        return self._tag

    def play(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def unpause(self):
        pass

    def set_volume(self, new_volume: float):
        pass

    def fadeout(self, ms: int):
        pass

class AudioSFX(_Audio):

    """
    A short, one-shot sound effect.

    Loads the audio file as a `pygame.mixer.Sound` and plays it
    through a dedicated channel, making it suitable for sound
    effects that may overlap with music or other sound effects
    (e.g. clicks, hits, footsteps).
    """

    def __init__(self, tag, path, volume = 1, loop = False):
        super().__init__(tag, path, volume, loop)

        if not Path(self.path).exists():
            raise FileNotFoundError(f"Cannot find the sfx file at: {self.path!r}")
        
        self._sound = pygame.mixer.Sound(self.path)
        self._sound.set_volume(self.volume)
        self._channel: Optional[pygame.mixer.Sound] = None

    def play(self):

        """
        Plays the sound effect on a free channel.

        Loops indefinitely if `self.loop` is True, otherwise plays
        once. Stores the channel used so it can be paused, resumed,
        or stopped later.
        """

        self._channel = self._sound.play(loops=-1 if self.loop else 0)

    def stop(self):

        """ Stops the sound effect if it is currently playing. """

        if self._channel is None:
            raise ValueError(f"The AudioSFX._channel is 'None' value")
        self._channel.stop()

    def set_volume(self, new_volume: float, /):

        """
        Sets the sound effect's volume.

        Args:
            new_volume (float): The new volume level, from 0.0
                (silent) to 1.0 (full volume).
        """

        self.volume = max(0., min(new_volume, 1.))
        self._sound.set_volume(self.volume)

    def fadeout(self, ms: int, /):

        """
        Gradually fades out and stops the sound effect.

        Args:
            ms (int): The duration of the fade-out, in milliseconds.
        """

        self._sound.fadeout(ms)

class AudioMusic(_Audio):

    """
    A streamed music track.

    Uses `pygame.mixer.music` to stream the audio file rather than
    loading it fully into memory, making it suitable for longer
    background music tracks. Since `pygame.mixer.music` only
    supports one active stream at a time, playing a new `AudioMusic`
    instance will replace any currently playing music.
    """

    def __init__(self, tag, path, volume = 1, loop = False):
        super().__init__(tag, path, volume, loop)

    def play(self):

        """
        Loads and starts playback of the music track.

        Loops indefinitely if `self.loop` is True, otherwise plays
        once.
        """

        if not Path(self.path).exists():
            raise FileNotFoundError(f"Cannot find the music file at: {self.path!r}")

        pygame.mixer.music.load(self.path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loops=-1 if self.loop else 0)

    def stop(self):

        """ Stops the currently playing music. """

        pygame.mixer.music.stop()

    def pause(self):

        """ Pauses the currently playing music. """

        pygame.mixer.music.pause()

    def unpause(self):

        """ Resumes the currently paused music. """

        pygame.mixer.music.unpause()

    def set_volume(self, new_volume: float, /):

        """
        Sets the music's volume.

        Args:
            new_volume (float): The new volume level, from 0.0
                (silent) to 1.0 (full volume).
        """

        self.volume = max(0., min(new_volume, 1.))
        pygame.mixer.music.set_volume(self.volume)

    def fadeout(self, ms: int, /):
        """
        Gradually fades out and stops the music.

        Args:
            ms (int): The duration of the fade-out, in milliseconds.
        """
        pygame.mixer.music.fadeout(ms)

