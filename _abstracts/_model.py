
from abc import ABC, abstractmethod

class _Model(ABC):

    @abstractmethod
    def execute(self):
        pass