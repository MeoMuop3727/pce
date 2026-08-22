from typing import Optional, Callable
from dataclasses import dataclass

# Engine import
from ..identify import Identify

@dataclass(slots=True)
class Connection:

    """
    Represents a link between two objects, describing which event
    on the target triggers a given action.

    Attributes:
        target (Identify): A reference to the object this connection 
            is bound to (e.g. the object being observed or interacted
            with). Defaults to None (no target bound yet).
        event (Optional[int]): The type of event that triggers this
            connection, such as click, hover, etc. Defaults to None
            (no event bound yet).
        action (Optional[Callable[[], None]]): The callback to invoke when the
            event occurs, defining the resulting behavior (e.g. hide
            or show a label). Defaults to None (no action bound yet).
    """

    target: Optional[Identify] = None
    event: Optional[int] = None
    action: Optional[Callable[[], None]] = None