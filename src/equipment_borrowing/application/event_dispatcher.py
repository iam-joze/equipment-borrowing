from abc import ABC, abstractmethod


class EventDispatcher(ABC):
    """How the application publishes domain events. The delivery mechanism
    (in-process today, a message broker tomorrow) is an infrastructure detail."""

    @abstractmethod
    def publish(self, event: object) -> None: ...