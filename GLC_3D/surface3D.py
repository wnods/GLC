import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy.core.sympify import SympifyError
from typing import Callable, Tuple, List, Dict
from mpl_toolkits.mplot3d import Axes3D

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
    print("Bem-vindo ao Gerador de Mapas de Contorno e Superfícies!")
    print("Este programa permite que você insira uma função matemática de múltiplas variáveis (x, y, z, etc.) e visualize seu gráfico de contorno e/ou superfície.")
    print("\nInstruções:")
    print("1) Insira a função desejada usando 'x', 'y', 'z', etc. como variáveis.")
    print("2) Utilize as funções matemáticas do SymPy, como sp.exp, sp.sin, sp.cos, sp.sqrt, etc.")
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
    Valida se a string de função fornecida é válida e pode ser convertida em uma função matemática.

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

def plot_surface_and_contour(f: Callable[[np.ndarray, np.ndarray], np.ndarray],
                             x_range: Tuple[float, float],
                             y_range: Tuple[float, float],
                             levels: List[float] = None,
                             title: str = 'Gráfico da Superfície',
                             title2: str = 'Gráfico das Curvas de Nível da Função',
                             save_path: str = None) -> None:
    """
    Plota tanto a superfície 3D quanto o gráfico de contorno para a função dada f(x, y).

    Args:
        f (Callable): Função que aceita dois argumentos (x, y) e retorna um valor.
        x_range (Tuple): Intervalo para o eixo x (min, max).
        y_range (Tuple): Intervalo para o eixo y (min, max).
        levels (List, optional): Níveis das curvas de contorno a serem plotadas. Se None, será utilizado um conjunto padrão.
        title (str, optional): Título do gráfico.
        save_path (str, optional): Caminho para salvar a imagem do gráfico. Se None, a imagem não será salva.
    """
    x = np.linspace(x_range[0], x_range[1], 400)
    y = np.linspace(y_range[0], y_range[1], 400)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig = plt.figure(figsize=(14, 7))

    
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax1.set_title(f'3D: {title}')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')

    
    ax2 = fig.add_subplot(122)
    if levels is None:
        levels = np.linspace(Z.min(), Z.max(), 10)
    contours = ax2.contour(X, Y, Z, levels=levels, cmap='viridis')
    ax2.clabel(contours, inline=True, fontsize=8)
    ax2.set_title(f'2D: {title2}')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.grid(True)
    ax2.axhline(0, color='black', linewidth=0.5)
    ax2.axvline(0, color='black', linewidth=0.5)

    
    if save_path:
        plt.savefig(save_path)
        print(f"Gráfico salvo em: {save_path}")

    plt.show()

show_instructions()


func_str = input("Digite a função que deseja calcular (use x e y como variáveis): ")

if validate_function(func_str):
    
    fixed_vars = {}
    while True:
        var_input = input("Digite a variável e valor para fixar (ex.: z=1), ou pressione Enter para continuar: ")
        if not var_input:
            break
        var, value = var_input.split('=')
        fixed_vars[var.strip()] = float(value.strip())

    user_function = parse_function(func_str, fixed_vars)
    
   
    save_path = input("Digite o caminho para salvar o gráfico (ex.: 'meu_grafico.png'), ou pressione Enter para não salvar: ")
    if save_path == '':
        save_path = None
    
    
    plot_surface_and_contour(user_function, (0, 10), (-5, 5), levels=[0.1, 0.4, 0.7, 1, 1.2, 1.4, 1.8], save_path=save_path)
else:
    print("Erro: A função inserida é inválida. Por favor, insira uma função válida.")
