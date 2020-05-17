from tkinter import *
from tkinter.scrolledtext import ScrolledText
import random
import math


class Vector:
    def __init__(self, x1, y1, x2, y2):
        self.x = x2 - x1
        self.y = y2 - y1

    def get(self):
        return self.x, self.y

    def scalar_product(self, other):
        return other.x * self.x + other.y * self.y


class Polygon:
    def __init__(self):
        self.vertex = []
        self.color = self.set_color()
        self.minx = self.miny = math.inf
        self.maxx = self.maxy = -math.inf

    def set_color(self):
        colors = ["red", "orange", "yellow", "green", "blue", "indigo",
                  "violet"]
        return random.choice(colors)

    def change_border(self, x, y):
        self.maxx = max(x, self.maxx)
        self.minx = min(x, self.minx)
        self.maxy = max(y, self.maxy)
        self.miny = min(y, self.miny)

    def add_vertex(self, x, y):
        self.vertex.append((x, y))
        self.change_border(x, y)

    def get_vertex(self):
        return self.vertex

    def get_color(self):
        return self.color

    def get_border(self):
        return self.minx, self.maxx, self.miny, self.maxy


class Task4:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()

        Label(self.frame, text='Введите координаты вершин многоугольника:') \
            .grid(row=0, column=0, columnspan=3, sticky='w')

        self.entry = ScrolledText(self.frame, height=10, width=5)
        self.entry.insert(INSERT,
                          "43, 31 \n129, -93 \n215, 62 \n172, 155 \n86, 155")
        self.entry.grid(row=1, column=0, columnspan=3, sticky="NESW")

        self.polygons = []
        self.color = None
        self.border = (math.inf, -math.inf, math.inf, -math.inf)

        self.window_border = 50
        self.count_grid_line = 20
        self.window_width = int(master.winfo_screenwidth() / 2)
        self.window_height = int(master.winfo_screenheight() / 3 * 2)
        self.work_space_width = self.window_width - 2 * self.window_border
        self.work_space_height = self.window_height - 2 * self.window_border
        self.range_x = int(self.work_space_width / 2)
        self.range_y = int(self.work_space_height / 2)

        self.my_canvas = Canvas(self.frame, width=self.window_width,
                                height=self.window_height, bg='white')
        self.my_canvas.grid(row=0, rowspan=32, column=4)

        Button(self.frame, text='Add', command=self.add, width=10) \
            .grid(row=5, column=0, sticky="NESW")
        Button(self.frame, text='Clear', command=self.clear, width=10) \
            .grid(row=5, column=2, sticky="NESW")

        self.clear_canvas()

    def draw_axis(self):
        x0 = self.window_width / 2
        y0 = self.window_height / 2
        self.my_canvas.create_line(x0, self.window_height - self.window_border,
                                   x0, self.window_border,
                                   width=2, arrow=LAST)
        self.my_canvas.create_line(self.window_border, y0,
                                   self.window_width - self.window_border, y0,
                                   width=2, arrow=LAST)

    def draw_vertical(self, x, text):
        self.my_canvas.create_text(
            x, self.window_height - self.window_border,
            anchor=NW, text=text)
        self.my_canvas.create_line(
            x, self.window_border,
            x, self.window_height - self.window_border,
            fill='grey')

    def draw_horizontal(self, y, text):
        self.my_canvas.create_text(
            self.window_border, y,
            anchor=E, text=text)
        self.my_canvas.create_line(
            self.window_border, y,
            self.window_width - self.window_border, y,
            fill='grey')

    def draw_line(self, work_space_size, create_line, direction):
        cell_size = work_space_size / self.count_grid_line
        start = direction * (work_space_size / 2)
        for i in range(self.count_grid_line + 1):
            coord = self.window_border + i * cell_size
            text = str(int(start))
            start -= direction * cell_size
            create_line(coord, text)

    def draw_grid(self):
        self.draw_line(self.work_space_width, self.draw_vertical, -1)
        self.draw_line(self.work_space_height, self.draw_horizontal, 1)

    def point_in_workspace(self, x, y):
        return -self.range_x <= x <= self.range_x and \
               -self.range_y <= y <= self.range_y

    def clear_entry(self):
        self.entry.delete("1.0", END)

        new_entry = ""
        for i in range(3):
            x = random.randint(-self.range_x, self.range_x)
            y = random.randint(-self.range_y, self.range_y)
            new_entry += "{0}, {1} \n".format(x, y)

        self.entry.insert(INSERT, new_entry)

    def clear_canvas(self):
        self.my_canvas.delete(ALL)
        self.draw_grid()
        self.draw_axis()

    def update_border(self, polygon):
        pminx, pmaxx, pminy, pmaxy = polygon.get_border()
        minx, maxx, miny, maxy = self.border
        self.border = (
            min(pminx, minx),
            max(pmaxx, maxx),
            min(pminy, miny),
            max(pmaxy, maxy))

    def parse_coords(self):
        str_coords = self.entry.get("1.0", END).split('\n')

        polygon = Polygon()
        for c in str_coords:
            if ', ' in c:
                x, y = map(int, c.split(', '))
                polygon.add_vertex(x, y)
        if len(polygon.get_vertex()) >= 3:
            self.polygons.append(polygon)
            self.update_border(polygon)

    def check_point(self, x, y):
        in_polygons = 0
        for polygon in self.polygons:
            vertex = polygon.get_vertex()
            result = False
            end_x, end_y = vertex[len(vertex) - 1]
            for point in vertex:
                px, py = point
                if (py <= y < end_y or end_y <= y < py) and \
                        (x > (end_x - px) * (y - py) / (end_y - py) + px):
                    result = not result
                end_x, end_y = px, py
            if result:
                self.color = polygon.get_color()
                in_polygons += 1

        return in_polygons == 1

    def add(self):
        self.parse_coords()
        self.clear_entry()
        self.clear_canvas()
        minx, maxx, miny, maxy = map(int, self.border)

        for i in range(minx, maxx):
            for j in range(miny, maxy):
                if self.check_point(i, j) and self.point_in_workspace:
                    x = i + self.window_border + self.work_space_width / 2
                    y = self.window_border + self.work_space_height / 2 - j
                    self.my_canvas.create_oval(
                        x, y, x, y,
                        width=1, outline=self.color)

    def clear(self):
        self.clear_entry()
        self.clear_canvas()
        self.polygons = []
