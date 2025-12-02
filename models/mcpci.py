from typing import Dict

from models.base_queue import BaseQueueModel


class MCPCI(BaseQueueModel):
    """Modelo com prioridade (com interrupção) e um servidor"""

    def __init__(
        self,
        lamb: float,
        mu: float,
        k: int,
        s: int,
        lamb1: float,
        lamb2: float,
        lamb3: float,
        lamb4: float,
    ) -> None:
        super().__init__(lamb, mu, k, s)

        self.rho = lamb / (mu)
        if self.rho >= 1:
            raise ValueError("Sistema instável: requer ρ < 1.")
        self.lamb1 = lamb1
        self.lamb2 = lamb2
        self.lamb3 = lamb3
        self.lamb4 = lamb4

        if self.lamb < 0 or self.mu <= 0 or self.s != 1:
            raise ValueError(
                "Parâmetros inválidos: requer λi ≥ 0, λ ≥ 0, μ > 0 e s ≥ 1."
            )

    def calculate_metrics(self) -> Dict[str, float]:
        # classe 1
        # Esses números serão usados em uma função de somar lambdas mais abaixo
        w1 = self.__calculate_avg_time_system(0, 1)
        wq1 = self.__calculate_avg_time_queue(w1)
        l1 = self.__calculate_avg_customers_system(w1, 1)
        lq1 = self.__calculate_avg_customers_queue(l1, 1)

        # classe 2
        w2 = self.__calculate_avg_time_system(1, 2)
        wq2 = self.__calculate_avg_time_queue(w2)
        l2 = self.__calculate_avg_customers_system(w2, 2)
        lq2 = self.__calculate_avg_customers_queue(l2, 2)

        # classe 3
        if self.lamb3 == 0:
            w3 = 0
            wq3 = 0
            l3 = 0
            lq3 = 0
        else:
            w3 = self.__calculate_avg_time_system(2, 3)
            wq3 = self.__calculate_avg_time_queue(w3)
            l3 = self.__calculate_avg_customers_system(w3, 3)
            lq3 = self.__calculate_avg_customers_queue(l3, 3)
        # classe 4
        if self.lamb4 == 0:
            w4 = 0
            wq4 = 0
            l4 = 0
            lq4 = 0
        else:
            w4 = self.__calculate_avg_time_system(3, 4)
            wq4 = self.__calculate_avg_time_queue(w4)
            l4 = self.__calculate_avg_customers_system(w4, 4)
            lq4 = self.__calculate_avg_customers_queue(l4, 4)
        # Sistema
        w = (
            w1 * self.lamb1 + w2 * self.lamb2 + w3 * self.lamb3 + w4 * self.lamb4
        ) / self.lamb
        wq = (
            wq1 * self.lamb1 + wq2 * self.lamb2 + wq3 * self.lamb3 + wq4 * self.lamb4
        ) / self.lamb
        l = l1 + l2 + l3 + l4
        lq = lq1 + lq2 + lq3 + lq4

        return {
            "Class 1": {
                "W1": round(w1, 6),
                "Wq1": round(wq1, 6),
                "L1": round(l1, 6),
                "Lq1": round(lq1, 6),
            },
            "Class 2": {
                "W2": round(w2, 6),
                "Wq2": round(wq2, 6),
                "L2": round(l2, 6),
                "Lq2": round(lq2, 6),
            },
            "Class 3": {
                "W3": round(w3, 6),
                "Wq3": round(wq3, 6),
                "L3": round(l3, 6),
                "Lq3": round(lq3, 6),
            },
            "Class 4": {
                "W4": round(w4, 6),
                "Wq4": round(wq4, 6),
                "L4": round(l4, 6),
                "Lq4": round(lq4, 6),
            },
            "System": {
                "Rho": round(self.rho, 6),
                "W": round(w, 6),
                "Wq": round(wq, 6),
                "L": round(l, 6),
                "Lq": round(lq, 6),
            },
        }

    def __calculate_lambda_sum(self, threshold: int) -> float:
        """
        Calcula a soma das taxas de chegada λ até a classe 'threshold'.
        """
        if threshold <= 0:
            return 0.0
        lambda_sum = 0.0
        if threshold >= 1:
            lambda_sum += self.lamb1
        if threshold >= 2:
            lambda_sum += self.lamb2
        if threshold >= 3:
            lambda_sum += self.lamb3
        if threshold >= 4:
            lambda_sum += self.lamb4
        return lambda_sum

    def __calculate_avg_time_system(self, x: int, y: int) -> float:
        first_term = 1 / self.mu
        second_term = 1 - (self.__calculate_lambda_sum(x) / (self.mu))
        third_term = 1 - (self.__calculate_lambda_sum(y) / (self.mu))
        w = first_term / (second_term * third_term)

        return w

    def __calculate_avg_time_queue(self, w: float) -> float:
        wq = w - (1 / self.mu)
        return wq

    def __calculate_avg_customers_system(self, w: float, x: int) -> float:
        soma_lambdas = self.__calculate_lambda_sum(x)
        l = soma_lambdas * w
        return l

    def __calculate_avg_customers_queue(self, l: float, x: int) -> float:
        soma_lambdas = self.__calculate_lambda_sum(x)
        lq = l - (soma_lambdas / self.mu)
        return lq
