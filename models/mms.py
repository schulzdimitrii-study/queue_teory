from math import exp
from math import factorial
from typing import Dict


from models.base_queue import BaseQueueModel

class MMs(BaseQueueModel):
    def __init__(
            self, lamb: float, mu: float, k: int , s: int, n: int, r: int,t: float
        ) -> None:
        super().__init__(lamb, mu, k, s)
        self.rho = lamb / (s * mu)  # Taxa de utilização do sistema
        self.a = lamb / mu  # Variável auxiliar A
        self.n = n # Número de clientes no sistema para Pn
        self.r = r # Número de clientes para Pr
        self.t = t # Tempo t para calcular P(W > t) e P(Wq > t)

        if s <= 1:
            raise ValueError("Número de servidores deve ser maior que 1.")
        if lamb >= mu*s:
            raise ValueError("Sistema instável: λ deve ser menor que s*μ.")
        if self.rho >= 1:
            raise ValueError("Sistema instável: ρ deve ser menor que 1.")
        if n < 0 or t < 0:
            raise ValueError("n e t devem ser valores não negativos.")

    def calculate_metrics(self) -> Dict:
        p0 = self.__calculate_probability_system_empty()
        pn = self.__calculate_probability_n_customers_system(self.n, p0)
        pr = self.__calculate_probability_n_customers_exceeding_r_system(self.n, p0)
        pw = self.__calculate_waiting_time_system_exceeding_t(p0)
        pwq = self.__calculate_waiting_time_queue_exceeding_t(p0)
        lq = self.__calculate_avg_customers_queue(p0)
        wq = self.__calculate_avg_time_queue(lq)
        l = self.__calculate_avg_customers_system(lq)
        w = self.__calculate_avg_time_system(wq)

        return {
            "Rho": round(self.rho, 2),
            "P0": round(p0, 2),
            "Pn": round(pn, 2),
            "Pr": round(pr, 2),
            "pw": round(pw, 2),
            "pwq": round(pwq, 2),
            "Lq": round(lq, 2),
            "Wq": round(wq, 2),
            "L": round(l, 2),
            "W": round(w, 2)
        }
    
    def __calculate_probability_system_empty(self) -> float:
        sum_terms = sum((self.a)**n / factorial(n) for n in range(self.s))
        last_term = ((self.a)**self.s) / (factorial(self.s) * (1 - self.rho))
        p0 = 1 / (sum_terms + last_term)
        return p0

    def __calculate_probability_n_customers_system(self, n:int, p0:float) -> float:
        if n < self.s:
            pn =(p0 * (self.a**n)) / factorial(n)
        else:
            pn = (p0 * (self.a**n)) / (factorial(self.s) * (self.s**(n - self.s)))
        return pn
    
    def __calculate_probability_n_customers_exceeding_r_system(self, r:int, p0:float) -> float:
        pr = 1 - sum(self.__calculate_probability_n_customers_system(n, p0) for n in range(r + 1))
        return pr
    
    def __calculate_waiting_time_system_exceeding_t(self, p0:float) -> float:
        first_term = (p0 * (self.a**self.s)) / (factorial(self.s) * (1 - self.rho))
        second_term = (1 - exp(-1 * (self.mu * (self.s - 1 - self.a) * self.t)))/(self.s - 1 - self.a)
        pw = exp(-1 * (self.mu * self.t))*(1 + first_term * second_term)
        return pw
    
    def __calculate_waiting_time_queue_exceeding_t(self, p0:float) -> float:
        pwq0 = sum(self.__calculate_probability_n_customers_system(n, p0) for n in range(self.s))
        first_term = (1 - pwq0)
        second_term = exp(-1 * (self.s * self.mu * (1 - self.rho) * self.t))
        pwq  = first_term * second_term
        return pwq
    
    def __calculate_avg_customers_queue(self, p0:float) -> float:
        numerator = (p0 * (self.a**(self.s)) * self.rho)
        denominator = factorial(self.s) * ((1 - self.rho)**2)
        lq = numerator / denominator
        return lq
    
    def __calculate_avg_time_queue(self, lq:float) -> float:
        wq = lq / self.lamb
        return wq
    
    def __calculate_avg_customers_system(self, lq:float) -> float:
        l = lq + self.a
        return l
    
    def __calculate_avg_time_system(self, wq:float) -> float:
        w = wq + (1 / self.mu)
        return w