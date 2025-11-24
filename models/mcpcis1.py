from typing import Dict

from models.base_queue import BaseQueueModel

class mcpcis1(BaseQueueModel):
    def __init__(
        self, lamb: float, mu: float, k: int, s: int, lamb1: float, lamb2: float, lamb3: float 
    ) -> None:
        super().__init__(lamb, mu, k, s)

        self.lamb1 = lamb1
        self.lamb2 = lamb2
        self.lamb3 = lamb3
        self.r = self.lamb / self.mu
        self.s = s

        # somas acumuladas λ1, λ1+λ2, λ1+λ2+λ3
        self.lamb_sum_1 = self.lamb1
        self.lamb_sum_2 = self.lamb1 + self.lamb2
        self.lamb_sum_3 = self.lamb1 + self.lamb2 + self.lamb3

        if any(l < 0 for l in (lamb1, lamb2, lamb3)) or mu <= 0 or s != 1:
            raise ValueError("Parâmetros inválidos: requer λi ≥ 0, μ > 0 e s = 1.")

    def calculate_metrics(self) -> Dict:
        # Classe 1
        w1 = self.__calculate_avg_time_system_1()
        wq1 = self.__calculate_avg_time_queue_1(w1)
        l1 = self.__calculate_avg_customers_system_1(w1)
        lq1 = self.__calculate_avg_customers_queue_1(l1)

        # Classe 2
        w2 = self.__calculate_avg_time_system_2()
        wq2 = self.__calculate_avg_time_queue_2(w2)
        l2 = self.__calculate_avg_customers_system_2(w2)
        lq2 = self.__calculate_avg_customers_queue_2(l2)

        # Classe 3
        w3 = self.__calculate_avg_time_system_3()
        wq3 = self.__calculate_avg_time_queue_3(w3)
        l3 = self.__calculate_avg_customers_system_3(w3)
        lq3 = self.__calculate_avg_customers_queue_3(l3)

        return {
            # Classe 1
            "W1": round(w1, 4),
            "Wq1": round(wq1, 4),
            "L1": round(l1, 4),
            "Lq1": round(lq1, 4),

            # Classe 2
            "W2": round(w2, 4),
            "Wq2": round(wq2, 4),
            "L2": round(l2, 4),
            "Lq2": round(lq2, 4),

            # Classe 3
            "W3": round(w3, 4),
            "Wq3": round(wq3, 4),
            "L3": round(l3, 4),
            "Lq3": round(lq3, 4),
        }

    # --------- Classe 1 ---------

    def __calculate_avg_time_system_1(self) -> float:
        # W1 = 1 / (μ - λ1)
        return 1 / (self.mu - self.lamb1)

    def __calculate_avg_time_queue_1(self, w1: float) -> float:
        # Wq1 = W1 - 1/μ
        return w1 - (1 / self.mu)

    def __calculate_avg_customers_system_1(self, w1: float) -> float:
        # L1 = λ1 * W1
        return self.lamb_sum_1 * w1

    def __calculate_avg_customers_queue_1(self, l1: float) -> float:
        # Lq1 = L1 - λ1/μ
        return l1 - (self.lamb_sum_1 / self.mu)

    # --------- Classe 2 ---------

    def __calculate_avg_time_system_2(self) -> float:
        # W2 = μ / [(μ - λ1) * (μ - (λ1 + λ2))]
        return self.mu / (
            (self.mu - self.lamb_sum_1) *
            (self.mu - self.lamb_sum_2)
        )

    def __calculate_avg_time_queue_2(self, w2: float) -> float:
        # Wq2 = W2 - 1/μ
        return w2 - (1 / self.mu)

    def __calculate_avg_customers_system_2(self, w2: float) -> float:
        # L2 = (λ1 + λ2) * W2
        return self.lamb_sum_2 * w2

    def __calculate_avg_customers_queue_2(self, l2: float) -> float:
        # Lq2 = L2 - (λ1 + λ2)/μ
        return l2 - (self.lamb_sum_2 / self.mu)

    # --------- Classe 3 ---------

    def __calculate_avg_time_system_3(self) -> float:
        # W3 = μ / {[μ - (λ1 + λ2)] * [μ - (λ1 + λ2 + λ3)]}
        return self.mu / (
            (self.mu - self.lamb_sum_2) *
            (self.mu - self.lamb_sum_3)
        )

    def __calculate_avg_time_queue_3(self, w3: float) -> float:
        # Wq3 = W3 - 1/μ
        return w3 - (1 / self.mu)

    def __calculate_avg_customers_system_3(self, w3: float) -> float:
        # L3 = (λ1 + λ2 + λ3) * W3
        return self.lamb_sum_3 * w3

    def __calculate_avg_customers_queue_3(self, l3: float) -> float:
        # Lq3 = L3 - (λ1 + λ2 + λ3)/μ
        return l3 - (self.lamb_sum_3 / self.mu)