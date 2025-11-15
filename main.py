from models.mm1 import MM1
from models.mm1k import MM1K
from models.mmsk import MMsK
from models.mm1n import MM1N


def main():
    print("Escolha um método para calcular as métricas:")
    print("1. M/M/1")
    print("2. M/M/s>1")
    print("3. M/M/1/K")
    print("4. M/M/s>1/K")
    print("5. M/M/1 com população finita (N)")
    choice = input()

    match choice:
        case "1":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            r = int(input("Digite o número de clientes para Pn (r): "))
            t = float(input("Digite o tempo t para calcular P(W > t) e P(Wq > t): "))
            queue = MM1(lamb=lamb, mu=mu, k=1, s=1, n=n, r=r, t=t)
            res = queue.calculate_metrics()
            print(res)
        case "2":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            servers = int(input("Digite o número de servidores (s): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            r = int(input("Digite o número de clientes para Pn (r): "))
            t = float(input("Digite o tempo t para calcular P(W > t) e P(Wq > t): "))
            queue = MMsK(lamb=lamb, mu=mu, k=float('inf'), servers=servers, n=n, r=r, t=t)
            res = queue.calculate_metrics()
        case "3":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            k = int(input("Digite o valor de K (capacidade máxima do sistema): "))
            queue = MM1K(lamb=lamb, mu=mu, k=k, s=1, n=n)
            res = queue.calculate_metrics()
            print(res)
        case "4":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            s = int(input("Digite o número de servidores (s): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            k = int(input("Digite o valor de K (capacidade máxima do sistema): "))
            queue = MMsK(lamb=lamb, mu=mu, k=k, s=s, n=n)
            res = queue.calculate_metrics()
            print(res)
        case "5":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            N = int(input("Digite o tamanho da população (N): "))
            n_for_prob = None if n < 0 else n
            queue = MM1N(lamb=lamb, mu=mu, k=1, s=1, n=n, N=N, n_for_prob=n_for_prob)
            res = queue.calculate_metrics()
            print(res)


if __name__ == "__main__":
    main()
