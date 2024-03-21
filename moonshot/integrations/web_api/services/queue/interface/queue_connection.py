from typing import Callable, Self
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")
class InterfaceQueueConnection(Generic[T], ABC):

    @abstractmethod
    def connect(self, queue_name: str | None = None) -> Self:
        pass
    
    @abstractmethod
    def subscribe(self, worker: Callable[[T], None]) -> None:
        pass

    @abstractmethod
    def unsubscribe(self) -> None:
        pass
    
    @abstractmethod
    def publish(self, task: T) -> bool | None:
        pass
    
    @abstractmethod
    def close(self):
        pass



