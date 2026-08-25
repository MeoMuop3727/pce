from typing import Optional

# Engine import
from .audio import _Audio
from ...input import KeyShort

class TreeAudio:

    """
    Manages a collection of named audio objects and switches between them.

    Acts as a state machine over multiple `_Audio` instances (e.g.
    `AudioSFX`, `AudioMusic`), keeping track of which one is
    currently active and playing it on demand. Useful for objects
    with multiple audio states, such as background music tracks or
    context-dependent sound effects.

    Attributes:
        current_name_audio (str): The tag of the audio currently
            active and played by `play`.
    """

    def __init__(self,
                 init_name: str,
                 /,
                 *audios: _Audio):
        self.current_name_audio = init_name
        self._list_audios: dict[str, _Audio] = {}
        self.register(*audios)

    def register(self, *audios: _Audio):

        """
        Adds one or more audio objects to the collection.

        Args:
            *audios (_Audio): One or more audio instances to
                register, keyed internally by their `tag`.
        """

        for index, audio in enumerate(audios):
            if not isinstance(audio, _Audio):
                raise ValueError(f"The audio at {index!r} is not an _Audio/AudioSFX/AudioMusic")

            if audio.tag in self._list_audios:
                raise KeyError(f"The {audio.tag!r} existed")

            self._list_audios[audio.tag] = audio

    def unregister(self, *audios: _Audio):

        """
        Removes one or more audio objects from the collection.

        Args:
            *audios (_Audio): One or more audio instances to remove,
                matched by their `tag`.
        """

        for index, audio in enumerate(audios):
            if not isinstance(audio, _Audio):
                raise ValueError(f"The audio at {index!r} is not an _Audio/AudioSFX/AudioMusic")

            if audio.tag not in self._list_audios:
                raise KeyError(f"The {audio.tag!r} is not existed")

            self._list_audios.pop(audio.tag)

    def switch(self, name_audio: str, event: Optional[KeyShort] = None, ms: float = 1.):

        """
        Switches the currently active audio.

        Fades out the currently active audio first, then switches to
        the new one. If no event is given, switches immediately. If
        an event is given, the switch only happens when the event is
        triggered (`event.is_call()` returns True).

        Args:
            name_audio (str): The tag of the audio to switch to.
            event (Optional[KeyShort]): An optional input event that
                gates when the switch occurs. Defaults to None
                (switch immediately).
            ms (float): The fadeout duration, in milliseconds, applied
                to the currently active audio before switching.
                Defaults to 1.0.
        """

        if name_audio not in self._list_audios:
            raise KeyError(f"The {name_audio!r} is not existed")

        self._list_audios[self.current_name_audio].fadeout(ms)

        if event is None:
            self.current_name_audio = name_audio
        else:
            if event.is_call():
                self.current_name_audio = name_audio 

    def play(self):
        if not self._list_audios: return
        self._list_audios[self.current_name_audio].play()

    def pause(self):
        if not self._list_audios: return
        self._list_audios[self.current_name_audio].pause()

    def unpause(self):
        if not self._list_audios: return
        self._list_audios[self.current_name_audio].unpause()

    def stop(self):
        if not self._list_audios: return
        self._list_audios[self.current_name_audio].stop()

    def set_volume(self, new_volume: float):
        if not self._list_audios: return
        self._list_audios[self.current_name_audio].set_volume(new_volume)
    
