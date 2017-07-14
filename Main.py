from Tkinter import *
import tkMessageBox
import Tkinter as tk
import math

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry('1000x1000')

        # Container is the parent container of the entire program
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menudict = {}
        menubar = Menu(self)
        Draw = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Draw", menu=Draw)
        menudict["Murray's Quarter"] = Menu(menubar, tearoff=0)
        menudict["Nadal's Quarter"] = Menu(menubar, tearoff=0)
        menudict["Federer's Quarter"] = Menu(menubar, tearoff=0)
        menudict["Djokovic's Quarter"] = Menu(menubar, tearoff=0)

        for key in menudict:
            Draw.add_cascade(label=key, menu=menudict[key])
            menudict[key].add_command(label="Full")
            menudict[key].add_command(label="Top Half")
            menudict[key].add_command(label="Bottom Half")

        self.config(menu=menubar)

        self.frames = {}
        '''
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Set frames to take up entire window
            frame.grid(row=0, column=0, sticky="nsew")
        '''
        self.frame = Bracket(parent=container, controller=self, cols=5, type="entry")
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.tkraise()

#        self.frame1 = Bracket(parent=container, controller=self, cols=5)
 #       self.frame1.grid(row=0, column=0, sticky="nsew")
  #      self.frame1.tkraise()

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        return self.frames[page_name]


class Bracket(tk.Frame):

    def __init__(self, parent, controller, cols, type):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        rows = 2 ** (cols - 1)
        self.scrollbar = Scrollbar(self)
        self.canvas = Canvas(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.frame = Frame(self.canvas)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0, 0, window=self.frame, anchor="nw")
        self.frame.grid(row=0, column=0, sticky='news')

        sum = 0
        self.labels = [""] * rows * 2
        self.entries = []
        self.entities = []
        for c in range(cols):
            prev = sum
            if c != 0:
                sum = 2 ** (c - 1) + prev
            for r in range(rows):
                if r % 2 ** c == 0:
                    self.canvas.create_line(10 + (c * 140), 30 + (30 * r) + 15 * (sum), 10 + (c + 1) * 140,
                                            30 + (30 * r) + 15 * (sum))
                    if type == "view":
                        self.label = Label(self.canvas, text="Holy dog sacks")
                        self.label.pack()
                        self.canvas.create_window(80 + (c * 140), 30 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=self.label)
                        self.labels.append(self.label)
                    elif type == "entry" and c == 0:
                        self.entity = StringVar()
                        self.entry = Entry(self.canvas, textvariable=self.entity)
                        self.entry.pack()
                        self.entities.append(self.entity)
                        self.canvas.create_window(80 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=self.entry)
                        self.entries.append(self.entry)

                if (r % 2 ** (c + 1) == 0) and (c < cols - 1):
                    self.canvas.create_line(10 + (140 * (c + 1)), 30 + (30 * r) + 15 * (sum), 10 + (140 * (c + 1)),
                                            30 + (30 * r) + 15 * (sum + (2 ** (c + 1))))


        self.button = Button(self.canvas, text="Submit")
        self.button.bind("<Button-1>", self.submit_entries)
        self.button.pack()
        self.canvas.create_window(800, 15, window=self.button)
        self.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def submit_entries(self, event):
        print self.entities[3].get()


if __name__ == "__main__":
    app = App()
    app.mainloop()