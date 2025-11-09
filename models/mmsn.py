# Desenvolvido por Lucca/Lucas (+ ajustes)
# models/mmsn.py

from math import factorial, comb
from typing import Dict, Optional
from models.base_queue import BaseQueueModel


class MMsN(BaseQueueModel):
    """
    Modelo M/M/s com população finita (N).
    Fórmulas do slide do professor Paulo Maia (M/M/s/N):

      P0 = [ sum_{n=0}^{s-1} C(N,n) (λ/μ)^n
             + sum_{n=s}^{N} [ N!/(N-n)! * (λ/μ)^n / (s! s^{n-s}) ] ]^{-1}

      Pn =
        - para n < s:  C(N,n) (λ/μ)^n * P0
        - para n >= s: [ N!/(N-n)! * (λ/μ)^n / (s! s^{n-s}) ] * P0

      L  = sum_{n=0}^N n * Pn
      Lq = L - (λ/μ) * (N - L)
      λ̄ = λ (N - L)
      W  = L  / λ̄
      Wq = Lq / λ̄
    """

    def __init__(self, lamb: float, mu: float, servers: int, N: int,
                 n_for_prob: Optional[int] = None) -> None:
        super().__init__(lamb, mu, capacity=N)  # aqui, capacity guarda N (população)
        self.s = int(servers)
        self.N = int(N)
        self.a = lamb / mu                           # a = λ/μ
        self.rho = (N * lamb) / (servers * mu)       # ρ = (Nλ)/(sμ)
        self.n_for_prob = n_for_prob

        if self.s <= 0 or self.N <= 0 or self.mu <= 0 or self.lamb < 0:
            raise ValueError("Parâmetros inválidos: requer λ ≥ 0, μ > 0, s ≥ 1 e N ≥ 1.")

    # ----------------- auxiliares -----------------

    def _p0(self) -> float:
        s, N, a = self.s, self.N, self.a

        # soma 1: n = 0 .. min(s-1, N)
        lim1 = min(s - 1, N)
        sum1 = 0.0
        if lim1 >= 0:
            sum1 = sum(comb(N, n) * (a ** n) for n in range(0, lim1 + 1))

        # soma 2: n = s .. N, com fator N!/(N-n)! / (s! s^{n-s})
        sum2 = 0.0
        if s <= N:
            s_fact = factorial(s)
            for n in range(s, N + 1):
                coef = factorial(N) / factorial(N - n)
                sum2 += coef * (a ** n) / (s_fact * (s ** (n - s)))

        denom = sum1 + sum2
        return 1.0 / denom

    def _pn(self, n: int, p0: float) -> float:
        if n < 0 or n > self.N:
            return 0.0
        a, s, N = self.a, self.s, self.N
        if n < s:
            return comb(N, n) * (a ** n) * p0
        else:  # n >= s
            coef = factorial(N) / factorial(N - n)
            return coef * (a ** n) * p0 / (factorial(s) * (s ** (n - s)))

    # ----------------- API pública -----------------

    def calculate_metrics(self) -> Dict:
        p0 = self._p0()
        pn_vals = [self._pn(n, p0) for n in range(0, self.N + 1)]

        # L = Σ n Pn
        L = sum(n * pn_vals[n] for n in range(0, self.N + 1))

        # Lq, λ̄, W, Wq (todas do slide)
        Lq = L - (self.lamb / self.mu) * (self.N - L)
        lamb_bar = self.lamb * (self.N - L)
        if lamb_bar <= 0:
            W = float("inf")
            Wq = float("inf")
        else:
            W = L / lamb_bar
            Wq = Lq / lamb_bar

        out: Dict[str, float] = {
            "ρ = (Nλ)/(sμ)": round(self.rho, 6),
            "P0": round(p0, 6),
            "L": round(L, 6),
            "Lq": round(Lq, 6),
            "λ̄ (lambda efetivo)": round(lamb_bar, 6),
            "W": round(W, 6),
            "Wq": round(Wq, 6),
            # extras úteis p/ conferir com gabaritos:
            "Operacionais médios (N-L)": round(self.N - L, 6),
        }

        # P1 e ociosidades (ajudam na letra (c) do exemplo)
        if self.N >= 1:
            P1 = pn_vals[1]
            out["P1"] = round(P1, 6)
            out["Ociosidade: existe técnico ocioso (P0+P1)"] = round(pn_vals[0] + P1, 6)
            out["Ociosidade média por técnico (P0 + 0.5*P1)"] = round(pn_vals[0] + 0.5 * P1, 6)

        # opcional: Pn solicitado
        if self.n_for_prob is not None:
            n = int(self.n_for_prob)
            out[f"Pn(n={n})"] = round(self._pn(n, p0), 6) if 0 <= n <= self.N else 0.0

        return out
