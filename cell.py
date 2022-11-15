import math
import platform
import random
import time
from tkinter import Button, messagebox

import settings

RIGHT_CLICK = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"


class Cell:
    all = []
    is_started = False
    start = None
    cell_size = 50
    root = None
    images = None

    def __init__(self, root, images, frame_game, x, y, is_mine=False):
        # Set global vars. Only first time.
        if Cell.root is None:
            Cell.root = root
        if Cell.images is None:
            Cell.images = images

        self.x = x
        self.y = y
        self.is_mine = is_mine
        self.is_possible_mine = False
        self.is_opened = False
        self.btn = Button(frame_game, text="", command=self.show_cell, bd=4, image=images["plain"], compound='center')
        self.btn.bind(RIGHT_CLICK, self.right_click)
        self.btn.grid(row=self.x, column=self.y)
        Cell.all.append(self)

    def right_click(self, event):
        if not (self.is_possible_mine or self.is_opened):
            event.widget.configure(image=Cell.images['flag'])
            self.is_possible_mine = True
            possible_mines = [cell for cell in Cell.all if cell.is_possible_mine]
            mines_left = settings.NUM_MINES - len(possible_mines)
            widget = Cell.root.nametowidget('frm_header.l_mines_left')
            widget.configure(text=mines_left)

    def show_cell(self):
        # TODO: When last cell that is not a mine is clicked, show a message saying "you win" (with Rikku's voice)
        count = 0
        if not Cell.is_started:
            Cell.is_started = True
            Cell.start = time.time()
            widget = Cell.root.nametowidget('frm_header.l_counter')
            widget.after(500, Cell.timer, widget)
        for cell in self.surrounded_cells:
            if cell.is_mine:
                count += 1
        if not self.is_opened:
            self.is_opened = True
            possible_mines = [cell for cell in Cell.all if cell.is_possible_mine]
            mines_left = settings.NUM_MINES - len(possible_mines)
            if self.is_mine:
                self.btn.configure(image=Cell.images['mine'])
                Cell.is_started = False
                messagebox.showerror(title='You lose', message='Press ok to begin a new game')
                Cell.reset()
            else:
                self.btn.configure(bd=1, image=Cell.images['plain'])
                if self.is_possible_mine:
                    self.is_possible_mine = False
                    # TODO: Create function to count left mines
                    widget = Cell.root.nametowidget('frm_header.l_mines_left')
                    widget.configure(text=mines_left)
                if count == 0:
                    for s_cell in self.surrounded_cells:
                        s_cell.show_cell()  # Recursive method
                else:
                    self.btn.configure(text=f'{count}')
                opened_cells = [cell for cell in Cell.all if cell.is_opened]
                if len(opened_cells) == len(Cell.all) - settings.NUM_MINES:
                    Cell.is_started = False
                    elapsed = math.ceil(time.time() - Cell.start)
                    messagebox.showinfo(title=f'You win in {elapsed} seconds!!', message='Press ok to begin a new game')
                    Cell.reset()
        else:
            if count > 0:
                num_possible_mines = 0
                for cell in self.surrounded_cells:
                    if cell.is_possible_mine:
                        num_possible_mines += 1
                if count == num_possible_mines:
                    for s_cell in self.surrounded_cells:
                        is_mine = s_cell.is_mine
                        if not (s_cell.is_opened or s_cell.is_possible_mine):
                            s_cell.show_cell()
                            if is_mine:
                                break

    @staticmethod
    def reset():
        for cell in Cell.all:
            cell.is_opened = False
            cell.btn.configure(text="", bd=4, image=Cell.images['plain'])
            cell.is_mine = False
            cell.is_possible_mine = False
        Cell.set_mines()
        Cell.start = None

    @staticmethod
    def __find_cell(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
        else:
            return None

    @property
    def surrounded_cells(self):
        cells = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if not (i == self.x and j == self.y):
                    cell = Cell.__find_cell(i, j)
                    if cell is not None:
                        cells.append(cell)
        return cells

    @staticmethod
    def set_mines():
        cell_mines = random.sample(Cell.all, settings.NUM_MINES)
        for cell in cell_mines:
            cell.is_mine = True

    @staticmethod
    def timer(l_counter):
        elapsed = math.ceil(time.time() - Cell.start)
        l_counter.configure(text=elapsed)
        if Cell.is_started:
            l_counter.after(1000, Cell.timer, l_counter)
        else:
            l_counter.configure(text=0)

    def __repr__(self):
        return f'Cell({self.x},{self.y})'
