"""
Public entry point for the engine's file system.

Provides the base classes for reading, writing, and serializing game
data (e.g. save files, configs, resources). Both `FileSystem` and
`Serializer` are designed to be subclassed rather than used directly
— they define the interface that concrete implementations must
provide.
"""

from .fs import FileSystem
from .serializer import Serializer

__all__ = ["FileSystem", "Serializer"]