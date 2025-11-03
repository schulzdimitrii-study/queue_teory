from abc import ABC, abstractmethod
from typing import Dict


class QueueInterface(ABC):
    def __init__(self, lamb: float, mu: float, rho: float) -> None:
        self.lamb = lamb
        self.mu = mu
        self.rho = rho
    
    @abstractmethod
    def calculate_metrics(self) -> Dict[str, float]:
        pass
    
    @abstractmethod
    def print_metrics(self):
        pass