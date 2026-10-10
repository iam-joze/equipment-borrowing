from collections.abc import Callable
from typing import Any

from equipment_borrowing.application.event_dispatcher import EventDispatcher


class InProcessEventDispatcher(EventDispatcher):
    """Delivers events to subscribed handlers, in the same process, immediately."""

    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: object) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)
            