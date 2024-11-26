import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time

# Función para imprimir el Sudoku
def imprimir_sudoku(sudoku):
    for fila in sudoku:
        print(" ".join(str(celda) if celda != 0 else '.' for celda in fila))
    print()

# Verificar si es seguro colocar un número en una celda
def es_seguro(sudoku, fila, col, num):
    # Revisar la fila
    if num in sudoku[fila]:
        return False
    # Revisar la columna
    if num in [sudoku[f][col] for f in range(9)]:
        return False
    # Revisar la subcuadrícula de 3x3
    inicio_fila, inicio_col = 3 * (fila // 3), 3 * (col // 3)
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if sudoku[i][j] == num:
                return False
    return True

# Resolver Sudoku con Backtracking visual
def resolver_sudoku_backtracking(sudoku, resaltados, ax, fig):
    # Función auxiliar de backtracking
    def backtrack(fila, col):
        if fila == 9:  # Si hemos recorrido todas las filas, el Sudoku está resuelto
            return True
        if col == 9:  # Si llegamos al final de una fila, avanzamos a la siguiente
            return backtrack(fila + 1, 0)
        if sudoku[fila][col] != 0:  # Si la celda ya tiene un número, pasamos a la siguiente
            return backtrack(fila, col + 1)
        
        # Intentamos con números del 1 al 9
        for num in range(1, 10):
            if es_seguro(sudoku, fila, col, num):
                sudoku[fila][col] = num  # Colocamos el número
                resaltados[fila][col] = True  # Marcamos la celda como resaltada
                actualizar_tablero(sudoku, ax, fig, resaltados)
                plt.pause(0.2)  # Pausa para hacer visible el cambio
                if backtrack(fila, col + 1):  # Intentamos resolver el siguiente
                    return True
                # Si no funcionó, retrocedemos (eliminamos el número)
                sudoku[fila][col] = 0
                resaltados[fila][col] = False
                actualizar_tablero(sudoku, ax, fig, resaltados)
                plt.pause(0.2)  # Pausa para mostrar el retroceso
        return False  # Si no encontramos una solución, retrocedemos

    # Iniciamos el backtracking desde la primera celda
    return backtrack(0, 0)

# Actualizar el tablero en pantalla
def actualizar_tablero(sudoku, ax, fig, resaltados):
    ax.clear()

    # Fondo azul claro para el Sudoku
    ax.set_facecolor('#a3d1ff')

    # Dibujar las celdas del tablero
    for i in range(9):
        for j in range(9):
            ax.add_patch(plt.Rectangle((j, 8-i), 1, 1, color='#a3d1ff', ec='none'))

    # Dibujar las líneas del tablero
    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5  # Líneas más gruesas para las subcuadrículas
        ax.axhline(i, color="#333333", lw=lw)  # Las líneas horizontales
        ax.axvline(i, color="#333333", lw=lw)  # Las líneas verticales

    # Rellenar los números
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

# Función que se activa con el botón "Resolver Sudoku"
def on_resolver_click(event):
    resaltados = np.zeros((9, 9), dtype=bool)  # Mantener los números resaltados
    print("Sudoku inicial:")
    imprimir_sudoku(sudoku_inicial)

    inicio = time.time()
    resolver_sudoku_backtracking(sudoku_inicial, resaltados, ax, fig)
    fin = time.time()

    print("Sudoku resuelto:")
    imprimir_sudoku(sudoku_inicial)
    print(f"Tiempo de ejecución: {fin - inicio:.2f} segundos")

# Tablero inicial del Sudoku
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

# Crear la figura y el tablero inicial
fig, ax = plt.subplots(figsize=(6, 6))

# Cambiar el color de fondo de la interfaz
fig.patch.set_facecolor('#5DAEFE')

# Añadir el texto con tu nombre y número de matrícula (ajustado)
fig.text(0.5, 1.05, 'JONATAN DAVID MACDONAL RODAS - 230300778', ha='center', va='center', fontsize=10, color='black')

# Título (mover hacia abajo para no solaparse con el texto)
fig.suptitle("SUDOKU - BACKTRACKING VISUAL", fontsize=14, fontweight='bold', y=0.93)

resaltados = np.zeros((9, 9), dtype=bool)
actualizar_tablero(sudoku_inicial, ax, fig, resaltados)

# Crear el botón "Resolver Sudoku"
ax_button = plt.axes([0.35, 0.01, 0.3, 0.075])  # Botón más grande: ajustar ancho y posición
btn_resolver = Button(ax_button, 'Resolver Sudoku')

# Ajustar estilo del botón
btn_resolver.label.set_fontsize(12)  # Reducir tamaño de fuente
btn_resolver.ax.set_facecolor('#a3d1ff')  # Fondo azul claro
btn_resolver.label.set_color('black')  # Cambiar color de texto a negro
btn_resolver.ax.patch.set_edgecolor('black')
btn_resolver.ax.patch.set_linewidth(2)

btn_resolver.on_clicked(on_resolver_click)

# Mostrar la interfaz
plt.show()
