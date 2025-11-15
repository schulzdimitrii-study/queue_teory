from math import comb, factorial
from typing import Dict, Optional

from models.base_queue import BaseQueueModel


class MM1N(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int, n: int, N: int, n_for_prob: Optional[int] = None,
    ) -> None:
        super().__init__(lamb, mu, k, s)
        self.n = n
        self.N = N
        self.n_for_prob = n_for_prob
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

    '''
    def __p0(self) -> float:
        lim1 = min(self.s - 1, self.k)
        sum1 = 0
        if lim1 >= 0:
            sum1 = sum(comb(self.k, n) * (self.a**n) for n in range(0, lim1 + 1))

        sum2 = 0
        if self.s <= self.k:
            s_fact = factorial(self.s)
            for n in range(self.s, self.k + 1):
                coef = factorial(self.k) / factorial(self.k - n)
                sum2 += coef * (self.a**n) / (s_fact * (self.s ** (n - self.s)))

        denom = sum1 + sum2
        return 1.0 / denom

    def __pn(self, n: int, p0: float) -> float:
        if n < 0 or n > self.k:
            return 0.0
        if n < self.s:
            return comb(self.k, n) * (self.a**n) * p0

        coef = factorial(self.k) / factorial(self.k - n)
        return coef * (self.a**n) * p0 / (factorial(self.s) * (self.s ** (n - self.s)))

    def calculate_metrics(self) -> Dict:
        p0 = self.__p0()
        pn_vals = [self.__pn(n, p0) for n in range(0, self.k + 1)]

        l = sum(n * pn_vals[n] for n in range(0, self.k + 1))

        lq = l - (self.lamb / self.mu) * (self.k - l)
        lamb_bar = self.lamb * (self.k - l)
        if lamb_bar <= 0:
            w = float("inf")
            wq = float("inf")
        else:
            w = l / lamb_bar
            wq = lq / lamb_bar

        out = {
            "p = (Nλ)/(sμ)": round(self.rho, 6),
            "P0": round(p0, 6),
            "L": round(l, 6),
            "Lq": round(lq, 6),
            "λ̄ (lambda efetivo)": round(lamb_bar, 6),
            "W": round(w, 6),
            "Wq": round(wq, 6),
            # extras úteis p/ conferir com gabaritos:
            "Operacionais médios (N-L)": round(self.k - l, 6),
        }

        if self.k >= 1:
            p1 = pn_vals[1]
            out["P1"] = round(p1, 6)
            out["Ociosidade: existe técnico ocioso (P0+P1)"] = round(pn_vals[0] + p1, 6)
            out["Ociosidade média por técnico (P0 + 0.5*P1)"] = round(
                pn_vals[0] + 0.5 * p1, 6
            )

        if self.n_for_prob is not None:
            n = int(self.n_for_prob)
            out[f"Pn(n={n})"] = (
                round(self.__pn(n, p0), 6) if 0 <= n <= self.k else 0.0
            )

        return out
    '''
