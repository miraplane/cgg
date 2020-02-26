from tkinter import *
from task1 import Task1


class MainMenu:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.button1 = Button(self.frame,
                              text='Задача 1',
                              width=15,
                              command=self.open_task1)
        self.button1.grid(row=0, pady=5, padx=35)
        self.button2 = Button(self.frame,
                              text='Задача 2',
                              width=15,
                              command=self.new_window)
        self.button2.grid(row=1, pady=5, padx=35)
        self.button3 = Button(self.frame,
                              text='Задача 3',
                              width=15,
                              command=self.new_window)
        self.button3.grid(row=2, pady=5, padx=35)
        self.button4 = Button(self.frame,
                              text='Задача 4',
                              width=15,
                              command=self.new_window)
        self.button4.grid(row=3, pady=5, padx=35)
        self.button5 = Button(self.frame,
                              text='Задача 5',
                              width=15,
                              command=self.new_window)
        self.button5.grid(row=4, pady=5, padx=35)
        self.button6 = Button(self.frame,
                              text='Задача 6',
                              width=15,
                              command=self.new_window)
        self.button6.grid(row=5, pady=5, padx=35)
        self.frame.pack()

    def new_window(self):
        pass

    def open_task1(self):
        self.task1 = Toplevel(self.master)
        self.app = Task1(self.task1)


if __name__ == "__main__":
    root = Tk()
    app = MainMenu(root)
    root.mainloop()
