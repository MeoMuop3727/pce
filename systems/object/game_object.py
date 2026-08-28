import pygame
from typing import Optional

# Engine import
from .components import (
    TreeAudio,
    TreeAnimation,
    ColliderGroup,
    ConnectionGroup
)
from .identify import Identify
from ...utils.tools import apply_instance, generate_id
class GameObject:
    def __init__(self,
                 surface: Optional[pygame.Surface] = None,
                 audios: Optional[TreeAudio] = None,
                 animations: Optional[TreeAnimation] = None,
                 colliders: Optional[ColliderGroup] = None,
                 connections: Optional[ConnectionGroup] = None):
        self._surface = surface
        self._audios = apply_instance(TreeAudio, audios)
        self._animations = apply_instance(TreeAnimation, animations)
        self._colliders = apply_instance(ColliderGroup, colliders)
        self._connections = apply_instance(ConnectionGroup, connections)

        self._id = Identify(generate_id(16), "")

    def get_id(self) -> str:
        return self._id.id
    
