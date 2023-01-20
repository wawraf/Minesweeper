from tkinter import *
from cell import Cell
import settings


root = Tk()

# Override default settings
root.configure(background="black")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title("Minesweeper")
root.resizable(False, False)

top_frame = Frame(
    root,
    bg='blue',
    width=settings.WIDTH,
    height=settings.height_perc(20)
)
top_frame.place(x=0,y=0)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Minesweeper',
    font=('', 48)
)

game_title.place(
    x=settings.width_perc(23),
    y=0
)

left_frame = Frame(
    root,
    bg="yellow",
    width=settings.width_perc(15),
    height=settings.height_perc(80)
)
left_frame.place(x=0, y=settings.height_perc(20))

center_frame = Frame(
    root,
    bg="pink",
    width=settings.width_perc(85),
    height=settings.height_perc(80)
)
center_frame.place(x=settings.width_perc(15), y=settings.height_perc(20))

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x,y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x, row=y)

# Call the label
Cell.create_cell_count_label((left_frame))
Cell.cell_count_label_object.place(
    x=0,
    y=0
)

Cell.randomize_mines()


# Run the window
root.mainloop()