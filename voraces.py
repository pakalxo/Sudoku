# JONATAN DAVID MACDONAL RODAS - 230300778
# ALGORITMOS VORACES

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time

# Función para imprimir el Sudoku
def imprimir_sudoku(sudoku):
    for fila in sudoku:
        print(" ".join(str(celda) if celda != 0 else '.' for celda in fila))
    print()

# Función para encontrar las opciones válidas
def encontrar_opciones(sudoku, fila, col):
    opciones = set(range(1, 10))
    opciones -= set(sudoku[fila])  # Remover números en la fila
    opciones -= set(sudoku[f][col] for f in range(9))  # Remover números en la columna

    # Remover números en la subcuadrícula 3x3
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            opciones.discard(sudoku[i][j])
    return list(opciones)

# Resolver Sudoku con algoritmo voraz
def resolver_sudoku_voraz(sudoku, ax, fig, resaltados):
    while True:
        progreso = False
        min_opciones = 10
        mejor_celda = None

        # Buscar la celda con menos opciones válidas
        for fila in range(9):
            for col in range(9):
                if sudoku[fila][col] == 0:
                    opciones = encontrar_opciones(sudoku, fila, col)
                    if len(opciones) < min_opciones:
                        min_opciones = len(opciones)
                        mejor_celda = (fila, col, opciones)

        if mejor_celda:
            fila, col, opciones = mejor_celda
            if opciones:  # Si hay opciones válidas
                time.sleep(1)  # Retraso para dar la sensación de análisis

                # Tomar la primera opción disponible
                sudoku[fila][col] = opciones[0]
                resaltados[fila][col] = True
                progreso = True
                actualizar_tablero(sudoku, ax, fig, resaltados)
                time.sleep(0.5)  # Pausa para observar el progreso
            else:
                print("No hay solución posible con el enfoque voraz.")
                return False
        else:
            break

        if not progreso:
            break

    # Verificar si se resolvió
    return np.all(sudoku != 0)

# Actualizar tablero
def actualizar_tablero(sudoku, ax, fig, resaltados):
    ax.clear()
    ax.set_facecolor('#a3d1ff')

    # Dibujar las celdas
    for i in range(9):
        for j in range(9):
            ax.add_patch(plt.Rectangle((j, 8 - i), 1, 1, color='#a3d1ff', ec='none'))

    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5
        ax.axhline(i, color="#333333", lw=lw)
        ax.axvline(i, color="#333333", lw=lw)

    # Dibujar números
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                color = "blue" if resaltados[i][j] else "black"
                ax.text(j + 0.5, 8 - i + 0.5, str(sudoku[i][j]),
                        ha="center", va="center", fontsize=16, color=color)

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.axis("off")
    fig.canvas.draw()
    plt.pause(0.1)

# Botón para resolver el Sudoku
def on_resolver_click(event):
    resaltados = np.zeros((9, 9), dtype=bool)
    print("Sudoku inicial:")
    imprimir_sudoku(sudoku_inicial)

    inicio = time.time()
    solucion = resolver_sudoku_voraz(sudoku_inicial, ax, fig, resaltados)
    fin = time.time()

    if solucion:
        print("Sudoku resuelto:")
        imprimir_sudoku(sudoku_inicial)
    else:
        print("El algoritmo voraz no pudo resolver el Sudoku.")
    print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")

# Tablero inicial
sudoku_inicial = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Interfaz gráfica
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('#5DAEFE')
fig.suptitle("Sudoku - Algoritmo Voraz", fontsize=14, fontweight='bold')

actualizar_tablero(sudoku_inicial, ax, fig, np.zeros((9, 9), dtype=bool))

ax_button = plt.axes([0.35, 0.01, 0.3, 0.075])
btn_resolver = Button(ax_button, 'Resolver Sudoku')
btn_resolver.on_clicked(on_resolver_click)

plt.show()
