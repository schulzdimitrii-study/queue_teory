from math import exp, factorial
from typing import Dict

from models.base_queue import BaseQueueModel


class MMsK(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: float, t: int, servers: int, n: int = 0
    ) -> None:
        super().__init__(lamb, mu, k, servers)
        self.rho = lamb / mu
        self.s = servers
        self.n = n
        self.time = t

    def calculate_metrics(self) -> Dict[str, float]:
        p0 = self.__calculate_probability_system_empty()
        l = self.__calculate_avg_customers_system()
        lq = self.__calculate_avg_customers_queue(l, p0)
        pn = self.__calculate_probability_n_customers_system(self.n)
        wq = self.__calculate_avg_time_queue(lq, pn)
        w = self.__calculate_avg_time_system(l, pn)
        pw = self.__calculate_waiting_time_exceeding_t(
            self.p0, self.lamb, self.mu, self.s
        )
        pwq = self.__calculate_waiting_time_queue_exceeding_t(self.mu, 3)

        return {
            "P0": round(p0, 2),
            "L": round(l, 2),
            "Lq": round(lq, 2),
            "Pn": round(pn, 2),
            "pw": round(pw, 2),
            "pwq": round(pwq, 2),
            "Wq": round(wq),
            "W": round(w),
        }

    def __calculate_probability_system_empty(self) -> float:
        return (1 - self.rho) / (1 - self.rho ** (self.capacity + 1))

    def __calculate_avg_customers_system(self) -> float:
        return self.rho / (1 - self.rho) - (
            (self.capacity + 1)
            * self.rho ** (self.capacity + 1)
            / (1 - self.rho ** (self.capacity + 1))
        )

    def __calculate_avg_customers_queue(self, l: float, p0: float) -> float:
        return l - (1 - p0)

    def __calculate_probability_n_customers_system(self, n: int) -> float:
        if n <= self.s:
            pn = (
                self.rho**n / factorial(n)
            ) * self.__calculate_probability_system_empty()
        else:
            pn = (1 - self.rho) * self.rho**n / (1 - self.rho ** (self.capacity + 1))
        return pn

    def __calculate_avg_time_queue(self, lq: float, pn: float) -> float:
        return lq / (self.lamb * (1 - pn))

    def __calculate_avg_time_system(self, l: float, pn: float) -> float:
        return l / (self.lamb * (1 - pn))

    def __calculate_waiting_time_exceeding_t(
        self, p0: float, lamb: float, mu: float, s: int
    ) -> float:
        numerator = (
            p0 * (lamb / mu) ** s * (1 - exp(-mu * self.time * (s - 1 - lamb / mu)))
        )
        denominator = factorial(s) * (1 - self.rho) * (s - 1 - lamb / mu)

        return exp(-mu * self.time) * (1 + numerator / denominator)

    def __calculate_waiting_time_queue_exceeding_t(self, mu: float, s: int) -> float:
        probability_wq_equal_zero = sum(
            self.__calculate_probability_n_customers_system(n) for n in range(s)
        )

        return (1 - probability_wq_equal_zero) * exp(
            -s * mu * (1 - self.rho) * self.time
        )
