import os

from models.queue_m_m_1 import MM1
from models.queue_m_m_1_k import MM1K
from models.queue_m_m_s_most_1_k import MMsK


def main():
    print('Escolha um método para calcular as métricas:')
    print('1. M/M/1')
    print('2. M/M/s>1')
    print('3. M/M/1/K')
    print('4. M/M/s>1/K')
    
    choice = input()
    
    match choice:
        case '1':
            queue = MM1(lamb=5, mu=7)
            queue.print_metrics()
        case '2':
            pass
        case '3':
            queue = MM1K(lamb=5, mu=7, k=5)
            queue.print_metrics()
        case '4':
            os.system('clear')
            lamb = 5
            mu = 7
            k = 5
            # lamb = input('Digite a taxa média de chegada (lambda): ')
            # mu = input('Digite a taxa média de serviço (mu): ')
            # k = input('Digite o valor de K (capacidade máxima do sistema): ')  
            queue = MMsK(lamb=lamb, mu=mu, k=k, s=2, n=5)
            queue.print_metrics()

if __name__ == "__main__":
    main()