import sys
from tkinter import Button, Label
from random import sample
from sys import exit
from time import sleep
import settings
import ctypes

class Cell:
    all = []
    cells_left = settings.GRID_SIZE ** 2

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.x = x
        self.y = y
        self.display_text = False
        self.cell_btn_object = None
        self.__isopened = False

        Cell.all.append(self)

    def create_btn_object(self, location):
        # location.update()
        # print(location.winfo_width())
        btn = Button(
            location,
            width=13, #int(location.winfo_width()/self.size),
            height=3, #int(location.winfo_height()/self.size),
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"Cells left: {Cell.cells_left}",
            width=13,
            height=3,
            bg='yellow',
            fg='black'
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.__isopened:
            return

        if self.is_mine:
            self.show_mine()
        else:
            cells, mines = self.get_surrounding_cells
            if mines == 0:
                for cell in cells:
                    cell.show_cell()
            self.show_cell()

    @property
    def get_surrounding_cells(self):
        func = lambda cell: (not cell.__isopened) and not (cell.x == self.x and cell.y == self.y) and (self.x-1 <= cell.x <= self.x+1) and (self.y-1 <= cell.y <= self.y+1)
        surrounding_cells = list(filter(func, Cell.all))
        mines = len([cell for cell in surrounding_cells if cell.is_mine])
        return surrounding_cells, mines

    def show_cell(self):
        l = self.get_surrounding_cells[1]
        self.cell_btn_object.configure(text=l)
        self.cell_btn_object.configure(fg="black")
        self.__isopened = True

        # Replace cell count label
        Cell.cells_left -= 1
        Cell.cell_count_label_object.configure(text=f"Cells left: {Cell.cells_left}")
        if Cell.cells_left == settings.MINES_COUNT:
            ctypes.windll.user32.MessageBoxW(0, 'Congrats! You have won!', 'Game over', 0)
            exit(1)

    def show_mine(self):
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, 'You stepped on the mine!', 'Game over', 0)
        exit(1)

    def right_click_actions(self, event):
        if self.__isopened: # unbind can be used for btn object
            return
        if not self.display_text:
            self.cell_btn_object.configure(text="X")
            self.cell_btn_object.configure(fg='red')
        else:
            self.cell_btn_object.configure(text="")
            self.cell_btn_object.configure(fg='black')

        self.display_text = not self.display_text


    @staticmethod
    def randomize_mines():
        mined_cells = sample(Cell.all, settings.MINES_COUNT)
        for cell in mined_cells:
            cell.is_mine = True

    def __repr__(self):
        return f"Cell{self.x,self.y}"