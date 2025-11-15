from typing import Dict

from models.base_queue import BaseQueueModel

class MM1K(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int, n: int
    ) -> None:
        super().__init__(lamb, mu, k, s)
        self.rho = lamb / mu
        self.k = k  # Capacidade máxima do sistema
        self.n = n # Número de clientes no sistema para Pn

        if lamb < 0 or mu <= 0 or s != 1:
            raise ValueError("Parâmetros inválidos: requer λ ≥ 0, μ > 0 e s = 1.")
        if n < 0 or k < 0:
            raise ValueError("Parâmetros inválidos: n e k devem ser não negativos.")
        if lamb >= mu:
            raise ValueError("Sistema instável: ρ deve ser menor que 1.")

    def calculate_metrics(self) -> Dict:
        p0 = self.__calculate_probability_system_empty()
        pn = self.__calculate_probability_n_customers_system()
        pk = self.__calculate_probability_k_customers_system()
        l = self.__calculate_avg_customers_system()
        lq = self.__calculate_avg_customers_queue(l, p0)
        w = self.__calculate_avg_time_system(l, pk)
        wq = self.__calculate_avg_time_queue(lq, pk)

        return {
            "P0": round(p0, 4),
            "Pn": round(pn, 4),
            "L": round(l, 4),
            "Lq": round(lq, 4),
            "W": round(w, 4),
            "Wq": round(wq, 4)
        }

    def __calculate_probability_system_empty(self) -> float:
        if self.rho == 1:
            return 1 / (self.k + 1)

        return (1 - self.rho) / (1 - self.rho ** (self.k + 1))
    
    def __calculate_probability_n_customers_system(self) -> float:
        return ((1 - self.rho) * (self.rho**self.n)) / (1 - self.rho ** (self.k + 1))
    
    def __calculate_probability_k_customers_system(self) -> float:
        return ((1 - self.rho) * (self.rho**self.k)) / (1 - self.rho ** (self.k + 1))
    
    def __calculate_avg_customers_system(self) -> float:
        first_part = self.rho / (1 - self.rho)
        last_part = ((self.k + 1) * (self.rho ** (self.k + 1))) / (1 - self.rho ** (self.k + 1))
        return first_part - last_part

    def __calculate_avg_customers_queue(self, l: float, p0: float) -> float:
        return l - (1 - p0)
    
    def __calculate_avg_time_system(self, l: float, pk: float) -> float:
        return l / (self.lamb * (1 - pk))

    def __calculate_avg_time_queue(self, lq: float, pk: float) -> float:
        return lq / (self.lamb * (1 - pk))