from tkinter import *
from PIL import Image, ImageTk
import math


class Task1:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        img = ImageTk.PhotoImage(Image.open('f.png').resize((280, 100)))
        label_img = Label(self.frame, image=img)
        label_img.image = img
        label_img.grid(row=0, column=0, rowspan=3, columnspan=4)
        Label(self.frame, text='Введите интервал:  [') \
            .grid(row=3, column=0, sticky='e')
        Label(self.frame, text=']') \
            .grid(row=3, column=3, sticky='w')
        Label(self.frame, text='Введите значение параметров:') \
            .grid(row=4, column=0, sticky='w')
        Label(self.frame, text='a = ')\
            .grid(row=4, column=1)
        Label(self.frame, text='b = ')\
            .grid(row=5, column=1)

        self.entry_start = Entry(self.frame, width=4, justify=CENTER)
        self.entry_end = Entry(self.frame, width=4, justify=CENTER)
        self.entry_a = Entry(self.frame, width=4, justify=CENTER)
        self.entry_b = Entry(self.frame, width=4, justify=CENTER)

        self.entry_start.grid(row=3, column=1)
        self.entry_end.grid(row=3, column=2)
        self.entry_a.grid(row=4, column=2)
        self.entry_b.grid(row=5, column=2)

        self.start = self.end = self.width = 0
        self.min_y = self.max_y = self.height = 0
        self.a = self.b = 0

        self.window_border = 100
        self.count_grid_line = 20
        self.window_width = int(master.winfo_screenwidth() / 2)
        self.window_height = int(master.winfo_screenheight() / 3 * 2)
        self.my_canvas = Canvas(self.frame, width=self.window_width,
                                height=self.window_height, bg='white')
        self.my_canvas.grid(row=0, rowspan=32, column=4)

        self.window_width -= 2 * self.window_border
        self.window_height -= 2 * self.window_border

        Button(self.frame, text='Paint', command=self.paint, width=10) \
            .grid(row=6, column=0, columnspan=4)

    def my_function(self, x):
        if (self.b - x) == 0:
            return None
        n = (self.a + x) / (self.b - x)
        if n == 0:
            return None
        return n ** 4

    def calculate_range(self):
        self.min_y = math.inf
        self.max_y = -math.inf
        for i in range(0, self.window_width):
            x = self.start + i * self.width / self.window_width
            y = self.my_function(x)
            if not y:
                continue
            self.min_y = min(y, self.min_y)
            self.max_y = max(y, self.max_y)

        self.height = self.max_y - self.min_y
        if self.height == 0:
            self.height = 2

    def update_arg(self):
        self.start = int(self.entry_start.get())
        self.end = int(self.entry_end.get())
        self.width = self.end - self.start

        self.a = int(self.entry_a.get())
        self.b = int(self.entry_b.get())

    def create_axis(self, begin, end):
        return self.my_canvas.create_line(begin, end, width=2, arrow=LAST)

    def check_axis(self, my_id, point, left_border, right_border):
        if point < left_border or point > right_border:
            self.my_canvas.delete(my_id)

    def draw_axis(self):
        x0 = self.start * self.window_width / -self.width + self.window_border
        y0 = self.max_y * self.window_height / self.height + self.window_border

        line_id = self.create_axis(
            (x0, self.window_height + self.window_border),
            (x0, self.window_border)
        )
        self.check_axis(line_id, int(x0), self.window_border,
                        self.window_width + self.window_border)

        line_id = self.create_axis(
            (self.window_border, y0),
            (self.window_width + self.window_border, y0)
        )
        self.check_axis(line_id, int(y0), self.window_border,
                        self.window_height + self.window_border)

    def draw_vertical(self, i, text):
        self.my_canvas.create_text(i + self.window_border,
                                   self.window_height + self.window_border,
                                   anchor=NW, text=text)
        self.my_canvas.create_line((i + self.window_border,
                                    self.window_border),
                                   (i + self.window_border,
                                    self.window_height + self.window_border),
                                   fill='grey')

    def draw_horizontal(self, j, text):
        self.my_canvas.create_text(self.window_border,
                                   j + self.window_border,
                                   anchor=E, text=text)
        self.my_canvas.create_line((self.window_border,
                                    j + self.window_border),
                                   (self.window_width + self.window_border,
                                    j + self.window_border),
                                   fill='grey')

    def draw_line(self, window_size, real_size, start, draw, direction):
        cell_size = window_size / real_size
        size = direction
        if (window_size / cell_size) > self.count_grid_line:
            cell_size = window_size / self.count_grid_line
            size = direction * real_size / self.count_grid_line
        
        count = int(window_size / cell_size) + 1
        for i in range(0, count):
            text = str(int(start))
            start += size
            draw(i * cell_size, text)

    def draw_grid(self):
        self.draw_line(self.window_width,
                       self.width,
                       self.start,
                       self.draw_vertical,
                       1)
        self.draw_line(self.window_height,
                       self.height,
                       self.max_y,
                       self.draw_horizontal,
                       -1)

    def paint(self):
        self.my_canvas.delete(ALL)
        self.update_arg()
        self.calculate_range()

        start_y = self.my_function(self.start)
        if start_y:
            dy = self.max_y - self.my_function(self.start)
        else:
            dy = self.max_y
        j = dy * self.window_height / self.height
        last = (self.window_border, j + self.window_border)

        self.draw_grid()
        self.draw_axis()

        for i in range(1, self.window_width):
            x = self.start + i * self.width / self.window_width
            y = self.my_function(x)
            if not y:
                continue

            j = (self.max_y - y) * self.window_height / self.height
            self.my_canvas.create_line(last,
                                       (i + self.window_border,
                                        j + self.window_border),
                                       width=3, fill='blue')
            last = (i + self.window_border, j + self.window_border)
