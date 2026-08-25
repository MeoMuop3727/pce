import pygame
from typing import Optional

# Engine import
from .connection import Connection
from ..identify import Identify

class ConnectionGroup:

    """
    Manages a collection of Connections keyed by their target object.

    Stores `Connection` instances (target + event + action) using the
    target object's `id` as the key, allowing lookups and triggering
    of an object's bound action by reference to the target itself.

    Attributes:
        (No public attributes; connections are managed internally
        and accessed via `get`/`active_action`.)
    """

    def __init__(self, *connections: Connection):
        # Use id of object which connected as a key
        self._list_connections: dict[str, Connection] = {}
        self.register(*connections)

    def register(self, *connections: Connection):

        """
        Adds one or more connections to the collection.

        Each connection is keyed internally by its target object's
        `id`.

        Args:
            *connections (Connection): One or more connections to
                register.
        """

        for index, connection in enumerate(connections):
            if not isinstance(connection, Connection):
                raise ValueError(f"The connection at {index!r} is not a Connection")

            id_obj = connection.target.id
            name_obj = connection.target.name

            if id_obj in self._list_connections:
                raise KeyError(f"The id of object {name_obj!r} existed")

            self._list_connections[id_obj] = connection

    def unregister(self, *connections: Connection):

        """
        Removes one or more connections from the collection.

        Args:
            *connections (Connection): One or more connections to
                remove, matched by their target object's `id`.
        """
        for index, connection in enumerate(connections):
            if not isinstance(connection, Connection):
                raise ValueError(f"The connection at {index!r} is not a Connection")

            id_obj = connection.target.id
            name_obj = connection.target.name

            if id_obj not in self._list_connections:
                raise KeyError(f"The id of object {name_obj!r} is not existed")

            self._list_connections.pop(id_obj)

    def get(self, target: Identify) -> Connection:

        """
        Retrieves the connection registered for a given target object.

        Args:
            target (Identify): The object whose connection to look up.

        Returns:
            Connection: The connection registered for `target`.
        """

        if target.id not in self._list_connections:
            raise KeyError(f"The id of object {target.name!r} is not existed")
        return self._list_connections[target.id]

    def active_action(self, target: Identify):

        """
        Triggers the action bound to a given target object's connection.

        Args:
            target (Identify): The object whose connection's action
                should be invoked.
        """
        
        if target.id not in self._list_connections:
            raise KeyError(f"The id of object {target.name!r} is not existed")
        self._list_connections[target.id].action()
