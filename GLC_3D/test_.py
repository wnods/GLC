import numpy as np
import sympy as sp
from sympy.core.sympify import SympifyError
from typing import Callable, Tuple, List, Dict
import plotly.graph_objs as go


def show_instructions() -> None:
    print("Bem-vindo ao Gerador de Gráfico de Curvas de Nível e Superfícies!")
    print("Instruções:")
    print("1) Insira a função desejada usando 'x', 'y', 'z', etc. como variáveis.")
    print("2) Utilize as funções matemáticas do SymPy, como exp, sin, cos, sqrt, etc.")
    print("3) Fixe valores para variáveis adicionais que não serão plotadas (ex.: z=1).")
    print("4) Não inclua a parte 'f(x,y,...) =' na sua entrada. Apenas insira a expressão matemática.")
    print("5) Use '**' para exponenciação em vez de '^'.")
    print("Exemplos:")
    print("  - 'sqrt(x) + y + z'")
    print("  - 'x**2 + y**2 + z**2'")
    print("  - 'sin(x) * cos(y) * z'")
    print("  - 'exp(-x**2 - y**2 + z)'")

def parse_function(func_str: str, fixed_vars: Dict[str, float] = None) -> Tuple[Callable[[np.ndarray, np.ndarray], np.ndarray], sp.Expr, sp.Symbol, sp.Symbol]:
    try:
        x, y = sp.symbols('x y')
        variables = sp.symbols('x y ' + ' '.join(fixed_vars.keys() if fixed_vars else []))
        expr = sp.sympify(func_str)
        if fixed_vars:
            expr = expr.subs(fixed_vars)
        func_lambdified = sp.lambdify((x, y), expr, modules=['numpy'])
        return func_lambdified, expr, x, y
    except (SympifyError, TypeError) as e:
        raise ValueError(f"Erro ao interpretar a função: {e}")

def validate_function(func_str: str) -> bool:
    try:
        sp.sympify(func_str)
        return True
    except SympifyError:
        return False

def calculate_derivatives_and_extrema(expr: sp.Expr, x: sp.Symbol, y: sp.Symbol):

    fx = sp.diff(expr, x)
    fy = sp.diff(expr, y)
    
    critical_points = sp.solve([fx, fy], (x, y))
    
    second_derivative_xx = sp.diff(fx, x)
    second_derivative_yy = sp.diff(fy, y)
    second_derivative_xy = sp.diff(fx, y)
    
    extrema = []
    for point in critical_points:
        H = second_derivative_xx.subs({x: point[0], y: point[1]}) * second_derivative_yy.subs({x: point[0], y: point[1]}) - second_derivative_xy.subs({x: point[0], y: point[1]})**2
        if H > 0:
            if second_derivative_xx.subs({x: point[0], y: point[1]}) > 0:
                extrema.append(('Minimo', point))
            else:
                extrema.append(('Maximo', point))
        elif H < 0:
            extrema.append(('Sela', point))
        else:
            extrema.append(('Indeterminado', point))
    
    return fx, fy, extrema

def calculate_limits(expr: sp.Expr, x: sp.Symbol, y: sp.Symbol):
    limit_x_inf = sp.limit(expr, x, sp.oo)
    limit_y_inf = sp.limit(expr, y, sp.oo)
    limit_x_neg_inf = sp.limit(expr, x, -sp.oo)
    limit_y_neg_inf = sp.limit(expr, y, -sp.oo)
    return limit_x_inf, limit_y_inf, limit_x_neg_inf, limit_y_neg_inf

def plot_interactive_surface_and_contour(f: Callable[[np.ndarray, np.ndarray], np.ndarray],
                                         x_range: Tuple[float, float],
                                         y_range: Tuple[float, float],
                                         title: str = 'Superfície e Mapa de Contorno Interativos',
                                         extrema: List[Tuple[str, Tuple[float, float]]] = None) -> None:
    x = np.linspace(x_range[0], x_range[1], 400)
    y = np.linspace(y_range[0], y_range[1], 400)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    surface = go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')
    contours = go.Contour(z=Z, x=x, y=y, colorscale='Viridis')

    markers = []
    if extrema:
        for etype, point in extrema:
            z_value = f(float(point[0]), float(point[1]))
            markers.append(go.Scatter3d(x=[point[0]], y=[point[1]], z=[z_value],
                                        mode='markers',
                                        marker=dict(size=5, color='red'),
                                        name=f'{etype} ({point[0]:.2f}, {point[1]:.2f}, {z_value:.2f})'))

    layout = go.Layout(
        title=title,
        scene=dict(xaxis=dict(title='x'), yaxis=dict(title='y'), zaxis=dict(title='z')),
        xaxis=dict(title='x'),
        yaxis=dict(title='y')
    )

    fig = go.Figure(data=[surface, contours] + markers, layout=layout)
    fig.show()

show_instructions()

func_str = input("Digite a função que deseja calcular (use x e y como variáveis): ")

if validate_function(func_str):
    fixed_vars = {}
    while True:
        var_input = input("Digite a variável e valor para fixar (ex.: z=1), ou pressione Enter para continuar: ")
        if not var_input:
            break
        try:
            var, value = var_input.split('=')
            fixed_vars[var.strip()] = float(value.strip())
        except ValueError:
            print("Erro: Entrada inválida. Use o formato 'variável=valor'.")

    user_function, expr, x, y = parse_function(func_str, fixed_vars)
    
    fx, fy, extrema = calculate_derivatives_and_extrema(expr, x, y)
    limit_x_inf, limit_y_inf, limit_x_neg_inf, limit_y_neg_inf = calculate_limits(expr, x, y)
    
    print(f"Equação: f(x, y) = {expr}")
    print(f"Derivada parcial em relação a x: ∂f/∂x = {fx}")
    print(f"Derivada parcial em relação a y: ∂f/∂y = {fy}")
    print(f"Pontos críticos e tipos: {extrema}")
    print(f"Limite quando x → ∞: {limit_x_inf}")
    print(f"Limite quando y → ∞: {limit_y_inf}")
    print(f"Limite quando x → -∞: {limit_x_neg_inf}")
    print(f"Limite quando y → -∞: {limit_y_neg_inf}")
    
    plot_interactive_surface_and_contour(user_function, (0, 10), (-5, 5), extrema=extrema)
else:
    print("Erro: A função inserida é inválida. Por favor, insira uma função válida.")

