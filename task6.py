from tkinter import *
from PIL import Image, ImageTk
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Task6:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        img = ImageTk.PhotoImage(Image.open('task6.png').resize((130, 60)))
        label_img = Label(self.frame, image=img)
        label_img.image = img
        label_img.grid(row=0, column=0, rowspan=3, columnspan=5)

        Label(self.frame, text='a = ') \
            .grid(row=3, column=0,  sticky='e')
        Label(self.frame, text='b = ') \
            .grid(row=4, column=0, sticky='e')

        Label(self.frame, text='z ∈ [ ') \
            .grid(row=5, column=0,  sticky='e')
        Label(self.frame, text=',') \
            .grid(row=5, column=2, sticky='w')
        Label(self.frame, text=']') \
            .grid(row=5, column=4, sticky='w')

        self.entry_a = Entry(self.frame, width=4, justify=CENTER)
        self.entry_b = Entry(self.frame, width=4, justify=CENTER)
        self.entry_z0 = Entry(self.frame, width=4, justify=CENTER)
        self.entry_zk = Entry(self.frame, width=4, justify=CENTER)

        self.entry_a.grid(row=3, column=1)
        self.entry_b.grid(row=4, column=1)
        self.entry_z0.grid(row=5, column=1)
        self.entry_zk.grid(row=5, column=3)

        self.entry_a.insert(0, '100')
        self.entry_b.insert(0, '100')
        self.entry_z0.insert(0, '0')
        self.entry_zk.insert(0, '300')

        self.window_width = int(master.winfo_screenwidth() / 2)
        self.window_height = int(master.winfo_screenheight() / 3 * 2)
        self.center = {
            'x': self.window_width / 2,
            'y': self.window_height / 3 * 2
        }

        self.my_canvas = Canvas(self.frame, width=self.window_width,
                                height=self.window_height, bg='white')
        self.my_canvas.grid(row=0, rowspan=32, column=5)

        Button(self.frame, text='Paint', command=self.paint, width=10) \
            .grid(row=7, column=0, columnspan=4)

        self.a = self.b = 1
        self.min_z, self.max_z = 0, 10
        self.buffer = []

    @staticmethod
    def from_rgb(rgb):
        return "#%02x%02x%02x" % rgb

    @staticmethod
    def screen_color(z):
        r = math.floor(153 * (math.atan(z / 100) / math.pi + 0.5))
        g = math.floor(204 * (math.atan(z / 100) / math.pi + 0.5))
        b = math.floor(255 * (math.atan(z / 100) / math.pi + 0.5))

        return r, g, b

    def draw_grid(self):
        size = 300
        step = 50

        z = self.min_z
        for y in range(-size, size, step):
            for x in range(size, -size, -1):
                color = 'black' if y == 0 else 'grey'
                screen_x, screen_y, screen_z = self.screen_coord(x, y, z)
                self.my_canvas.create_oval(
                    screen_x, screen_y,
                    screen_x, screen_y,
                    outline=color)
            screen_x, screen_y, screen_z = self.screen_coord(-size, y, z)
            self.my_canvas.create_text(
                screen_x, screen_y,
                anchor=NE, text=str(y)
            )

        for x in range(size, -size, -step):
            for y in range(-size, size):
                color = 'black' if x == 0 else 'grey'
                screen_x, screen_y, screen_z = self.screen_coord(x, y, z)
                self.my_canvas.create_oval(
                    screen_x, screen_y,
                    screen_x, screen_y,
                    outline=color)
            screen_x, screen_y, screen_z = self.screen_coord(x, size, z)
            self.my_canvas.create_text(
                screen_x, screen_y,
                anchor=NW, text=str(x)
            )

        for x in range(-size, size, step):
            for z in range(self.min_z, self.max_z):
                screen_x, screen_y, screen_z = self.screen_coord(
                    x, -size, z)
                self.my_canvas.create_oval(
                    screen_x, screen_y,
                    screen_x, screen_y,
                    outline='grey')

        for z in range(self.min_z, self.max_z + 1, step):
            for x in range(-size, size):
                screen_x, screen_y, screen_z = self.screen_coord(
                    x, -size, z)
                self.my_canvas.create_oval(
                    screen_x, screen_y,
                    screen_x, screen_y,
                    outline='grey')

        for y in range(-size, size, step):
            for z in range(self.min_z, self.max_z):
                screen_x, screen_y, screen_z = self.screen_coord(
                    size, y, z)
                self.my_canvas.create_oval(
                    screen_x, screen_y,
                    screen_x, screen_y,
                    outline='grey')

        for z in range(self.min_z, self.max_z + 1, step):
            for y in range(-size, size):
                screen_x, screen_y, screen_z = self.screen_coord(
                    size, y, z)
                self.my_canvas.create_oval(
                    screen_x, screen_y,
                    screen_x, screen_y,
                    outline='grey')
            screen_x, screen_y, screen_z = self.screen_coord(size, size, z)
            self.my_canvas.create_text(
                screen_x, screen_y,
                anchor=SW, text=str(z)
            )

    def screen_coord(self, x, y, z):
        angle_70 = math.radians(70)
        cos70 = math.cos(angle_70)
        sin70 = math.sin(angle_70)
        angle_60 = -math.radians(60)
        cos60 = math.cos(angle_60)
        sin60 = math.sin(angle_60)

        screen_x = math.floor(
            x * cos70 +
            y * sin70 + self.center['x']

        )
        screen_y = math.floor(
            -x * cos60 * sin70 +
            y * cos60 * cos70 +
            z * sin60 + self.center['y']
        )
        screen_z = math.floor(
            sin70 * sin60 * x -
            sin60 * cos70 * y +
            cos60 * z
        )

        return screen_x, screen_y, screen_z

    def update_arg(self):
        self.a = float(self.entry_a.get())
        self.b = float(self.entry_b.get())
        self.min_z = int(self.entry_z0.get())
        self.max_z = int(self.entry_zk.get())

        self.buffer = []
        for i in range(self.window_width + 1):
            self.buffer.append([])
            for j in range(self.window_height + 1):
                self.buffer[i].append(-math.inf)

    def in_window(self, x, y, z):
        return 0 <= x <= self.window_width and \
               0 <= y <= self.window_height and \
               z > self.buffer[x][y]

    def set_pixel(self, x, y, z, rgb):
        if self.in_window(x, y, z):
            self.my_canvas.create_oval(x, y, x, y, outline=self.from_rgb(rgb))
            self.buffer[x][y] = z

    def draw_cylinder(self):
        w_split = 800
        w_step = 2 * math.pi / w_split

        for i in range(w_split):
            x = self.a * math.cos(i * w_step)
            y = self.b * math.sin(i * w_step)
            for z in range(self.min_z, self.max_z):
                xx, yy, zz = self.screen_coord(x, y, z)
                rgb = self.screen_color(zz)
                self.set_pixel(xx, yy, zz, rgb)

    def paint(self):
        self.my_canvas.delete(ALL)
        self.update_arg()

        if self.a == 0 or self.b == 0 or self.max_z - self.min_z == 1:
            return

        self.draw_grid()
        self.draw_cylinder()
