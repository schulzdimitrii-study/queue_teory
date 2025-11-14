from math import exp, factorial
from typing import Dict

from models.base_queue import BaseQueueModel

class MMsK(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int, n: int
    ) -> None:
        super().__init__(lamb, mu, k, s)
        self.a = lamb / mu
        self.rho = self.lamb / (self.s * self.mu)
        self.k = k
        self.n = n

        if s <= 1:
            raise ValueError("Número de servidores deve ser maior que 1.")
        if n < 0 or k < 0:
            raise ValueError("n e k devem ser valores não negativos.")

    def calculate_metrics(self) -> Dict[str, float]:
        p0 = self.__calculate_probability_system_empty()
        pn = self.__calculate_probability_n_customers_system(p0, self.n)
        pk = self.__calculate_probability_k_customers_system(p0)
        lq = self.__calculate_avg_customers_queue(p0)
        l = self.__calculate_avg_customers_system(p0, lq)
        wq = self.__calculate_avg_time_queue(lq, pk)
        w = self.__calculate_avg_time_system(l, pk)

        return {
            "P0": round(p0, 4),
            "Pn": round(pn, 4),
            "Lq": round(lq, 4),
            "L": round(l, 4),
            "Wq": round(wq, 4),
            "W": round(w, 4)
        }

    def __calculate_probability_system_empty(self) -> float:
        sum_part1 = sum(self.a**n / factorial(n) for n in range(self.s + 1))
        middle_part = (self.a**self.s) / (factorial(self.s))
        sum_part2 = sum(self.rho**(n - self.s) for n in range(self.s + 1, self.k + 1))
        return 1 / (sum_part1 + middle_part * sum_part2)
    
    def __calculate_probability_n_customers_system(self, p0: float, n: int) -> float:
        if n <= self.s:
            return (self.a**n / factorial(n)) * p0
        elif n <= self.k:
            return (self.a**n) / (factorial(self.s) * self.s**(n - self.s)) * p0
        else:
            return 0.0
        
    def __calculate_probability_k_customers_system(self, p0: float) -> float:
        if self.k <= self.s:
            return (self.a**self.k / factorial(self.k)) * p0
        else:
            return (self.a**self.k) / (factorial(self.s) * self.s**(self.k - self.s)) * p0
        
    def __calculate_avg_customers_queue(self, p0: float) -> float:
        first_part = (p0*(self.a**self.s) * self.rho) / (factorial(self.s) * (1 - self.rho)**2)
        second_part = (1 - self.rho**(self.k - self.s) - (1 - self.rho)*(self.k - self.s)*self.rho**(self.k - self.s))
        return first_part * second_part

    def __calculate_avg_customers_system(self, p0: float, lq: float) -> float:
        first_part = sum(n * self.__calculate_probability_n_customers_system(p0, n) for n in range(self.s)) + lq
        second_part = self.s * (1 - sum(self.__calculate_probability_n_customers_system(p0, n) for n in range(self.s)))
        return first_part + second_part

    def __calculate_avg_time_queue(self, lq: float, pk: float) -> float:
        return lq / (self.lamb * (1 - pk))

    def __calculate_avg_time_system(self, l: float, pk: float) -> float:
        return l / (self.lamb * (1 - pk))