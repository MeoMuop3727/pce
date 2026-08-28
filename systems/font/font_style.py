import pygame
from typing import Optional, Literal

# Engine import
from ..object import Transform
from ...utils.tools import apply_instance

class FontStyle:
    def __init__(self,
                 content: str = "",
                 /,
                 font_family: Optional[str] = None,
                 font_size: int = 11,
                 bold: bool = False,
                 underline: bool = False,
                 italic: bool = False,
                 highlight: bool = False,
                 text_color: pygame.color.Color = (0, 0, 0, 255),
                 highlight_color: pygame.color.Color = (253, 241, 0, 255),
                 link: Optional[str] = None):
        self.content = content
        self.font_family = font_family
        self.font_size = font_size
        self.bold = bold
        self.underline = underline
        self.italic = italic
        self.highlight = highlight
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.link = link

        self._font = pygame.font.Font(self.font_family, self.font_size)
        self._font.bold = self.bold
        self._font.underline = self.underline
        self._font.italic = self.italic

    def render(self, 
               surface: pygame.Surface, 
               transform: Optional[Transform] = None,
               anchor: Literal[
                   "topleft", "midtop", "topright",
                   "midleft", "center", "midright",
                   "bottomleft", "midbottom", "bottomright"
               ] = "topleft"):
        trans = apply_instance(Transform, transform)

        if self.highlight:
            text_surface = self._font.render(
                self.content,
                True,
                self.text_color,
                self.highlight_color
            )
        else:
            text_surface = self._font.render(
                self.content,
                True,
                self.text_color
            )

        match anchor:
            case "topleft":
                text_rect = text_surface.get_rect(topleft=trans.position)
            case "midtop":
                text_rect = text_surface.get_rect(midtop=trans.position)
            case "topright":
                text_rect = text_surface.get_rect(topright=trans.position)

            case "midleft":
                text_rect = text_surface.get_rect(midleft=trans.position)
            case "center":
                text_rect = text_surface.get_rect(center=trans.position)
            case "midright":
                text_rect = text_surface.get_rect(midright=trans.position)

            case "bottomleft":
                text_rect = text_surface.get_rect(bottomleft=trans.position)
            case "midbottom":
                text_rect = text_surface.get_rect(midbottom=trans.position)
            case "bottomright":
                text_rect = text_surface.get_rect(bottomright=trans.position)

        surface.blit(text_surface, text_rect)
