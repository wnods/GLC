import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from typing import Callable, Tuple, List


def show_instructions() -> None:
    print("Bem-vindo ao Gerador de Mapas de Contornos/Curva de Nível!")
    print("Este programa permite que você insira uma função matemática de duas variáveis (x, y) e visualize seu gráfico de contorno.")
    print("\nInstruções:")
    print("1) Insira a função desejada usando 'x' e 'y' como variáveis.")
    print("2) Utilize as funções matemáticas do NumPy, como np.exp, np.sin, np.cos, np.sqrt, etc.")
    print("3) Não inclua a parte 'f(x,y) =' na sua entrada. Apenas insira a expressão matemática.")
    print("4) Use '**' para exponenciação em vez de '^'.")
    print("\nExemplos de funções que você pode inserir:")
    print("  - 'sqrt(x) + y'")
    print("  - 'x**2 + y**2'")
    print("  - 'sin(x) * cos(y)'")
    print("  - 'exp(-x**2 - y**2)'")
    print("  - 'x * log(y + 1)'")
    print("\nDigite a função desejada no formato indicado e veja o resultado!")

def parse_function(func_str: str) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    x, y = sp.symbols('x y')

    numpy_to_sympy = {
        'np.sin': 'sp.sin',
        'np.cos': 'sp.cos',
        'np.tan': 'sp.tan',
        'np.exp': 'sp.exp',
        'np.log': 'sp.log',
        'np.sqrt': 'sp.sqrt',
        'np.abs': 'sp.Abs'
    }

    for np_func, sp_func in numpy_to_sympy.items():
        func_str = func_str.replace(np_func, sp_func)

    expr = sp.sympify(func_str)
    func_lambdified = sp.lambdify((x, y), expr, modules=['numpy'])
    return func_lambdified

def plot_contour(f: Callable[[np.ndarray, np.ndarray], np.ndarray],
                 x_range: Tuple[float, float],
                 y_range: Tuple[float, float],
                 levels: List[float] = None,
                 title: str = 'Gráfico das Curvas de Nível para a Função',
                 save_as_png: bool = False,
                 filename: str = 'grafico.png',
                 color_map: str = 'viridis',
                 line_style: str = '-') -> None:
    x = np.linspace(x_range[0], x_range[1], 400)
    y = np.linspace(y_range[0], y_range[1], 400)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    plt.figure(figsize=(8, 8))
    if levels is None:
        levels = np.linspace(Z.min(), Z.max(), 10)
    
    contours = plt.contour(X, Y, Z, levels=levels, cmap=color_map, linestyles=line_style)
    plt.clabel(contours, inline=True, fontsize=8)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    if save_as_png:
        if not filename:
            filename = 'GLC.png'  
        plt.savefig(filename, format='png')
        print(f"Gráfico salvo como {filename}")

    plt.show(block=True)  

show_instructions()

func_str = input("Digite a função que deseja calcular (use x e y como variáveis): ")
user_function = parse_function(func_str)

save_option = input("Deseja salvar o Gráfico das Curvas de Nível? (Y/N): ").strip().lower()
save_as_png = save_option == 'y'  

filename = "GLC.png"  
if save_as_png:
    custom_filename = input("Digite o nome do arquivo (ex: meu_grafico.png): ").strip()
    if custom_filename:
        filename = custom_filename

     
                               """
                               
                     Customização do gráfico
                               
                               """
                               
color_map = input("Escolha um mapa de cores (ex: 'viridis', 'plasma', 'inferno', 'cividis'): ").strip()
if not color_map:
    color_map = 'viridis'  

line_style = input("Escolha um estilo de linha (ex: '-', '--', '-.', ':'): ").strip()
if not line_style:
    line_style = '-' 

plot_contour(user_function, (0, 10), (-5, 5), levels=[0.1, 0.2, 0.4, 0.6, 0.8, 1.0], 
             save_as_png=save_as_png, filename=filename, color_map=color_map, line_style=line_style)
