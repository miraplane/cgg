from tkinter import *
from PIL import Image, ImageTk
import math


class Task5:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        img = ImageTk.PhotoImage(Image.open('task5.png').resize((150, 70)))
        label_img = Label(self.frame, image=img)
        label_img.image = img
        label_img.grid(row=0, column=0, rowspan=3, columnspan=5)
        Label(self.frame, text='Область определения:') \
            .grid(row=3, column=0, sticky='w')
        Label(self.frame, text='x ∈ [ ') \
            .grid(row=4, column=0,  sticky='e')
        Label(self.frame, text=',') \
            .grid(row=4, column=2, sticky='w')
        Label(self.frame, text=']') \
            .grid(row=4, column=4, sticky='w')
        Label(self.frame, text='y ∈ [ ') \
            .grid(row=5, column=0,  sticky='e')
        Label(self.frame, text=',') \
            .grid(row=5, column=2, sticky='w')
        Label(self.frame, text=']') \
            .grid(row=5, column=4, sticky='w')

        self.entry_x0 = Entry(self.frame, width=4, justify=CENTER)
        self.entry_xk = Entry(self.frame, width=4, justify=CENTER)
        self.entry_y0 = Entry(self.frame, width=4, justify=CENTER)
        self.entry_yk = Entry(self.frame, width=4, justify=CENTER)

        self.entry_x0.grid(row=4, column=1)
        self.entry_xk.grid(row=4, column=3)
        self.entry_y0.grid(row=5, column=1)
        self.entry_yk.grid(row=5, column=3)

        self.entry_x0.insert(0, '-3')
        self.entry_xk.insert(0, '3')
        self.entry_y0.insert(0, '-3')
        self.entry_yk.insert(0, '3')

        self.window_border = 90
        self.window_width = int(master.winfo_screenwidth() / 2)
        self.window_height = int(master.winfo_screenheight() / 3 * 2)

        self.my_canvas = Canvas(self.frame, width=self.window_width,
                                height=self.window_height, bg='white')
        self.my_canvas.grid(row=0, rowspan=32, column=5)

        Button(self.frame, text='Paint', command=self.paint, width=10) \
            .grid(row=6, column=0, columnspan=4)

        self.window_width -= 2 * self.window_border
        self.window_height -= 2 * self.window_border

        self.first_count = 70
        self.second_count = self.window_width * 2
        self.min_x, self.max_x = 0, 0
        self.min_y, self.max_y = 0, 0
        self.max_screen_x = self.max_screen_y = self.max_screen_z = -math.inf
        self.min_screen_x = self.min_screen_y = self.min_screen_z = math.inf

    @staticmethod
    def my_function(x, y):
        return x * y

    @staticmethod
    def screen_coord(x, y, z):
        screen_x = (y - x) * math.sqrt(3) / 2
        screen_y = (y + x) / 2 - z
        return screen_x, screen_y

    def add_border(self, x, y):
        return x + self.window_border, y + self.window_border

    def create_point(self, x, y, color):
        x, y = self.add_border(x, y)
        self.my_canvas.create_oval(x, y, x, y, outline=color)

    def create_line(self, x0, y0, xk, yk):
        x0, y0 = self.add_border(x0, y0)
        xk, yk = self.add_border(xk, yk)
        self.my_canvas.create_line(x0, y0, xk, yk, fill='grey')

    def create_text(self, x, y, anchor, text):
        x, y = self.add_border(x, y)
        self.my_canvas.create_text(x, y, anchor=anchor, text=text)

    def move_coord(self, x, y):
        kx = self.window_width / (self.max_screen_x - self.min_screen_x)
        ky = self.window_height / (self.max_screen_y - self.min_screen_y)
        return (
            round((x - self.min_screen_x) * kx),
            round((y - self.min_screen_y) * ky)
        )

    def set_boundaries(self):
        for i in range(self.first_count):
            x = self.max_x - i * (self.max_x - self.min_x) / self.first_count
            for j in range(self.second_count):
                y = self.max_y - j * (self.max_y - self.min_y) / self.second_count
                self.init_horizon(x, y)

    def init_horizon(self, x, y):
        z = self.my_function(x, y)
        screen_x, screen_y = self.screen_coord(x, y, z)
        self.max_screen_x = max(self.max_screen_x, screen_x)
        self.min_screen_x = min(self.min_screen_x, screen_x)
        self.max_screen_y = max(self.max_screen_y, screen_y)
        self.min_screen_y = min(self.min_screen_y, screen_y)
        self.max_screen_z = max(self.max_screen_z, z)
        self.min_screen_z = min(self.min_screen_z, z)

    def get_coord(self, x, y, z):
        screen_x, screen_y = self.screen_coord(x, y, z)
        return self.move_coord(screen_x, screen_y)

    def draw_point(self, x, y, top, bottom):
        z = self.my_function(x, y)
        screen_x, screen_y = self.get_coord(x, y, z)
        if screen_y > bottom[screen_x]:
            self.create_point(screen_x, screen_y, "indigo")
            bottom[screen_x] = screen_y
        if screen_y < top[screen_x]:
            self.create_point(screen_x, screen_y, "violet")
            top[screen_x] = screen_y

    def draw_lines_x(self):
        top = [self.window_height] * (self.window_width + 1)
        bottom = [0] * (self.window_width + 1)
        for i in range(1, self.first_count):
            x = self.max_x - i * (self.max_x - self.min_x) / self.first_count
            for j in range(self.second_count):
                y = self.max_y - j * (self.max_y - self.min_y) / self.second_count
                self.draw_point(x, y, top, bottom)

    def draw_lines_y(self):
        top = [self.window_height] * (self.window_width + 1)
        bottom = [0] * (self.window_width + 1)
        for j in range(1, self.first_count):
            y = self.max_y - j * (self.max_y - self.min_y) / self.first_count
            for i in range(self.second_count):
                x = self.max_x - i * (self.max_x - self.min_x) / self.second_count
                self.draw_point(x, y, top, bottom)

    def draw_grid(self):
        z = self.min_screen_z
        step = (self.max_y - self.min_y) / 5
        for i in range(5 + 1):
            y = self.min_y + i * step
            x0, y0 = self.get_coord(self.min_x, y, z)
            xk, yk = self.get_coord(self.max_x, y, z)
            self.create_line(x0, y0, xk, yk)
            self.create_text(xk, yk, 'nw', str(round(y)))

        step = (self.max_x - self.min_x) / 5
        for i in range(5 + 1):
            x = self.min_x + i * step
            x0, y0 = self.get_coord(x, self.min_y, z)
            xk, yk = self.get_coord(x, self.max_y, z)
            self.create_line(x0, y0, xk, yk)
            self.create_text(xk, yk, 'ne', str(round(x)))

        x = self.min_x
        step = (self.max_y - self.min_y) / 5
        for i in range(5 + 1):
            y = self.min_y + i * step
            x0, y0 = self.get_coord(x, y, self.min_screen_z)
            xk, yk = self.get_coord(x, y, self.max_screen_z)
            self.create_line(x0, y0, xk, yk)

        step = (self.max_screen_z - self.min_screen_z) / 5
        for i in range(5 + 1):
            z = self.min_screen_z + i * step
            x0, y0 = self.get_coord(x, self.min_y, z)
            xk, yk = self.get_coord(x, self.max_y, z)
            self.create_line(x0, y0, xk, yk)

        y = self.min_y
        step = (self.max_x - self.min_x) / 5
        for i in range(5 + 1):
            x = self.min_x + i * step
            x0, y0 = self.get_coord(x, y, self.min_screen_z)
            xk, yk = self.get_coord(x, y, self.max_screen_z)
            self.create_line(x0, y0, xk, yk)

        step = (self.max_screen_z - self.min_screen_z) / 5
        for i in range(5 + 1):
            z = self.min_screen_z + i * step
            x0, y0 = self.get_coord(self.min_x, y, z)
            xk, yk = self.get_coord(self.max_x, y, z)
            self.create_line(x0, y0, xk, yk)
            self.create_text(xk, yk, 'se', str(round(z)))

    def update_arg(self):
        self.max_screen_x = self.max_screen_y = -math.inf
        self.min_screen_x = self.min_screen_y = math.inf

        self.min_x = float(self.entry_x0.get())
        self.max_x = float(self.entry_xk.get())
        self.min_y = float(self.entry_y0.get())
        self.max_y = float(self.entry_yk.get())

    def paint(self):
        self.my_canvas.delete(ALL)
        self.update_arg()

        self.set_boundaries()
        self.draw_grid()
        self.draw_lines_x()
        self.draw_lines_y()
