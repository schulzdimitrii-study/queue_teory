# models/mmsk.py
from .base_queue import BaseQueueModel
from typing import Dict
import math

class MMsQueue(BaseQueueModel):
    """
    Modelo M/M/s - Fila com múltiplos servidores
    População infinita, capacidade pode ser finita ou infinita
    """
    
    def __init__(self, arrival_rate: float, service_rate: float, servers: int, capacity: int = float('inf')) -> None:
        super().__init__(arrival_rate, service_rate, capacity, servers)
        self.rho = self.lamb / (self.s * self.mu)  # Intensidade de tráfego por servidor
    
    def calculate_metrics(self) -> Dict:
        """Calcula todas as métricas do sistema M/M/s"""
        
        if self.capacity == float('inf'):
            return self._calculate_infinite_capacity()
        else:
            return self._calculate_finite_capacity()
    
    def _calculate_infinite_capacity(self) -> Dict:
        """Calcula métricas para sistema com capacidade infinita"""
        
        # Verificar estabilidade
        is_stable = self.rho < 1
        
        # Calcular P0
        sum_part = 0
        for n in range(self.s):
            sum_part += (self.lamb / self.mu) ** n / math.factorial(n)
        
        p0_denominator = sum_part + ((self.lamb / self.mu) ** self.s / 
                                   math.factorial(self.s)) * (1 / (1 - self.rho))
        p0 = 1 / p0_denominator if is_stable else 0.0
        
        if not is_stable:
            # Sistema instável
            return {
                'system': f'M/M/{self.s}',
                'arrival_rate': self.lamb,
                'service_rate': self.mu,
                'servers': self.s,
                'capacity': '∞',
                'traffic_intensity': self.rho,
                'is_stable': False,
                'p0': 0.0,
                'l': float('inf'),
                'lq': float('inf'),
                'w': float('inf'),
                'wq': float('inf'),
                'effective_arrival_rate': self.lamb
            }
        
        # Calcular Lq
        lq = (p0 * (self.lamb / self.mu) ** self.s * self.rho / 
              (math.factorial(self.s) * (1 - self.rho) ** 2))
        
        # Calcular outras métricas
        l = lq + (self.lamb / self.mu)
        wq = lq / self.lamb
        w = wq + (1 / self.mu)
        
        return {
            'system': f'M/M/{self.s}',
            'arrival_rate': self.lamb,
            'service_rate': self.mu,
            'servers': self.s,
            'capacity': '∞',
            'traffic_intensity': self.rho,
            'is_stable': True,
            'p0': p0,
            'l': l,
            'lq': lq,
            'w': w,
            'wq': wq,
            'effective_arrival_rate': self.lamb
        }
    
    def _calculate_finite_capacity(self) -> Dict:
        """Calcula métricas para sistema com capacidade finita (M/M/s/K)"""
        
        # Calcular P0
        p0_sum = 0
        for n in range(0, self.s + 1):
            p0_sum += (self.lamb / self.mu) ** n / math.factorial(n)
        
        for n in range(self.s + 1, self.capacity + 1):
            p0_sum += (self.lamb / self.mu) ** n / (math.factorial(self.s) * (self.s ** (n - self.s)))
        
        p0 = 1 / p0_sum
        
        # Calcular L (número médio no sistema)
        l = 0
        for n in range(1, self.capacity + 1):
            if n <= self.s:
                pn = ((self.lamb / self.mu) ** n / math.factorial(n)) * p0
            else:
                pn = ((self.lamb / self.mu) ** n / 
                      (math.factorial(self.s) * (self.s ** (n - self.s)))) * p0
            l += n * pn
        
        # Calcular Lq (número médio na fila)
        lq = 0
        for n in range(self.s + 1, self.capacity + 1):
            if n <= self.s:
                pn = ((self.lamb / self.mu) ** n / math.factorial(n)) * p0
            else:
                pn = ((self.lamb / self.mu) ** n / 
                      (math.factorial(self.s) * (self.s ** (n - self.s)))) * p0
            lq += (n - self.s) * pn
        
        # Taxa efetiva de chegada
        pN = self.probability_n_customers(self.capacity)
        lambda_eff = self.lamb * (1 - pN)
        
        # Tempos médios (Lei de Little)
        w = l / lambda_eff if lambda_eff > 0 else float('inf')
        wq = lq / lambda_eff if lambda_eff > 0 else float('inf')
        
        return {
            'system': f'M/M/{self.s}/{self.capacity}',
            'arrival_rate': self.lamb,
            'service_rate': self.mu,
            'servers': self.s,
            'capacity': self.capacity,
            'traffic_intensity': self.rho,
            'is_stable': True,  # Sempre estável com capacidade finita
            'p0': p0,
            'l': l,
            'lq': lq,
            'w': w,
            'wq': wq,
            'effective_arrival_rate': lambda_eff,
            'pN': pN  # Probabilidade do sistema estar cheio
        }
    
    def probability_n_customers(self, n: int) -> float:
        """Probabilidade de haver exatamente n clientes no sistema"""
        if n < 0 or n > self.capacity:
            return 0.0
        
        metrics = self.calculate_metrics()
        p0 = metrics['p0']
        
        if n <= self.s:
            return ((self.lamb / self.mu) ** n / math.factorial(n)) * p0
        else:
            return ((self.lamb / self.mu) ** n / 
                   (math.factorial(self.s) * (self.s ** (n - self.s)))) * p0
    
    def probability_no_wait(self) -> float:
        """Probabilidade de um cliente não precisar esperar"""
        prob = 0
        for n in range(self.s):
            prob += self.probability_n_customers(n)
        return prob
    
    def probability_all_servers_busy(self) -> float:
        """Probabilidade de todos os servidores estarem ocupados"""
        prob = 0
        max_n = self.capacity if self.capacity != float('inf') else self.s + 10
        for n in range(self.s, max_n + 1):
            prob += self.probability_n_customers(n)
        return prob