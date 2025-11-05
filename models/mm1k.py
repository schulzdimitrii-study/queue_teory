from math import exp
from typing import Dict

from models.base_queue import BaseQueueModel


class MM1K(BaseQueueModel):
    def __init__(self, lamb: float, mu: float, k: float) -> None:
        super().__init__(lamb, mu, k)
        self.rho = lamb / mu

    def calculate_metrics(self) -> Dict:
        p0 = self.__calculate_probability_system_empty()
        l = self.__calculate_avg_customers_system()
        lq = self.__calculate_avg_customers_queue(l, p0)
        pn = self.__calculate_probability_n_customers_system(2)
        wq = self.__calculate_avg_time_queue(lq, pn)
        w = self.__calculate_avg_time_system(l, pn)
        pw = self.__calculate_waiting_time_exceeding_t(self.mu, 3)
        pwq = self.__calculate_waiting_time_queue_exceeding_t(self.mu, 3)

        return {
            "P0": round(p0, 2),
            "L": round(l, 2),
            "Lq": round(lq, 2),
            "Pn": round(pn, 2),
            "pw": round(pw, 2),
            "pwq": round(pwq, 2),
            "Wq": round(wq),
            "W": round(w)
        }

    def __calculate_probability_system_empty(self) -> float:
        if self.rho == 1:
            return 1 / (self.k + 1)

        return (1 - self.rho) / (1 - self.rho**(self.k + 1))

    def __calculate_avg_customers_queue(self, l: float, p0: float) -> float:
        return l - (1 - p0)

    def __calculate_avg_customers_system(self) -> float:
        return self.rho / (1 - self.rho) - ((self.k + 1) * self.rho**(self.k + 1) / (1 - self.rho**(self.k + 1)))

    def __calculate_probability_n_customers_system(self, n: int) -> float:
        return (1 - self.rho) * self.rho**n / (1 - self.rho**(self.k + 1))

    def __calculate_avg_time_queue(self, lq: float, pn: float) -> float:
        return lq / (self.lamb * (1 - pn))

    def __calculate_avg_time_system(self, l: float, pn: float) -> float:
        return l / (self.lamb * (1 - pn))

    def __calculate_waiting_time_exceeding_t(self, mu: float, t: float) -> float:
        return exp(-mu * t * (1 - self.rho))

    def __calculate_waiting_time_queue_exceeding_t(self, mu: float, t: float) -> float:
        return self.rho * exp(-mu * t * (1 - self.rho))
