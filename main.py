from models.mm1 import MM1
from models.mm1k import MM1K
from models.mmsk import MMsK


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
            queue.calculate_metrics()
        case '2':
            pass
        case '3':
            queue = MM1K(lamb=5, mu=7, k=5)
            res = queue.calculate_metrics()
            print(res)
        case '4':
            lamb = float(input('Digite a taxa média de chegada (lambda): '))
            mu = float(input('Digite a taxa média de serviço (mu): '))
            k = float(input('Digite o valor de K (capacidade máxima do sistema): '))
            time = float(input('Digite o tempo t para calcular P(W > t) e P(Wq > t): '))

            queue = MMsK(lamb=lamb, mu=mu, k=k, t=time, servers=2, n=5)
            res = queue.calculate_metrics()
            print(res)

if __name__ == "__main__":
    main()
