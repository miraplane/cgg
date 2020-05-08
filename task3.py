from tkinter import *
from PIL import Image, ImageTk
import math


class Task3:
    def __init__(self, master):
        self.master = master
        self.master.title('Постороние параболы методом Брезенхема')
        self.frame = Frame(self.master)
        self.frame.pack()

        img = ImageTk.PhotoImage(Image.open('task3.png').resize((200, 100)))
        label_img = Label(self.frame, image=img)
        label_img.image = img
        label_img.grid(row=0, column=0, rowspan=3, columnspan=4)
        Label(self.frame, text='Введите значение параметра:') \
            .grid(row=3, column=0, sticky='w')
        Label(self.frame, text='p = ') \
            .grid(row=3, column=1)

        self.entry_p = Entry(self.frame, width=4, justify=CENTER)

        self.entry_p.grid(row=3, column=2)

        self.p = 0

        self.window_border = 50
        self.count_grid_line = 20
        self.window_width = int(master.winfo_screenwidth() / 2)
        self.window_height = int(master.winfo_screenheight() / 3 * 2)
        self.work_space_width = self.window_width - 2 * self.window_border
        self.work_space_height = self.window_height - 2 * self.window_border

        self.my_canvas = Canvas(self.frame, width=self.window_width,
                                height=self.window_height, bg='white')
        self.my_canvas.grid(row=0, rowspan=32, column=4)

        Button(self.frame, text='Paint', command=self.paint, width=10) \
            .grid(row=5, column=0, columnspan=4)

    def my_function(self, x):
        if self.p == 0:
            return None
        return x * x / (2 * self.p)

    def update_arg(self):
        self.p = float(self.entry_p.get())

    def get_distance(self, x, y):
        return math.fabs(y - self.my_function(x))

    def draw_point(self, x, y):
        y += self.window_border
        x += self.window_border
        self.my_canvas.create_oval(x, y, x, y, width=2, outline='blue')

    def draw_parabola(self):
        x = y = 0
        max_x = self.work_space_width / 2
        max_y = self.work_space_height
        dy = 1 if self.p > 0 else -1
        start_x = max_x
        start_y = max_y if self.p > 0 else 0
        while True:
            if math.fabs(x) > max_x or math.fabs(y) > max_y:
                break
            self.draw_point(start_x + x, start_y - y)
            self.draw_point(start_x - x, start_y - y)

            diagonal_d = self.get_distance(x + 1, y + dy)
            vertical_d = self.get_distance(x, y + dy)
            horizontal_d = self.get_distance(x + 1, y)
            if horizontal_d <= vertical_d:
                if diagonal_d < horizontal_d:
                    y += dy
                x += 1
            else:
                if diagonal_d < vertical_d:
                    x += 1
                y += dy

    def draw_axis(self):
        x0 = self.window_width / 2
        y0 = self.window_height - self.window_border
        yk = self.window_border
        if self.p < 0:
            let = y0
            y0 = yk
            yk = let
        self.my_canvas.create_line(x0, y0, x0, yk,
                                   width=2, arrow=LAST)
        self.my_canvas.create_line(self.window_border, y0,
                                   self.window_width - self.window_border, y0,
                                   width=2, arrow=LAST)

    def draw_vertical(self):
        cell_size = self.work_space_width / self.count_grid_line
        start = -1 * (self.work_space_width / 2)
        for i in range(self.count_grid_line + 1):
            x = self.window_border + i * cell_size
            text = str(int(start))
            start += cell_size
            self.my_canvas.create_text(
                x, self.window_height - self.window_border,
                anchor=NW, text=text)
            self.my_canvas.create_line(
                x, self.window_border,
                x, self.window_height - self.window_border,
                fill='grey')

    def draw_horizontal(self):
        cell_size = self.work_space_height / self.count_grid_line
        start = self.work_space_height if self.p > 0 else 0
        for i in range(self.count_grid_line + 1):
            y = self.window_border + i * cell_size
            text = str(int(start))
            start -= cell_size
            self.my_canvas.create_text(
                self.window_border, y,
                anchor=E, text=text)
            self.my_canvas.create_line(
                self.window_border, y,
                self.window_width - self.window_border, y,
                fill='grey')

    def draw_grid(self):
        self.draw_vertical()
        self.draw_horizontal()

    def paint(self):
        self.my_canvas.delete(ALL)
        self.update_arg()

        self.draw_grid()
        self.draw_axis()
        self.draw_parabola()
