# ROAD TO BUSCAMINAS (Versión Choco-Bomb)
# - temporizador
# - grid nxm.
# - Número de minas.
# - Colocar minas aleatoriamente en el grid.
# - El número de las celdas sin minas debe ser igual al número de minas que tiene alrededor
# - Si el número de minas es cero no pintar número
# tkinter
# class
from tkinter import Tk, Button, Label
from tkinter import ttk

import settings
from cell import Cell

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    # Options (Size, num_mine (standard and custom), results)
    frm_options = ttk.Frame(root, padding=10)
    frm_options.grid(row=0, column=0)
    l_option = Label(frm_options, text="Options").grid(row=0, column=0)

    # Header (Reset, count_mine, temp, pause)
    frm_header = ttk.Frame(root, padding=10, name='frm_header')
    frm_header.grid(row=1, column=0)
    l_mines_left = Label(frm_header, name='l_mines_left', text=settings.NUM_MINES, background='black', width=10,
                         foreground='green', font=('', 12, 'bold')).grid(row=0, column=0, ipady=2)
    btn_reset = Button(frm_header, text="Reset", font=('', 10, 'bold'), command=Cell.reset,
                       bd=0).grid(row=0, column=1, padx=50)
    l_counter = Label(frm_header, name='l_counter', text="0", background='black', width=10,
                      foreground='green', font=('', 12, 'bold')).grid(row=0, column=2, ipady=2)

    # Game (cells)
    frm_game = ttk.Frame(root, padding=10, name='frm_game')
    frm_game.grid(row=2, column=0)

    # Create cells
    size = settings.SIZE
    for x in range(0, size):
        for y in range(0, size):
            cell = Cell(root, frm_game, x, y)

    # Set mines in cells randomly
    Cell.set_mines()

    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
