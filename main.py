# ROAD TO BUSCAMINAS (Versión Choco-Bomb)
# - temporizador
# - grid nxm.
# - Número de minas.
# - Colocar minas aleatoriamente en el grid.
# - El número de las celdas sin minas debe ser igual al número de minas que tiene alrededor
# - Si el número de minas es cero no pintar número
# tkinter
# class
from tkinter import Tk, Button, Label, PhotoImage
from tkinter import ttk

from PIL import Image, ImageTk

import settings
from cell import Cell

BEGINNER = 'Principiante'
MEDIUM = 'Intermedio'
EXPERT = 'Experto'


def create_cells(size_x, size_y):
    Cell.all = []
    for x in range(0, size_x):
        for y in range(0, size_y):
            Cell(root, images, frm_game, x, y)
    Cell.reset()


def selection_changed(event):
    option = event.widget.get()
    if option == MEDIUM:
        settings.size_x = 16
        settings.size_y = 16
        settings.num_mines = 40
    elif option == EXPERT:
        settings.size_x = 16
        settings.size_y = 32
        settings.num_mines = 99
    else:
        settings.size_x = 8
        settings.size_y = 8
        settings.num_mines = 10
    for widget in frm_game.winfo_children():
        widget.destroy()
    create_cells(settings.size_x, settings.size_y)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    # Options (Size, num_mine (standard and custom), results)
    frm_options = ttk.Frame(root, padding=10)
    frm_options.grid(row=0, column=0)
    cb_option = ttk.Combobox(frm_options, state='readonly', values=[BEGINNER, MEDIUM, EXPERT])
    cb_option.grid(row=0, column=0)
    cb_option.bind("<<ComboboxSelected>>", selection_changed)

    # Header (Reset, count_mine, temp, pause)
    frm_header = ttk.Frame(root, padding=10, name='frm_header')
    frm_header.grid(row=1, column=0)
    l_mines_left = Label(frm_header, name='l_mines_left', text=settings.num_mines, background='black', width=10,
                         foreground='green', font=('', 12, 'bold')).grid(row=0, column=0, ipady=2)
    btn_reset = Button(frm_header, text="Reset", font=('', 10, 'bold'), command=Cell.reset,
                       bd=0).grid(row=0, column=1, padx=50)
    l_counter = Label(frm_header, name='l_counter', text="0", background='black', width=10,
                      foreground='green', font=('', 12, 'bold')).grid(row=0, column=2, ipady=2)

    # Game (cells)
    frm_game = ttk.Frame(root, height=Cell.cell_size * settings.size_y + 20, padding=10, name='frm_game')
    frm_game.grid(row=2, column=0)

    # Set images
    bomb = Image.open('images/bomb.png')
    bomb_cell = bomb.resize((Cell.cell_size, Cell.cell_size))
    chocoflag = Image.open('images/chocoflag.png')
    chocoflag_cell = chocoflag.resize((Cell.cell_size, Cell.cell_size))
    images = {
        "plain": PhotoImage(width=Cell.cell_size, height=Cell.cell_size),
        "mine": ImageTk.PhotoImage(bomb_cell),
        "flag": ImageTk.PhotoImage(chocoflag_cell)
    }

    # Create cells
    create_cells(settings.size_x, settings.size_y)

    root.mainloop()
