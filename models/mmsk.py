from math import factorial
from typing import Dict

from models.base_queue import BaseQueueModel


class MMsK(BaseQueueModel):
    def __init__(self, lamb: float, mu: float, k: float, servers: int = 1, customers: int = 0) -> None:
        super().__init__(lamb, mu, k)
        self.rho = lamb / mu # System utilization
        self.s = servers     # Number of servers
        self.n = customers   # Number of customers in the system

    def calculate_metrics(self) -> Dict[str, float]:
        p0 = self.__calculate_probability_system_empty()
        l = self.__calculate_avg_customers_system()
        lq = self.__calculate_avg_customers_queue(l, p0)
        pn = self.__calculate_probability_n_customers_system(self.n)
        wq = self.__calculate_avg_time_queue(lq, pn)
        w = self.__calculate_avg_time_system(l, pn)

        return {
            "P0": p0,
            "L": l,
            "Lq": lq,
            "Pn": pn,
            "Wq": wq,
            "W": w
        }

    def __calculate_probability_system_empty(self) -> float:
        """ P0 = (1 - p) / (1 - p^(K + 1)) """
        return (1 - self.rho) / (1 - self.rho**(self.k + 1))

    def __calculate_avg_customers_system(self) -> float:
        """ L = (p / (1 - p)) - ((K + 1) * p^(K + 1) / (1 - p^(K + 1))) """
        return (self.rho / (1 - self.rho) - ((self.k + 1) * self.rho**(self.k + 1) / (1 - self.rho**(self.k + 1))))

    def __calculate_avg_customers_queue(self, l: float, p0: float) -> float:
        """ Lq = L - (1 - P0) """
        return l - (1 - p0)

    def __calculate_probability_n_customers_system(self, n: int) -> float:
        if n <= self.s:
            pn = (self.rho**n / factorial(n)) * self.__calculate_probability_system_empty()
        else:
            pn = (1 - self.rho) * self.rho**n / (1 - self.rho**(self.k + 1))
        return pn

    def __calculate_avg_time_queue(self, lq: float, pn: float) -> float:
        """ Wq = Lq / λ(1 - Pn) """
        return lq / (self.lamb * (1 - pn))

    def __calculate_avg_time_system(self, l: float, pn: float) -> float:
        """ W = L / λ(1 - Pn) """
        return l / (self.lamb * (1 - pn))
