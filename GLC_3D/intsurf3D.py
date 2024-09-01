import numpy as np
import sympy as sp
from sympy.core.sympify import SympifyError
from typing import Callable, Tuple, List, Dict
import plotly.graph_objs as go
import plotly.figure_factory as ff


"""
===========================================================================================
===========================================================================================
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                                                        %%%
Projeto desenvolvido com a funcionabilidade de interação ao usuário e simplicidade para %%% 
visualização de curvas de nível a partir de uma dada função.                            %%%
                                                                                        %%%
Autor: Wilson Weliton Oliveira de Souza                                                 %%%
Data: 25/08/2024                                                                        %%%     
                                                                                        %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
===========================================================================================
===========================================================================================
"""


def show_instructions() -> None:
    """
    Exibe as instruções sobre como usar o código e fornece exemplos de funções que podem ser inseridas.
    
    """
    print("Bem-vindo ao Gerador de Gráfico de Curvas de Nível e Superfícies!")
    print("Este programa permite que você insira uma função matemática de múltiplas variáveis (x, y, z, etc.) e visualize seu gráfico de contorno e/ou superfície.")
    print("\nInstruções:")
    print("1) Insira a função desejada usando 'x', 'y', 'z', etc. como variáveis.")
    print("2) Utilize as funções matemáticas do SymPy, como exp, sin, cos, sqrt, etc.")
    print("3) Fixe valores para variáveis adicionais que não serão plotadas (ex.: z=1).")
    print("4) Não inclua a parte 'f(x,y,...) =' na sua entrada. Apenas insira a expressão matemática.")
    print("5) Use '**' para exponenciação em vez de '^'.")
    print("\nExemplos de funções que você pode inserir:")
    print("  - 'sqrt(x) + y + z'")
    print("  - 'x**2 + y**2 + z**2'")
    print("  - 'sin(x) * cos(y) * z'")
    print("  - 'exp(-x**2 - y**2 + z)'")
    print("\nDigite a função desejada no formato indicado e veja o resultado!")

def parse_function(func_str: str, fixed_vars: Dict[str, float] = None) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    """
    Converte uma string de função matemática em uma função Python segura, permitindo a fixação de variáveis.

                               !! RETIREI EVAL POR SEGURANÇA !!

    Args:
        func_str (str): String da função que o usuário insere.
        fixed_vars (Dict[str, float], optional): Dicionário de variáveis a serem fixadas com seus respectivos valores.

    Returns:
        Callable[[np.ndarray, np.ndarray], np.ndarray]: Função que calcula o valor baseado na entrada x e y, considerando variáveis fixas.
    """
    try:
        variables = sp.symbols('x y ' + ' '.join(fixed_vars.keys() if fixed_vars else []))
        expr = sp.sympify(func_str)
        if fixed_vars:
            expr = expr.subs(fixed_vars)
        func_lambdified = sp.lambdify(('x', 'y'), expr, modules=['numpy'])
        return func_lambdified
    except (SympifyError, TypeError) as e:
        raise ValueError(f"Erro ao interpretar a função: {e}")

def validate_function(func_str: str) -> bool:
    """
    Valida se a string de função fornecida é válida e pode ser convertida em uma função.

    Args:
        func_str (str): String da função que o usuário insere.

    Returns:
        bool: True se a função for válida, False caso contrário.
    """
    try:
        sp.sympify(func_str)
        return True
    except SympifyError:
        return False

def plot_interactive_surface_and_contour(f: Callable[[np.ndarray, np.ndarray], np.ndarray],
                                         x_range: Tuple[float, float],
                                         y_range: Tuple[float, float],
                                         title: str = 'Superfície e Curvas de Nível da Função') -> None:
    """
    Plota tanto a superfície 3D quanto o gráfico de contorno e a curva de nível para a função dada f(x, y).

    Args:
        f (Callable): Função que aceita dois argumentos (x, y) e retorna um valor.
        x_range (Tuple): Intervalo para o eixo x (min, max).
        y_range (Tuple): Intervalo para o eixo y (min, max).
        title (str, optional): Título do gráfico.
    """
    x = np.linspace(x_range[0], x_range[1], 400)
    y = np.linspace(y_range[0], y_range[1], 400)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)


    surface = go.Surface(z=Z, x=X, y=Y, colorscale='inferno')


    contours = go.Contour(z=Z, x=x, y=y, colorscale='inferno')


    layout = go.Layout(
        title=title,
        scene=dict(
            xaxis=dict(title='x'),
            yaxis=dict(title='y'),
            zaxis=dict(title='z')
        ),
        xaxis=dict(title='x'),
        yaxis=dict(title='y')
    )

    
    fig = go.Figure(data=[surface, contours], layout=layout)

    
    fig.show()

show_instructions()


func_str = input("Digite a função que deseja calcular (use x e y como variáveis): ")

if validate_function(func_str):
    
    fixed_vars = {}
    while True:
        var_input = input("Digite a variável e valor para fixar (ex.: z=1), ou pressione ENTER para continuar: ")
        if not var_input:
            break
        var, value = var_input.split('=')
        fixed_vars[var.strip()] = float(value.strip())

    user_function = parse_function(func_str, fixed_vars)

    
    plot_interactive_surface_and_contour(user_function, (0, 10), (-5, 5))
else:
    print("Erro: A função inserida é inválida. Por favor, insira uma função válida.")

