from math import comb, factorial
from typing import Dict, Optional

from models.base_queue import BaseQueueModel


class MM1N(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int, n: int, N: int
    ) -> None:
        super().__init__(lamb, mu, k, s)
        self.n = n
        self.N = N
        self.a = lamb / mu
        self.rho = (self.N * self.a)

        if self.s != 1 or self.n <= 0 or self.N <= 0 or self.mu <= 0 or self.lamb < 0:
            raise ValueError(
                "Parâmetros inválidos: requer λ ≥ 0, μ > 0, s = 1, n ≥ 1 e N ≥ 1."
            )
        
    def calculate_metrics(self) -> Dict[str, float]:
        p0 = self.__calculate_probability_system_empty()
        pn = self.__calculate_probability_n_customers_system(p0, self.n)
        lq = self.__calculate_avg_customers_queue(p0)
        l = self.__calculate_avg_customers_system(p0)
        wq = self.__calculate_avg_time_queue(lq, l)
        w = self.__calculate_avg_time_system(l)

        return {
            "P0": round(p0, 4),
            "Pn": round(pn, 4),
            "Lq": round(lq, 4),
            "L": round(l, 4),
            "Wq": round(wq, 4),
            "W": round(w, 4)
        }
    
    def __calculate_probability_system_empty(self) -> float:
        sum_part = sum((factorial(self.N) / factorial(self.N - n)) * (self.a**n) for n in range(self.N + 1))
        return 1 / sum_part
    
    def __calculate_probability_n_customers_system(self, p0: float, n: int) -> float:
        return (factorial(self.N) / factorial(self.N - n)) * (self.a**n) * p0
    
    def __calculate_avg_customers_queue(self, p0: float) -> float:
        return self.N - ((self.lamb + self.mu) / (self.lamb)) * (1 - p0)
    
    def __calculate_avg_customers_system(self, p0: float) -> float:
        return self.N - (self.mu / self.lamb) * (1 - p0)
    
    def __calculate_avg_time_queue(self, lq: float, l: float) -> float:
        return lq / (self.lamb * (self.N - l))
    
    def __calculate_avg_time_system(self, l: float) -> float:
        return l / (self.lamb * (self.N - l))