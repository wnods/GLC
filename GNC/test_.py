import numpy as np
import matplotlib.pyplot as plt

"""
Autor: Wilson Weliton Oliveira de Souza
Projeto: O projeto visa aplicar uma forma rápida de visualização de mapa de contornos para funções de várias variáveis de forma simples e rápida. Está em fase de desenvolvimento para funções mais complexas.

"""

def show_instructions():
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

def plot_contour(f, x_range, y_range, levels=None):
    """
    Plota um gráfico de contorno para a função dada f(x, y).

    Args:
        f (function): Função que aceita dois argumentos (x, y) e retorna um valor.
        x_range (tuple): Intervalo para o eixo x (min, max).
        y_range (tuple): Intervalo para o eixo y (min, max).
        levels (list, optional): Níveis das curvas de contorno a serem plotadas. Se None, será utilizado um conjunto padrão.
    """
    # Definir o intervalo para x e y
    x = np.linspace(x_range[0], x_range[1], 400)
    y = np.linspace(y_range[0], y_range[1], 400)
    X, Y = np.meshgrid(x, y)

    # Calcular f(x, y)
    Z = f(X, Y)

    # Plotar as curvas de nível
    plt.figure(figsize=(8, 8))
    if levels is None:
        levels = np.linspace(Z.min(), Z.max(), 10)  # Níveis padrão
    contours = plt.contour(X, Y, Z, levels=levels)

    # Adicionar labels e título
    plt.clabel(contours, inline=True, fontsize=8)
    plt.title(f'Mapa de Contorno para a Função')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    plt.show()

# Mostrar instruções
show_instructions()

# Solicitar a função do usuário
func_str = input("Digite a função que deseja calcular (use x e y como variáveis, por exemplo, 'y * np.exp(x)'): ")

# Criar a função dinamicamente usando eval
def user_function(x, y):
    return eval(func_str)

# Usar a função plot_contour
plot_contour(user_function, (0, 10), (-5, 5), levels=[1, 2, 3, 4])

