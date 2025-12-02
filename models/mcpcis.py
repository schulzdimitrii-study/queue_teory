from math import factorial
from typing import Dict

from models.base_queue import BaseQueueModel


class MCPCIS(BaseQueueModel):
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

        self.rho_total = lamb / (s * mu)
        if self.rho_total >= 1:
            raise ValueError("Sistema instável: requer ρ < 1.")
        self.lamb1 = lamb1
        self.lamb2 = lamb2
        self.lamb3 = lamb3
        self.lamb4 = lamb4
        self.lamb_list = [lamb1, lamb2, lamb3, lamb4]

        if self.lamb < 0 or self.mu <= 0 or self.s < 1:
            raise ValueError(
                "Parâmetros inválidos: requer λi ≥ 0, λ ≥ 0, μ > 0 e s ≥ 1."
            )

    def calculate_metrics(self) -> Dict[str, float]:
        # classe 1
        lq1 = self.__calculate_avg_customers_queue_mms(1)
        l1 = self.__calculate_avg_customers_system_mms(1)
        w1 = self.__calculate_avg_time_system_mms(1)
        wq1 = self.__calculate_avg_time_queue_mms(1)

        # classe 2
        w2 = self.__calculate_avg_time_system(2)
        wq2 = self.__calculate_avg_time_queue(2)
        l2 = self.__calculate_avg_customers_system(2)
        lq2 = self.__calculate_avg_customers_queue(2)

        # classe 3
        if self.lamb3 == 0:
            w3 = 0
            wq3 = 0
            l3 = 0
            lq3 = 0
        else:
            w3 = self.__calculate_avg_time_system(3)
            wq3 = self.__calculate_avg_time_queue(3)
            l3 = self.__calculate_avg_customers_system(3)
            lq3 = self.__calculate_avg_customers_queue(3)

        # classe 4
        if self.lamb4 == 0:
            w4 = 0
            wq4 = 0
            l4 = 0
            lq4 = 0
        else:
            w4 = self.__calculate_avg_time_system(4)
            wq4 = self.__calculate_avg_time_queue(4)
            l4 = self.__calculate_avg_customers_system(4)
            lq4 = self.__calculate_avg_customers_queue(4)

        # Sistema
        w = (
            w1 * self.lamb1 + w2 * self.lamb2 + w3 * self.lamb3 + w4 * self.lamb4
        ) / self.lamb
        wq = (
            wq1 * self.lamb1 + wq2 * self.lamb2 + wq3 * self.lamb3 + wq4 * self.lamb4
        ) / self.lamb
        l = l1 + l2 + l3 + l4
        lq = lq1 + lq2 + lq3 + lq4

        data = {
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
                "Rho": round(self.rho_total, 6),
                "W": round(w, 6),
                "Wq": round(wq, 6),
                "L": round(l, 6),
                "Lq": round(lq, 6),
            },
        }

        if self.lamb3 == 0:
            del data["Class 3"]
        if self.lamb4 == 0:
            del data["Class 4"]

        return data

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

    def __calculate_s_sum(self, x: int) -> float:
        r = self.__calculate_lambda_sum(x) / self.mu
        summation = sum((r**num) / factorial(num) for num in range(self.s))

        return summation

    def __calculate_probability_system_empty(self, x: int) -> float:
        r = self.__calculate_lambda_sum(x) / self.mu
        rho = r / self.s
        first_term = self.__calculate_s_sum(x)
        second_term = (r**self.s) / factorial(self.s)
        third_term = 1 / (1 - rho)
        denominator = first_term + second_term * third_term
        p0 = 1 / denominator

        return p0

    # Classe 1

    def __calculate_avg_customers_queue_mms(self, x: int) -> float:
        r = self.__calculate_lambda_sum(x) / self.mu
        rho = r / self.s
        p0 = self.__calculate_probability_system_empty(x)

        numerator = p0 * (r ** (self.s)) * rho
        denominator = factorial(self.s) * ((1 - rho) ** 2)
        lq = numerator / denominator

        return lq

    def __calculate_avg_customers_system_mms(self, x: int) -> float:
        lq = self.__calculate_avg_customers_queue_mms(x)
        r = self.__calculate_lambda_sum(x) / self.mu
        l = lq + r

        return l

    def __calculate_avg_time_system_mms(self, x: int) -> float:
        l = self.__calculate_avg_customers_system_mms(x)
        w = l / self.__calculate_lambda_sum(x)

        return w

    def __calculate_avg_time_queue_mms(self, x: int) -> float:
        w = self.__calculate_avg_time_system_mms(x)
        wq = w - (1 / self.mu)

        return wq

    # Classes 2, 3 e 4

    def __calculate_avg_time_system(self, x: int) -> float:
        # λ1 + ... + λx
        lamb_cum = self.__calculate_lambda_sum(x)

        # W_MS = M/M/s com λ = lamb_cum
        lq_ms = self.__calculate_avg_customers_queue_mms(x)
        wq_ms = lq_ms / lamb_cum
        w_ms = wq_ms + (1 / self.mu)

        # Classe 2:
        if x == 2:
            # W_MS = (λ1/(λ1+λ2)) W1 + (λ2/(λ1+λ2)) W2
            # Isolando W2:
            w1 = self.__calculate_avg_time_system_mms(1)
            coef = self.lamb2 / lamb_cum

            w2 = (w_ms - (self.lamb1 / lamb_cum) * w1) / coef

            return w2

        # Classe 3:
        if x == 3:
            w1 = self.__calculate_avg_time_system_mms(1)
            w2 = self.__calculate_avg_time_system(2)
            coef = self.lamb3 / lamb_cum  # λ3 / (λ1+λ2+λ3)

            w3 = (
                w_ms - (self.lamb1 / lamb_cum) * w1 - (self.lamb2 / lamb_cum) * w2
            ) / coef

            return w3

        # Classe 4: (caso exista e follow same logic)
        if x == 4:
            w1 = self.__calculate_avg_time_system_mms(1)
            w2 = self.__calculate_avg_time_system(2)
            w3 = self.__calculate_avg_time_system(3)
            coef = self.lamb4 / lamb_cum

            w4 = (
                w_ms
                - (self.lamb1 / lamb_cum) * w1
                - (self.lamb2 / lamb_cum) * w2
                - (self.lamb3 / lamb_cum) * w3
            ) / coef

            return w4

    def __calculate_avg_time_queue(self, x: int) -> float:
        w = self.__calculate_avg_time_system(x)
        wq = w - (1 / self.mu)

        return wq

    def __calculate_avg_customers_system(self, x: int) -> float:
        lambda_i = self.__calculate_lambda_sum(x)
        w = self.__calculate_avg_time_system(x)
        l = lambda_i * w

        return l

    def __calculate_avg_customers_queue(self, x: int) -> float:
        lambda_i = self.__calculate_lambda_sum(x)
        l = self.__calculate_avg_customers_system(x)
        lq = l - (lambda_i / self.mu)

        return lq
