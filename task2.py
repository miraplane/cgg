from tkinter import *
from PIL import Image, ImageTk
import math


class Task2:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        img = ImageTk.PhotoImage(Image.open('task2.png').resize((280, 100)))
        label_img = Label(self.frame, image=img)
        label_img.image = img
        label_img.grid(row=0, column=0, rowspan=3, columnspan=4)
        Label(self.frame, text='Введите интервал:   φ ∈ [') \
            .grid(row=3, column=0, sticky='e')
        Label(self.frame, text=']') \
            .grid(row=3, column=3, sticky='w')
        Label(self.frame, text='Введите значение параметра:') \
            .grid(row=4, column=0, sticky='w')
        Label(self.frame, text='a = ')\
            .grid(row=4, column=1)

        self.entry_start = Entry(self.frame, width=4, justify=CENTER)
        self.entry_end = Entry(self.frame, width=4, justify=CENTER)
        self.entry_a = Entry(self.frame, width=4, justify=CENTER)

        self.entry_start.grid(row=3, column=1)
        self.entry_end.grid(row=3, column=2)
        self.entry_a.grid(row=4, column=2)

        self.start = self.end = 0
        self.max_r = self.size = 0
        self.a = 0
        self.coords = []

        self.window_border = 40
        self.count_grid_line = 10
        self.window_size = int(master.winfo_screenheight() / 2)
        self.center = int(self.window_size / 2)
        self.my_canvas = Canvas(self.frame, width=self.window_size,
                                height=self.window_size, bg='white')
        self.my_canvas.grid(row=0, rowspan=32, column=4)

        self.window_size -= 2 * self.window_border

        Button(self.frame, text='Paint', command=self.paint, width=10) \
            .grid(row=6, column=0, columnspan=4)

    def my_function(self, phi):
        n = self.a * math.pi
        if n == 0:
            return None
        return 2 * math.radians(phi) / n

    def calculate_range(self):
        self.max_r = -math.inf

        for phi in range(self.start, self.end+1):
            r = self.my_function(phi)
            if not r:
                continue
            self.coords.append((phi, r))
            self.max_r = max(math.fabs(r), self.max_r)

        self.size = round(self.max_r, 1)

    def update_arg(self):
        self.start = int(self.entry_start.get())
        self.end = int(self.entry_end.get())

        self.a = int(self.entry_a.get())
        self.coords = []

    def draw_angle(self, count, cell_size):
        length = round(count) * cell_size
        for angle in range(0, 360, 30):
            self.my_canvas.create_arc(
                self.center - length,
                self.center - length,
                self.center + length,
                self.center + length,
                start=angle,
                extent=30,
                outline='grey'
            )

    def draw_radial(self, count, cell_size, step):
        for i in range(0, round(count) + 1):
            left = self.center - i*cell_size
            right = self.center + i*cell_size
            left_coord = (left, left)
            right_coord = (right, right)
            self.my_canvas.create_oval(left_coord, right_coord, outline='grey')

            text = str(round(i * step, 1))
            if text[len(text) - 1] == '0':
                text = text[:-2]
            self.my_canvas.create_text(
                right,
                self.center,
                text=text,
                anchor=NW
            )

    def draw_axis(self):
        self.my_canvas.create_line(
            (self.window_border, self.center),
            (self.window_size + self.window_border, self.center)
        )
        self.my_canvas.create_line(
            (self.center, self.window_border),
            (self.center, self.window_size + self.window_border)
        )
        self.my_canvas.create_text(
            self.window_size + self.window_border * 1.5,
            self.center,
            text='0°',
        )
        self.my_canvas.create_text(
            self.center,
            self.window_border / 2,
            text='90°',
        )
        self.my_canvas.create_text(
            self.window_border / 2,
            self.center,
            text='180°',
        )
        self.my_canvas.create_text(
            self.center,
            self.window_size + self.window_border * 1.5,
            text='270°',
        )

    def draw_grid(self):
        step = 0.1
        count = self.size / step

        while count > self.count_grid_line:
            step *= 2
            count = self.size / step

        cell_size = self.window_size / (count * 2)

        self.draw_angle(count, cell_size)
        self.draw_radial(count, cell_size, step)
        self.draw_axis()

    def rotate(self, point, angle):
        angle = math.radians(-1*angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)

        x, y = point
        x -= self.center
        y -= self.center

        new_x = x * cos_val - y * sin_val
        new_y = x * sin_val + y * cos_val

        return new_x + self.center, new_y + self.center

    def paint(self):
        self.my_canvas.delete(ALL)
        self.update_arg()
        if self.a == 0 or self.start - self.end == 0:
            return

        self.calculate_range()

        self.draw_grid()

        phi, r = self.coords[0]
        point = (self.center + r * (self.window_size / (self.size * 2)),
                 self.center)
        last = self.rotate(point, phi)
        for coord in self.coords:
            phi, r = coord
            point = (self.center + r * (self.window_size / (self.size * 2)),
                     self.center)
            current = self.rotate(point, phi)
            self.my_canvas.create_line(last, current,
                                       width=4, fill='blue')
            last = current
