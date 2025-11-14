from models.mm1 import MM1
from models.mm1k import MM1K
from models.mmsk import MMsK
from models.mmsn import MMsN


def main():
    print("Escolha um método para calcular as métricas:")
    print("1. M/M/1")
    print("2. M/M/s>1")
    print("3. M/M/1/K")
    print("4. M/M/s>1/K")
    print("5. M/M/s com população finita (N)")
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
            k = float(input("Digite o valor de K (capacidade máxima do sistema): "))
            time = float(input("Digite o tempo t para calcular P(W > t) e P(Wq > t): "))

            queue = MMsK(lamb=lamb, mu=mu, k=k, t=time, servers=2, n=5)
            res = queue.calculate_metrics()
            print(res)
        case "5":
            print("\n[M/M/s com população finita (N)]")
            lamb = float(input("Digite λ (taxa média de chegada): "))
            mu = float(input("Digite μ (taxa média de serviço): "))
            s = int(input("Digite s (número de servidores): "))
            N = int(input("Digite N (tamanho da população finita): "))
            n = int(
                input("Opcional: valor de n para calcular Pn (ou -1 para ignorar): ")
            )

            n_for_prob = None if n < 0 else n
            queue = MMsN(lamb=lamb, mu=mu, servers=s, n=N, n_for_prob=n_for_prob)
            res = queue.calculate_metrics()
            print(res)


if __name__ == "__main__":
    main()
