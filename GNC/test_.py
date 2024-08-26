import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from typing import Callable, Tuple, List

"""
Autor: Wilson Weliton Oliveira de Souza
Data: 25/08/2024
Projeto: O projeto visa aplicar uma forma rápida de visualização de mapa de contornos para funções de várias variáveis de forma simples e rápida.
Está em fase de desenvolvimento para funções mais complexas.
"""

def show_instructions() -> None:
    """
    Exibe as instruções sobre como usar o código e fornece exemplos de funções que podem ser inseridas.
    """
    print("Bem-vindo ao Gerador de Mapas de Contorno!")
    print("Este programa permite que você insira uma função matemática de duas variáveis (x, y) e visualize seu gráfico de contorno.")
    print("\nInstruções:")
    print("1. Insira a função desejada usando 'x' e 'y' como variáveis.")
    print("2. Utilize as funções matemáticas do NumPy, como np.exp, np.sin, np.cos, np.sqrt, etc.")
    print("3. Não inclua a parte 'f(x,y) =' na sua entrada. Apenas insira a expressão matemática.")
    print("4. Use '**' para exponenciação em vez de '^'.")
    print("\nExemplos de funções que você pode inserir:")
    print("  - 'np.sqrt(x) + y'")
    print("  - 'x**2 + y**2'")
    print("  - 'np.sin(x) * np.cos(y)'")
    print("  - 'np.exp(-x**2 - y**2)'")
    print("  - 'x * np.log(y + 1)'")
    print("\nDigite a função desejada no formato indicado e veja o resultado!")

def parse_function(func_str: str) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    """
    Converte uma string de função matemática em uma função Python segura.

    Args:
        func_str (str): String da função que o usuário insere.

    Returns:
        Callable[[np.ndarray, np.ndarray], np.ndarray]: Função que calcula o valor baseado na entrada x e y.
    """
    x, y = sp.symbols('x y')
    expr = sp.sympify(func_str)
    func_lambdified = sp.lambdify((x, y), expr, modules=['numpy'])
    return func_lambdified

def plot_contour(f: Callable[[np.ndarray, np.ndarray], np.ndarray],
                 x_range: Tuple[float, float],
                 y_range: Tuple[float, float],
                 levels: List[float] = None,
                 title: str = 'Mapa de Contorno para a Função') -> None:
    """
    Plota um gráfico de contorno para a função dada f(x, y).

    Args:
        f (Callable): Função que aceita dois argumentos (x, y) e retorna um valor.
        x_range (Tuple): Intervalo para o eixo x (min, max).
        y_range (Tuple): Intervalo para o eixo y (min, max).
        levels (List, optional): Níveis das curvas de contorno a serem plotadas. Se None, será utilizado um conjunto padrão.
        title (str, optional): Título do gráfico.
    """
    x = np.linspace(x_range[0], x_range[1], 400)
    y = np.linspace(y_range[0], y_range[1], 400)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    plt.figure(figsize=(8, 8))
    if levels is None:
        levels = np.linspace(Z.min(), Z.max(), 10)  
    contours = plt.contour(X, Y, Z, levels=levels)
    plt.clabel(contours, inline=True, fontsize=8)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()

show_instructions()

# Solicita a função ao usuário
func_str = input("Digite a função que deseja calcular (use x e y como variáveis): ")
user_function = parse_function(func_str)

# Gera o gráfico
plot_contour(user_function, (0, 10), (-5, 5), levels=[1, 2, 3, 4])
