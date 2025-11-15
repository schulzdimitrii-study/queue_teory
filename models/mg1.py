from math import factorial
from typing import Dict

from models.base_queue import BaseQueueModel

class MG1(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int
    ) -> None:
        super().__init__(lamb, mu, k, s)
        self.rho = lamb / mu
        self.var = (1 / self.mu)**2

        if self.s != 1 or self.mu <= 0 or self.lamb < 0:
            raise ValueError(
                "Parâmetros inválidos: requer λ ≥ 0, μ > 0, s = 1."
            )
        
    def calculate_metrics(self) -> Dict[str, float]:
        p0 = self.__calculate_probability_system_empty()
        lq = self.__calculate_avg_customers_queue()
        l = self.__calculate_avg_customers_system(lq)
        wq = self.__calculate_avg_time_queue(lq)
        w = self.__calculate_avg_time_system(wq)

        return {
            "P0": round(p0, 4),
            "Lq": round(lq, 4),
            "L": round(l, 4),
            "Wq": round(wq, 4),
            "W": round(w, 4)
        }
    
    def __calculate_probability_system_empty(self) -> float:
        return 1 - self.rho
    
    def __calculate_avg_customers_queue(self) -> float:
        return (self.rho**2 * (1 + self.var * self.mu**2)) / (2 * (1 - self.rho))
    
    def __calculate_avg_customers_system(self, lq: float) -> float:
        return lq + self.rho
    
    def __calculate_avg_time_queue(self, lq: float) -> float:
        return lq / self.lamb
    
    def __calculate_avg_time_system(self, wq: float) -> float:
        return wq + (1 / self.mu)