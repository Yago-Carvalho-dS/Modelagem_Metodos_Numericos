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

    derivada = sp.diff(expressao, x)  
    f = sp.lambdify(x, expressao, "math")
    df = sp.lambdify(x, derivada, "math")
    return f, df, expressao, derivada


def newton_raphson(f, df, x0, tolerancia, max_iteracoes):
    x = x0

    print(f"\n{'iter':>4} | {'x':>18} | {'f(x)':>14} | {'f´(x)':>14} | {'x_novo':>18} | {'erro':>12}")
    print("-" * 95)

    for i in range(1, max_iteracoes + 1):
        fx = f(x)
        dfx = df(x)

        if dfx == 0:
            print(f"\nErro! f'(x) = 0 em x = {x}.")
            print("A reta tangente é HORIZONTAL e nunca corta o eixo x -> divisão por zero.")
            print("O método não pode continuar. Tente outro chute inicial.")
            return None

        x_novo = x - fx / dfx
        erro = abs(x_novo - x)
        print(f"{i:>4} | {x:>18.10g} | {fx:>14.6e} | {dfx:>14.6e} | {x_novo:>18.10g} | {erro:>12.4e}")

        if erro < tolerancia:
            print(f"\nConvergiu em {i} iterações.")
            print(f"Raiz aproximada: x = {x_novo:.10f}")
            print(f"Verificação: f(x) = {f(x_novo):.4e}")
            return x_novo

        x = x_novo

    print(f"\nNÃO convergiu em {max_iteracoes} iterações (erro final = {erro:.4e}).")
    print("O método divergiu, entrou em ciclo ou a função não tem raiz real perto do chute.")
    print(f"Último x calculado: {x}")
    return None


if __name__ == "__main__":
    print("Funções aceitas: + - * / ^, sqrt/raiz, exp, e, ln/log, sen/sin, cos, tg/tan, arctg/atan, pi")
    texto = input("f(x) = ")
    x0 = float(input("Chute inicial x0: "))
    tol = input("Tolerância [1e-6]: ").strip()
    tol = float(tol) if tol else 1e-6
    max_it = input("Máximo de iterações [50]: ").strip()
    max_it = int(max_it) if max_it else 50

    try:
        f, df, expressao, derivada = preparar(texto)
    except (sp.SympifyError, SyntaxError, TypeError, ValueError) as erro:
        print(f"Erro! Não consegui entender a função digitada ({erro}).")
        raise SystemExit

    print(f"\nf(x)  = {expressao}")
    print(f"f'(x) = {derivada}")
    try:
        newton_raphson(f, df, x0, tol, max_it)
    except (ValueError, ZeroDivisionError, OverflowError, TypeError) as erro:
        print(f"\nErro matemático durante o cálculo: {erro}")
        print("O método levou x para um ponto onde f(x) ou f'(x) não existe (ou explode).")

