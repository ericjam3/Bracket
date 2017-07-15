from Tkinter import *
import tkMessageBox
import Tkinter as tk
import math
from ttk import *
import ttk
import functools

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

    def __init__(self, parent, controller, numTeams, type, name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.type = type

        cols = 1
        rem = numTeams
        while rem > 1:
            rem /= 2
            cols += 1

        rows = numTeams
        self.scrollbar = Scrollbar(self)
        self.canvas = Canvas(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.frame = Frame(self.canvas)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0, 0, window=self.frame, anchor="nw")
        self.frame.grid(row=0, column=0, sticky='news')

        sum = 0
        self.labels = []
        for i in range(rows * 2):
            temp = Label(self.canvas)
            temp.pack()
            self.labels.append(temp)
        ind = numTeams
        end = (numTeams * 2) - 1

        for c in range(cols):
            prev = sum
            if c != 0:
                sum = 2 ** (c - 1) + prev
            for r in range(rows):
                if r % 2 ** c == 0:
                    self.canvas.create_line(10 + (c * 140), 30 + (30 * r) + 15 * (sum), 10 + (c + 1) * 140,
                                            30 + (30 * r) + 15 * (sum))
                    if type == "view":
                        label = Label(self.canvas, text=self.controller.brackets[name]["entries"][ind].get())
                        label.pack()
                        self.canvas.create_window(80 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=label)
                        if ind >= end:
                            end = ((ind + 1) / 2) - 1
                            ind = (ind + 1) / 4
                            ind -= 1
                        ind += 1

                    elif type == "entry" and c == 0:
                        entry = Entry(self.canvas, textvariable=self.controller.brackets[name]["entries"][ind])
                        entry.pack()
                        ind += 1
                        self.canvas.create_window(80 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=entry)

                    elif type == "edit":
                        self.labels[ind] = Label(self.canvas, text=self.controller.brackets[name]["entries"][ind].get())
                        self.labels[ind].bind("<Button-1>", functools.partial(self.advance, ind=ind))
                        self.labels[ind].pack()
                        self.canvas.create_window(80 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=self.labels[ind])
                        if ind >= end:
                            end = ((ind + 1) / 2) - 1
                            ind = (ind + 1) / 4
                            ind -= 1
                        ind += 1


                if (r % 2 ** (c + 1) == 0) and (c < cols - 1):
                    self.canvas.create_line(10 + (140 * (c + 1)), 30 + (30 * r) + 15 * (sum), 10 + (140 * (c + 1)),
                                            30 + (30 * r) + 15 * (sum + (2 ** (c + 1))))


        if type == "edit" or type == "entry":
            button = Button(self.canvas, text="Submit")
            button.bind("<Button-1>", self.submit_entries)
            button.pack()
            self.canvas.create_window(800, 15, window=button)


        self.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def submit_entries(self, event):
        if self.type == "entry":
            for i in range(len(self.labels)):
                self.controller.brackets[self.name]["actual"][i] = self.controller.brackets[self.name]["entries"][i]

        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()

    def advance(self, event, ind):
        if ind != 1:
            self.labels[int(math.floor(ind / 2))]["text"] = self.labels[ind]["text"]
            self.controller.brackets[self.name]["entries"][int(math.floor(ind / 2))] = StringVar(value=self.labels[ind]["text"])


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
        createTeam = Create_Tournament(parent=self.parent, controller=self.controller)
        createTeam.grid(row=0, column=0, sticky="nsew")
        createTeam.tkraise()

    def load_tourney(self, event):
        loadTeam = Load_Bracket(parent=self.parent, controller=self.controller)
        loadTeam.grid(row=0, column=0, sticky="nsew")
        loadTeam.tkraise()


class Create_Tournament(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        Label(self, text="Bracket Name:").grid(sticky="w")
        self.name = StringVar()
        entry1 = Entry(self, textvariable=self.name)
        entry1.grid(row=0, column=1)

        Label(self, text="Draw size:").grid(row=1, column=0, sticky="w")
        self.numTeams = IntVar()
        entry2 = Combobox(self, textvariable=self.numTeams)
        entry2['values'] = [2,4,8,16,32,64,128]
        entry2.grid(row=1, column=1)

        Label(self, text="Number of Seeds:").grid(row=2, column=0, sticky="w")
        self.numSeeds = IntVar()
        entry3 = Combobox(self, textvariable=self.numSeeds)
        entry3.grid(row=2, column=1)

        button = Button(self, text="Done")
        button.bind("<Button-1>", self.done_button)
        button.grid()

    def done_button(self, event):
        self.controller.brackets[self.name.get()] = {}
        self.controller.brackets[self.name.get()]["numTeams"] = self.numTeams
        self.controller.brackets[self.name.get()]["numSeeds"] = self.numSeeds
        self.controller.brackets[self.name.get()]["entries"] = []
        for i in range(2 * self.numTeams.get()):
            self.controller.brackets[self.name.get()]["entries"].append(StringVar(value=""))

        self.controller.brackets[self.name.get()]["actual"] = []
        for i in range(2 * self.numTeams.get()):
            self.controller.brackets[self.name.get()]["actual"].append(StringVar(value=""))

        self.controller.home.tkraise()


class Load_Bracket(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.team = StringVar()
        self.box = Combobox(self, textvariable=self.team)
        self.box.bind("<<ComboboxSelected>>", self.select)
        teams = []
        for key in self.controller.brackets:
            teams.append(key)

        self.box['values'] = teams
        self.box.grid()

    def select(self, event):
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.team.get())
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()


class Bracket_Home(tk.Frame):

    def __init__(self, parent, controller, name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.numTeams = self.controller.brackets[name]["numTeams"]
        self.numSeeds = self.controller.brackets[name]["numSeeds"]
        self.entries = [StringVar()] * (self.numTeams.get() * 2)
        self.actual = [StringVar()] * (self.numTeams.get() * 2)

        button1 = Button(self, text="Create/Edit Original Draw")
        button1.bind("<Button-1>", self.create_button)
        button1.grid()

        button2 = Button(self, text="Make Picks")
        button2.bind("<Button-1>", self.make_button)
        button2.grid()

        button3 = Button(self, text="View Picks")
        button3.bind("<Button-1>", self.view_button)
        button3.grid()

    def create_button(self, event):
        self.create = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams.get() , type="entry",
                              name=self.name)
        self.create.grid(row=0, column=0, sticky="nsew")
        self.create.tkraise()
    def make_button(self, event):
        self.make = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams.get() , type="edit",
                            name=self.name)
        self.make.grid(row=0, column=0, sticky="nsew")
        self.make.tkraise()

    def view_button(self, event):
        self.view = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams.get(), type="view",
                            name=self.name)
        self.view.grid(row=0, column=0, sticky="nsew")
        self.view.tkraise()



if __name__ == "__main__":
    app = App()
    app.mainloop()