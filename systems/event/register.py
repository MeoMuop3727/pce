import pygame

# Internal engine API — not intended for direct use by end users of
# the engine, and this class is not designed to be subclassed.

_ENGINE_EVENTS: tuple[str] = (
    "HOVER",
)

class EventRegistry:

    """
    Internal registry mapping custom engine event names to pygame event type IDs.

    This class is used internally by the engine to allocate and track
    custom pygame event types (via `pygame.event.custom_type()`)
    under human-readable string names, avoiding collisions with
    pygame's own built-in event constants. It is not meant to be
    subclassed, and end users of the engine should not interact with
    it directly.

    Attributes:
        (No public attributes; registered events are accessed via
        `get_event`, `get_engine_events`, and `get_pygame_events`.)
    """

    def __init__(self):
        self.__list_events: dict[str, int] = {}
        self.register(*tuple(_ENGINE_EVENTS))
        
    def register(self, *events: str):

        """
        Registers one or more custom event names.

        Allocates a new pygame custom event type for each given name.

        Args:
            *events (str): One or more event names to register.

        Raises:
            KeyError: If an event name conflicts with an existing
                attribute on the `pygame` module, or is already
                registered.
        """

        for event in events:
            if hasattr(pygame, event):
                raise KeyError(f"Event {event!r} conflicts with pygame events")
            
            if event in self.__list_events:
                raise KeyError(f"Event {event!r} existed")
            
            self.__list_events[event] = pygame.event.custom_type()

    def unregister(self, *events: str):

        """
        Removes one or more registered event names.

        Note that this only removes the name-to-id mapping; pygame
        does not support releasing an allocated custom event type.

        Args:
            *events (str): One or more event names to remove.

        Raises:
            KeyError: If an event name is not currently registered.
        """

        for event in events:
            if event not in self.__list_events:
                raise KeyError(f"Event {event!r} is not existed")
            self.__list_events.pop(event)

    def get_pygame_events(self) -> list[pygame.event.Event]:

        """
        Retrieves all pending pygame events from the event queue.

        Returns:
            list[pygame.Event]: The events currently in the queue,
                as returned by `pygame.event.get()`.
        """

        return pygame.event.get()

    def get_engine_events(self) -> dict[str, int]:

        """
        Retrieves a copy of all registered engine event names and their IDs.

        Returns:
            dict[str, int]: A mapping of event name to pygame custom
                event type ID.
        """

        return self.__list_events.copy()

    def get_event(self, event: str) -> int:

        """
        Retrieves the pygame event type ID for a registered event name.

        Args:
            event (str): The name of the registered event.

        Returns:
            int: The corresponding pygame custom event type ID.

        Raises:
            KeyError: If `event` is not currently registered.
        """

        if event not in self.__list_events:
            raise KeyError(f"Event {event!r} is not existed")
        return self.__list_events[event]

