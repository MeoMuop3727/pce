import pygame
from .register import EventRegistry

class _EventMeTa(type):
    _event_register = EventRegistry()

    def __new__(mcls, name, bases, namespace, /, **kwds):
        return super().__new__(mcls, name, bases, namespace, **kwds)

    def __getattr__(cls, name):
        # Try find the event in engine events
        # If the event exists, return it
        # Else, pass and try find it in pygame events
        try:
            return cls._event_register.get_event(name)
        except KeyError:
            pass

        # Try find the event in pygame events
        try:
            return getattr(pygame, name)
        except AttributeError:
            raise AttributeError(f"{cls.__name__!r} has no event {name!r}")

class Event(metaclass=_EventMeTa):
    @classmethod
    def register(cls, *events: str):
        cls._event_register.register(*events) 

    @classmethod
    def unregister(cls, *events: str):
        cls._event_register.unregister(*events)

    @classmethod
    def get_engine_events(cls):
        return cls._event_register.get_engine_events()

    @classmethod
    def get_pygame_events(cls):
        return cls._event_register.get_pygame_events() 