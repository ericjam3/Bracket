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

        self.brackets = {}

        self.home = Home(parent=container, controller=self)
        self.home.grid(row=0, column=0, sticky="nsew")
        self.home.tkraise()


       # self.frames = {}
    #    dummy = StringVar()
   #     self.entries = [dummy] * 17
  #      self.frame = Bracket(parent=container, controller=self, cols=4, type="entry")
 #       self.frame.grid(row=0, column=0, sticky="nsew")
#        self.frame.tkraise()

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
        self.parent = parent

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
        self.ind = 9
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
                        self.controller.entries[self.ind] = self.entity
                        self.ind += 1
                        self.canvas.create_window(80 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=self.entry)

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
        for i in range(len(self.controller.entries)):
            if self.controller.entries[i].get():
                print self.controller.entries[i].get()


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        # Create bracket button
        Label(self, text="Bracket City", font=36).grid()
        self.create = Button(self, text="Create Tournament")
        self.create.bind("<Button-1>", self.create_tourney)
        self.create.grid()

        # Load bracket button
        self.load = Button(self, text="Load Tournament")
        self.load.bind("<Button-1>", self.load_tourney)
        self.load.grid()

    def create_tourney(self, event):
        createTeam = Create_Bracket(parent=self.parent, controller=self.controller)
        createTeam.grid(row=0, column=0, sticky="nsew")
        createTeam.tkraise()

    def load_tourney(self, event):
        loadTeam = Load_Bracket(parent=self.parent, controller=self.controller)
        loadTeam.grid(row=0, column=0, sticky="nsew")
        loadTeam.tkraise()


class Create_Bracket(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        Label(self, text="Bracket Name:").grid(sticky="w")
        self.name = StringVar()
        entry1 = Entry(self, textvariable=self.name)
        entry1.grid(row=0, column=1)

        Label(self, text="Number of Teams:").grid(row=1, column=0, sticky="w")
        self.numTeams = IntVar()
        entry2 = Entry(self, textvariable=self.numTeams)
        entry2.grid(row=1, column=1)

        Label(self, text="Number of Seeds:").grid(row=2, column=0, sticky="w")
        self.numSeeds = IntVar()
        entry3 = Entry(self, textvariable=self.numSeeds)
        entry3.grid(row=2, column=1)

        button = Button(self, text="Done")
        button.bind("<Button-1>", self.done_button)
        button.grid()

    def done_button(self, event):
        self.controller.brackets[self.name.get()] = {}
        self.controller.brackets[self.name.get()]["numTeams"] = self.numTeams
        self.controller.brackets[self.name.get()]["numSeeds"] = self.numSeeds
        self.controller.home.tkraise()


class Load_Bracket(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent



if __name__ == "__main__":
    app = App()
    app.mainloop()