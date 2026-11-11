import sympy as sp


NOMES = {"e": sp.E, "ln": sp.log, "sen": sp.sin, "tg": sp.tan,
         "arctg": sp.atan, "raiz": sp.sqrt}


def preparar(formula):
    formula = formula.replace("^", "**")
    expressao = sp.sympify(formula, locals=NOMES)
    x = sp.symbols("x")

    outras = expressao.free_symbols - {x}
    if outras:
        raise ValueError(f"a função só pode ter a variável x (encontrei: {outras})")

    return sp.lambdify(x, expressao, "math"), expressao


def falsa_posicao(f, a, b, tolerancia, max_iteracoes):
    fa = f(a)
    fb = f(b)

    print(f"\nf({a}) = {fa:.6f}    f({b}) = {fb:.6f}")

    if fa == 0:
        print(f"O próprio a = {a} já é raiz.")
        return a
    if fb == 0:
        print(f"O próprio b = {b} já é raiz.")
        return b

    if fa * fb > 0:
        print("Erro! f(a) e f(b) têm o MESMO SINAL.")
        print("Pelo Teorema de Bolzano não há garantia de raiz em [a, b]:")
        print("pode não ter raiz nenhuma, ou ter um número PAR de raízes (ex: raiz dupla).")
        print("O método não pode começar.")
        return None

    print(f"\n{'iter':>4} | {'a':>14} | {'b':>14} | {'x':>14} | {'f(x)':>14} | {'erro':>12}")
    print("-" * 87)

    x_anterior = None
    x = a
    for i in range(1, max_iteracoes + 1):
        x = (a * fb - b * fa) / (fb - fa)
        fx = f(x)

        erro = abs(x - x_anterior) if x_anterior is not None else float("inf")
        print(f"{i:>4} | {a:>14.8f} | {b:>14.8f} | {x:>14.8f} | {fx:>14.6e} | {erro:>12.4e}")

        if fx == 0 or erro < tolerancia:
            print(f"\nConvergiu em {i} iterações.")
            print(f"Raiz aproximada: x = {x:.10f}")
            print(f"Verificação: f(x) = {fx:.4e}")
            return x

        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx

        x_anterior = x

    print(f"\nNÃO convergiu em {max_iteracoes} iterações (erro final = {erro:.4e}).")
    print(f"Última aproximação: x = {x:.10f}, f(x) = {f(x):.4e}")
    return None


if __name__ == "__main__":
    print("Funções aceitas: + - * / ^, sqrt/raiz, exp, e, ln/log, sen/sin, cos, tg/tan, arctg/atan, pi")
    texto = input("f(x) = ")
    a = float(input("a (início do intervalo): "))
    b = float(input("b (fim do intervalo): "))
    tol = input("Tolerância [1e-6]: ").strip()
    tol = float(tol) if tol else 1e-6
    max_it = input("Máximo de iterações [50]: ").strip()
    max_it = int(max_it) if max_it else 50

    try:
        f, expressao = preparar(texto)
    except (sp.SympifyError, SyntaxError, TypeError, ValueError) as erro:
        print(f"Erro! Não consegui entender a função digitada ({erro}).")
        raise SystemExit

    print(f"\nf(x) = {expressao}")
    try:
        falsa_posicao(f, a, b, tol, max_it)
    except (ValueError, ZeroDivisionError, OverflowError, TypeError) as erro:
        print(f"\nErro matemático durante o cálculo: {erro}")
        print("A função não está definida (ou explode) em algum ponto que o método precisou avaliar.")

