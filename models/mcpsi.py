from typing import Dict
from math import factorial

from models.base_queue import BaseQueueModel

class mcpsi(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int, lamb_list: list[float]
    ) -> None:
        super().__init__(lamb, mu, k, s)

        self.k = k
        self.lamb_list = lamb_list
        self.r = lamb / mu

        if any(l < 0 for l in self.lamb_list) or self.lamb < 0 or self.mu <= 0 or self.s < 1:
            raise ValueError(
                "Parâmetros inválidos: requer λi ≥ 0, λ ≥ 0, μ > 0 e s ≥ 1."
            )
        
    def calculate_metrics(self) -> Dict[str, float]:
        w = self.__calculate_avg_time_system()
        wq = self.__calculate_avg_time_queue(w)
        l = self.__calculate_avg_customers_system(w)
        lq = self.__calculate_avg_customers_queue(l)

        return {
            "W": round(w, 4),
            "Wq": round(wq, 4),
            "L": round(l, 4),
            "Lq": round(lq, 4)
        }
    
    def __calculate_avg_time_system(self) -> float:
        if self.r == 0:
            return 1 / self.mu
        
        first_term = (
            (
                factorial(self.s) * (
                    ((self.s * self.mu) - self.lamb) / (self.r ** self.s)
                ) * (
                    sum(self.r ** j / factorial(j) for j in range(self.s))
                )
            ) + (self.s * self.mu)
        )

        second_term = (1 - (sum(self.lamb_list[:self.k-1]) / (self.s * self.mu)))
        third_term = (1 - (sum(self.lamb_list[:self.k]) / (self.s * self.mu)))

        w = (1 / (first_term * second_term * third_term)) + (1 / self.mu)
        return w

    def __calculate_avg_time_queue(self, w: float) -> float:
        wq = w - (1 / self.mu)
        return wq
    
    def __calculate_avg_customers_system(self, w: float) -> float:
        l = self.lamb * w
        return l
    
    def __calculate_avg_customers_queue(self, l: float) -> float:
        lq = l - (self.lamb / self.mu)
        return lq