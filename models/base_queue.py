from abc import ABC, abstractmethod
from typing import Dict


class BaseQueueModel(ABC):
    def __init__(
        self, arrival_rate: float, service_rate: float, capacity: int, servers: int
    ) -> None:
        if arrival_rate < 0 or service_rate <= 0 or capacity < 0 or servers < 1:
            raise ValueError("Parâmetros inválidos")
        self.lamb = arrival_rate
        self.mu = service_rate
        self.capacity = capacity
        self.s = servers

    @abstractmethod
    def calculate_metrics(self) -> Dict:
        pass
