# models/mm1.py
from .base_queue import BaseQueueModel
from typing import Dict
import math

class MM1Queue(BaseQueueModel):
    """
    Modelo M/M/1 - Fila com um único servidor
    População infinita, capacidade pode ser finita ou infinita
    """
    
    def __init__(self, arrival_rate: float, service_rate: float, capacity: int = float('inf')) -> None:
        super().__init__(arrival_rate, service_rate, capacity, 1)
        self.rho = self.lamb / self.mu  # Intensidade de tráfego
    
    def calculate_metrics(self) -> Dict:
        """Calcula todas as métricas do sistema M/M/1"""
        
        if self.capacity == float('inf'):
            return self._calculate_infinite_capacity()
        else:
            return self._calculate_finite_capacity()
    
    def _calculate_infinite_capacity(self) -> Dict:
        """Calcula métricas para sistema com capacidade infinita"""
        
        # Verificar estabilidade
        is_stable = self.rho < 1
        
        if not is_stable:
            # Sistema instável - retornar valores limites
            return {
                'system': 'M/M/1',
                'arrival_rate': self.lamb,
                'service_rate': self.mu,
                'servers': 1,
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
        
        # Sistema estável
        p0 = 1 - self.rho
        l = self.rho / (1 - self.rho)
        lq = self.rho ** 2 / (1 - self.rho)
        w = 1 / (self.mu - self.lamb)
        wq = self.rho / (self.mu - self.lamb)
        
        return {
            'system': 'M/M/1',
            'arrival_rate': self.lamb,
            'service_rate': self.mu,
            'servers': 1,
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
        """Calcula métricas para sistema com capacidade finita (M/M/1/K)"""
        
        if self.rho == 1:
            # Caso especial quando rho = 1
            p0 = 1 / (self.capacity + 1)
            l = self.capacity / 2
            lq = (self.capacity - 1) * self.capacity / (2 * (self.capacity + 1))
        else:
            # Caso geral
            p0 = (1 - self.rho) / (1 - self.rho ** (self.capacity + 1))
            l = self.rho / (1 - self.rho) - (self.capacity + 1) * self.rho ** (self.capacity + 1) / (1 - self.rho ** (self.capacity + 1))
            
            # Calcular Lq baseado em L
            pN = p0 * (self.rho ** self.capacity)
            lq = l - (1 - pN)  # Lq = L - (1 - P0)
        
        # Taxa efetiva de chegada
        pN = p0 * (self.rho ** self.capacity) if self.rho != 1 else 1 / (self.capacity + 1)
        lambda_eff = self.lamb * (1 - pN)
        
        # Tempos médios (Lei de Little)
        w = l / lambda_eff if lambda_eff > 0 else float('inf')
        wq = lq / lambda_eff if lambda_eff > 0 else float('inf')
        
        return {
            'system': f'M/M/1/{self.capacity}',
            'arrival_rate': self.lamb,
            'service_rate': self.mu,
            'servers': 1,
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
        if n < 0 or (self.capacity != float('inf') and n > self.capacity):
            return 0.0
        
        metrics = self.calculate_metrics()
        p0 = metrics['p0']
        
        if self.capacity == float('inf'):
            return p0 * (self.rho ** n)
        else:
            if self.rho == 1:
                return 1 / (self.capacity + 1)
            else:
                return p0 * (self.rho ** n)
    
    def probability_wait_exceeds(self, t: float) -> float:
        """Probabilidade do tempo de espera na fila exceder t"""
        if self.capacity != float('inf'):
            return 0.0  # Cálculo complexo para sistema finito
        
        metrics = self.calculate_metrics()
        if not metrics['is_stable']:
            return 1.0
        
        return self.rho * math.exp(-self.mu * (1 - self.rho) * t)