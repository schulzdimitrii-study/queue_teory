from abc import ABC, abstractmethod
from typing import Dict


class BaseQueueModel(ABC):
    def __init__(self, arrival_rate: float, service_rate: float, capacity: int) -> None:
        self.lamb = arrival_rate
        self.mu = service_rate
        self.k = capacity

    @abstractmethod
    def calculate_metrics(self) -> Dict:
        pass
