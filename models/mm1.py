from math import exp
from typing import Dict

from models.base_queue import BaseQueueModel

class MM1(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int , s: int, n: int, r: int, t: float
    ) -> None:
        super().__init__(lamb, mu, k, s)
        self.rho = lamb / mu  # Taxa de utilização do sistema
        self.n = n # Número de clientes no sistema para Pn
        self.r = r # Número de clientes para Pn
        self.t = t # Tempo t para calcular P(W > t) e P(Wq > t)

        if lamb < 0 or mu <= 0 or s != 1:
            raise ValueError("Parâmetros inválidos: requer λ ≥ 0, μ > 0 e s = 1.")
        if n < 0 or r < 0 or t < 0:
            raise ValueError("Parâmetros inválidos: n, r e t devem ser não negativos.")
        if lamb >= mu:
            raise ValueError("Sistema instável: ρ deve ser menor que 1.")

    def calculate_metrics(self) -> Dict:
        p0 = self.__calculate_probability_system_empty()
        pn = self.__calculate_probability_n_customers_system()
        pr = self.__calculate_probability_n_customers_exceeding_r_system()
        l = self.__calculate_avg_customers_system()
        lq = self.__calculate_avg_customers_queue()
        w = self.__calculate_avg_time_system()
        wq = self.__calculate_avg_time_queue()
        pw = self.__calculate_waiting_time_system_exceeding_t()
        pwq = self.__calculate_waiting_time_queue_exceeding_t()

        return {
            "Rho": round(self.rho, 4),
            "P0": round(p0, 4),
            "Pn": round(pn, 4),
            "Pr": round(pr, 4),
            "L": round(l, 4),
            "Lq": round(lq, 4),
            "W": round(w, 4),
            "Wq": round(wq, 4),
            "pw": round(pw, 4),
            "pwq": round(pwq, 4)
        }
    
    def __calculate_probability_system_empty(self) -> float:
        return 1 - self.rho
    
    def __calculate_probability_n_customers_system(self) -> float:
        return (1 - self.rho) * self.rho**self.n
    
    def __calculate_probability_n_customers_exceeding_r_system(self) -> float:
        return self.rho**(self.r + 1)
    
    def __calculate_avg_customers_system(self) -> float:
        return self.rho / (1 - self.rho)
    
    def __calculate_avg_customers_queue(self) -> float:
        return self.rho**2 / (1 - self.rho)
    
    def __calculate_avg_time_system(self) -> float:
        return 1 / (self.mu - self.lamb)
    
    def __calculate_avg_time_queue(self) -> float:
        return 60 * self.rho / (self.mu * (1 - self.rho))
    
    def __calculate_waiting_time_system_exceeding_t(self) -> float:
        return exp(-1 * (self.mu - self.lamb) * self.t)
    
    def __calculate_waiting_time_queue_exceeding_t(self) -> float:
        return self.rho * exp(-1 * (self.mu - self.lamb) * self.t)