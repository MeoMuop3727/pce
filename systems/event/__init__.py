"""
Public entry point for the engine's event system.

Before anything else is imported, this module runs
`stub_event_generate()` to generate the `Event` class, which
combines every built-in pygame event constant together with the
engine's own custom events (registered via `EventRegistry`). This
lets code reference both pygame events (e.g. `Event.QUIT`,
`Event.KEYDOWN`) and engine-specific events (e.g. `Event.HOVER`)
through a single unified `Event` interface, instead of having to
mix `pygame.EVENTNAME` constants with separately tracked custom
event IDs.

Exports:
    Event: The combined pygame + engine event type, generated at
        import time by `stub_event_generate`.
"""

from ._stub_generate import stub_event_generate
stub_event_generate()

from .events import Event

__all__ = ["Event"]