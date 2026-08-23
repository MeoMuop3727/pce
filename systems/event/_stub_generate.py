import pygame
from pathlib import Path

# Engine import
from .register import _ENGINE_EVENTS

def get_pygame_events() -> dict[str, int]:
    
    """ Choose, filter and return a mapping pygame events """

    events: dict[str, int] = {}

    for name in dir(pygame):
        value = getattr(pygame, name)

        if not isinstance(value, int): continue

        try: 
            event_name = pygame.event.event_name(value)
        except Exception:
            continue

        if event_name:
            events[name] = value

    return events

def stub_event_generate():
    pygame_events = get_pygame_events()
    engine_events = _ENGINE_EVENTS
    engine_funcs = [
        "register(cls, *events: str): ...",
        "unregister(cls, *events: str): ...",
        "get_engine_events(cls): ...",
        "get_pygame_events(cls): ..."
    ]

    lines: list[str] = [
        "class Event:",
        "",
        "\t# Pygame event (Default events)",
    ]

    # Adding pygame events
    for event in pygame_events:
        lines.append(f"\t{event}: int")

    lines.append("")
    lines.append("\t# Engine events (Custom events)")

    # Adding engine events
    for event in engine_events:
        lines.append(f"\t{event}: int")

    lines.append("")

    # Adding engine funcs
    for func in engine_funcs:
        lines.append(f"\tdef {func}")

    stub_path = Path(__file__).with_name("events.pyi")
    stub_path.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )
