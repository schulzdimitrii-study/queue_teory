class MM1:
    def __init__(self, lamb: float, mu: float) -> None:
        self.lamb = lamb  # Taxa média de chegada (clientes por unidade de tempo)
        self.mu = mu  # Taxa média de serviço (clientes por unidade de tempo)

    def calculate_metrics(self):
        rho = self.lamb / self.mu  # Utilização do sistema
        Lq = (self.lamb**2) / (
            self.mu * (self.mu - self.lamb)
        )  # Número médio de clientes na fila
        L = self.lamb / (self.mu - self.lamb)  # Número médio de clientes no sistema
        Wq = Lq / self.lamb  # Tempo médio de espera na fila
        W = L / self.lamb  # Tempo médio no sistema
        P0 = 1 - rho  # Probabilidade de zero clientes no sistema

        return {"rho": rho, "Lq": Lq, "L": L, "Wq": Wq, "W": W, "P0": P0}

    def print_metrics(self):
        metrics = self.calculate_metrics()
        print("M/M/1 Model:")
        print(f'p = {metrics["rho"]:.2f}')
        print(f'Lq = {metrics["Lq"]:.2f}')
        print(f'L = {metrics["L"]:.2f}')
        print(f'Wq = {metrics["Wq"]:.2f}')
        print(f'W = {metrics["W"]:.2f}')
        print(f'P0 = {metrics["P0"]:.2f}')
