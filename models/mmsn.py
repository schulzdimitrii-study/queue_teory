from math import comb, factorial
from typing import Dict, Optional

from models.base_queue import BaseQueueModel


class MMsN(BaseQueueModel):
    def __init__(
        self,
        lamb: float,
        mu: float,
        servers: int,
        n: int,
        n_for_prob: Optional[int] = None,
    ) -> None:
        super().__init__(lamb, mu, capacity=n, servers=servers)
        self.a = lamb / mu
        self.rho = (n * lamb) / (servers * mu)
        self.n_for_prob = n_for_prob

        if self.s <= 0 or self.capacity <= 0 or self.mu <= 0 or self.lamb < 0:
            raise ValueError(
                "Parâmetros inválidos: requer λ ≥ 0, μ > 0, s ≥ 1 e N ≥ 1."
            )

    def __p0(self) -> float:
        lim1 = min(self.s - 1, self.capacity)
        sum1 = 0
        if lim1 >= 0:
            sum1 = sum(comb(self.capacity, n) * (self.a**n) for n in range(0, lim1 + 1))

        sum2 = 0
        if self.s <= self.capacity:
            s_fact = factorial(self.s)
            for n in range(self.s, self.capacity + 1):
                coef = factorial(self.capacity) / factorial(self.capacity - n)
                sum2 += coef * (self.a**n) / (s_fact * (self.s ** (n - self.s)))

        denom = sum1 + sum2
        return 1.0 / denom

    def __pn(self, n: int, p0: float) -> float:
        if n < 0 or n > self.capacity:
            return 0.0
        if n < self.s:
            return comb(self.capacity, n) * (self.a**n) * p0

        coef = factorial(self.capacity) / factorial(self.capacity - n)
        return coef * (self.a**n) * p0 / (factorial(self.s) * (self.s ** (n - self.s)))

    def calculate_metrics(self) -> Dict:
        p0 = self.__p0()
        pn_vals = [self.__pn(n, p0) for n in range(0, self.capacity + 1)]

        l = sum(n * pn_vals[n] for n in range(0, self.capacity + 1))

        lq = l - (self.lamb / self.mu) * (self.capacity - l)
        lamb_bar = self.lamb * (self.capacity - l)
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
            "Operacionais médios (N-L)": round(self.capacity - l, 6),
        }

        if self.capacity >= 1:
            p1 = pn_vals[1]
            out["P1"] = round(p1, 6)
            out["Ociosidade: existe técnico ocioso (P0+P1)"] = round(pn_vals[0] + p1, 6)
            out["Ociosidade média por técnico (P0 + 0.5*P1)"] = round(
                pn_vals[0] + 0.5 * p1, 6
            )

        if self.n_for_prob is not None:
            n = int(self.n_for_prob)
            out[f"Pn(n={n})"] = (
                round(self.__pn(n, p0), 6) if 0 <= n <= self.capacity else 0.0
            )

        return out
