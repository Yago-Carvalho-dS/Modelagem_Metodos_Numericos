import numpy as np

TOLERANCIA_ZERO = 1e-12  

def eliminacao_gauss(A, b, pivoteamento=False):
    n = len(A)
    if any(len(linha) != n for linha in A) or len(b) != n:
        print("Erro! A matriz precisa ser quadrada (n x n) e b precisa ter n valores.")
        return None

    M = np.array([list(A[i]) + [b[i]] for i in range(n)], dtype=float)

    print("\nMatriz aumentada inicial [A | b]:")
    print(M)

    for k in range(n - 1):

        if pivoteamento:
            maior = k
            for i in range(k + 1, n):
                if abs(M[i, k]) > abs(M[maior, k]):
                    maior = i
            if maior != k:
                M[[k, maior]] = M[[maior, k]]
                print(f"\nTroca de linhas: L{k + 1} <-> L{maior + 1}")

        pivo = M[k, k]

        if abs(pivo) < TOLERANCIA_ZERO:
            print(f"\nErro! Pivô nulo na etapa {k + 1} (posição [{k + 1},{k + 1}]).")
            if pivoteamento:
                print("Mesmo trocando linhas, a coluna inteira é zero -> det(A) = 0.")
                print("O sistema NÃO tem solução única (impossível ou indeterminado).")
            else:
                print("Não dá pra dividir por zero. Sem troca de linhas o método não continua.")
                print("(Tente com pivoteamento. Se ainda falhar, a matriz é singular.)")
            return None

        for i in range(k + 1, n):
            m = M[i, k] / pivo
            M[i, k:] = M[i, k:] - m * M[k, k:]
            M[i, k] = 0.0  

        print(f"\nMatriz após a etapa {k + 1}:")
        print(M)

    if abs(M[n - 1, n - 1]) < TOLERANCIA_ZERO:
        print(f"\nErro! O último pivô (posição [{n},{n}]) é zero -> det(A) = 0.")
        if abs(M[n - 1, n]) < TOLERANCIA_ZERO:
            print("A última linha virou 0 = 0 -> sistema POSSÍVEL E INDETERMINADO (infinitas soluções).")
        else:
            print(f"A última linha virou 0 = {M[n - 1, n]:.4f} -> sistema IMPOSSÍVEL (sem solução).")
        return None

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        soma = 0.0
        for j in range(i + 1, n):
            soma += M[i, j] * x[j]
        x[i] = (M[i, n] - soma) / M[i, i]

    print("\n===== RESULTADO =====")
    for i in range(n):
        print(f"x{i + 1} = {x[i]:.8f}")

    residuo = np.array(A, dtype=float) @ x - np.array(b, dtype=float)
    print(f"\nVerificação: maior |A·x - b| = {np.max(np.abs(residuo)):.2e}")

    return x


def ler_sistema():
    n = int(input("Número de equações/incógnitas (n): "))
    print(f"Digite cada linha com os {n} coeficientes e o termo independente, separados por espaço.")
    print("Exemplo para 2x + y - z = 8  ->  2 1 -1 8")

    A, b = [], []
    for i in range(n):
        valores = [float(v) for v in input(f"Linha {i + 1}: ").split()]
        A.append(valores[:-1])
        b.append(valores[-1])

    resp = input("Usar pivoteamento parcial (troca de linhas)? (s/n) [n]: ").strip().lower()
    return A, b, resp == "s"


if __name__ == "__main__":
    A, b, piv = ler_sistema()
    eliminacao_gauss(A, b, pivoteamento=piv)

