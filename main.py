from models.mcpci import MCPCI
from models.mcpcis import MCPCIS
from models.mcpsi import MCPSI
from models.mg1 import MG1
from models.mm1 import MM1
from models.mm1k import MM1K
from models.mm1n import MM1N
from models.mms import MMS
from models.mmsk import MMsK
from models.mmsn import MMSN


def main():
    print("Escolha um método para calcular as métricas:")
    print("1. M/M/1")
    print("2. M/M/s>1")
    print("3. M/M/1/K")
    print("4. M/M/s>1/K")
    print("5. M/M/1 com população finita (N)")
    print("6. M/M/s>1 com população finita (N)")
    print("7. M/G/1")
    print("8. Modelo com prioridade (com interrupção) e um servidor")
    print("9. Modelo com prioridade (com interrupção) e múltiplos servidores")
    print("10. Modelos com prioridade (sem interrupção)")
    choice = input("------- Escolha um modelo -------\n")

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
            s = int(input("Digite o número de servidores (s): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            r = int(input("Digite o número de clientes para Pn (r): "))
            t = float(input("Digite o tempo t para calcular P(W > t) e P(Wq > t): "))
            queue = MMS(lamb=lamb, mu=mu, k=1, s=s, n=n, r=r, t=t)
            res = queue.calculate_metrics()
            print(res)
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
            tam_pop = int(input("Digite o tamanho da população (N): "))
            queue = MM1N(lamb=lamb, mu=mu, k=1, s=1, n=n, N=tam_pop)
            res = queue.calculate_metrics()
            print(res)
        case "6":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            s = int(input("Digite o número de servidores (s): "))
            n = int(input("Digite o número de clientes no sistema (n): "))
            tam_pop = int(input("Digite o tamanho da população (N): "))
            queue = MMSN(lamb=lamb, mu=mu, k=1, s=s, n=n, N=tam_pop)
            res = queue.calculate_metrics()
            print(res)
        case "7":
            lamb = float(input("Digite a taxa média de chegada (lambda): "))
            mu = float(input("Digite a taxa média de serviço (mu): "))
            var = float(
                input(
                    "Digite a variância do tempo de serviço (var, use 0 para tempo constante): "
                )
            )
            queue = MG1(lamb=lamb, mu=mu, k=1, s=1, var=var)
            res = queue.calculate_metrics()
            print(res)
        case "8":
            lamb = float(input("Digite a taxa média de chegada total (lambda_total): "))
            # A taxa total de chegada (lambda_total) deve ser igual à soma das taxas de chegada de todas as classes de prioridade.
            # Para 2 classes, defina lamb3 e lamb4 como 0.
            # Para 3 classes, defina lamb4 como 0.
            # Para 4 classes, preencha todos os valores com números maiores que 0.
            # O código está preparado para até 4 classes, embora normalmente sejam usadas até 3.
            lamb1 = float(
                input(
                    "Digite a taxa média de chegada para a primeira classe de prioridade (lambda1): "
                )
            )
            lamb2 = float(
                input(
                    "Digite a taxa média de chegada para a segunda classe de prioridade (lambda2): "
                )
            )
            lamb3 = float(
                input(
                    "Digite a taxa média de chegada para a terceira classe de prioridade (lambda3): "
                )
            )
            lamb4 = float(
                input(
                    "Digite a taxa média de chegada para a quarta classe de prioridade (lambda4): "
                )
            )

            mu = float(input("Digite a taxa média de serviço (mu): "))

            queue = MCPCI(
                lamb=lamb,
                mu=mu,
                k=1,
                s=1,
                lamb1=lamb1,
                lamb2=lamb2,
                lamb3=lamb3,
                lamb4=lamb4,
            )
            res = queue.calculate_metrics()
            print(res)
        case "9":
            lamb = float(input("Digite a taxa média de chegada total (lambda_total): "))
            # A taxa total de chegada (lambda_total) deve ser igual à soma das taxas de chegada de todas as classes de prioridade.
            # Para 2 classes, defina lamb3 e lamb4 como 0.
            # Para 3 classes, defina lamb4 como 0.
            # Para 4 classes, preencha todos os valores com números maiores que 0.
            # O código está preparado para até 4 classes, embora normalmente sejam usadas até 3.
            lamb1 = float(
                input(
                    "Digite a taxa média de chegada para a primeira classe de prioridade (lambda1): "
                )
            )
            lamb2 = float(
                input(
                    "Digite a taxa média de chegada para a segunda classe de prioridade (lambda2): "
                )
            )
            lamb3 = float(
                input(
                    "Digite a taxa média de chegada para a terceira classe de prioridade (lambda3): "
                )
            )
            lamb4 = float(
                input(
                    "Digite a taxa média de chegada para a quarta classe de prioridade (lambda4): "
                )
            )

            mu = float(input("Digite a taxa média de serviço (mu): "))
            s = int(input("Digite o número de servidores (s): "))

            queue = MCPCIS(
                lamb=lamb,
                mu=mu,
                k=1,
                s=s,
                lamb1=lamb1,
                lamb2=lamb2,
                lamb3=lamb3,
                lamb4=lamb4,
            )
            res = queue.calculate_metrics()
            print(res)
        case "10":
            lamb = float(input("Digite a taxa média de chegada total (lambda_total): "))
            # Lambda total é sempre a soma das taxas de chegada de todas as classes de prioridade
            # Se o Paulo cobrar 2 duas classes, lamb3 e lamb4 serão 0
            # Se forem 3, lamb4 será 0
            # Se forem 4, todos devem ser preenchidos com valores maiores que 0
            # O Paulo falou que não ia cobrar mais do que 3 classes, mas deixei o código preparado para 4
            lamb1 = float(
                input(
                    "Digite a taxa média de chegada para a primeira classe de prioridade (lambda1): "
                )
            )
            lamb2 = float(
                input(
                    "Digite a taxa média de chegada para a segunda classe de prioridade (lambda2): "
                )
            )
            lamb3 = float(
                input(
                    "Digite a taxa média de chegada para a terceira classe de prioridade (lambda3): "
                )
            )
            lamb4 = float(
                input(
                    "Digite a taxa média de chegada para a quarta classe de prioridade (lambda4): "
                )
            )

            mu = float(input("Digite a taxa média de serviço (mu): "))
            s = int(input("Digite o número de servidores (s): "))

            queue = MCPSI(
                lamb=lamb,
                mu=mu,
                k=1,
                s=s,
                lamb1=lamb1,
                lamb2=lamb2,
                lamb3=lamb3,
                lamb4=lamb4,
            )
            res = queue.calculate_metrics()
            print(res)


if __name__ == "__main__":
    main()
