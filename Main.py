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
        self.container = container


        menubar = Menu(self)
        M = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=M)
        m1 = Menu(menubar, tearoff=0)
        M.add_command(label="Home", command=self.home_button)

        self.config(menu=menubar)

        self.brackets = {}
        self.load()

        self.home = Home(parent=container, controller=self)
        self.home.grid(row=0, column=0, sticky="nsew")
        self.home.tkraise()

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_name):
        return self.frames[page_name]

    def home_button(self):
        self.home = Home(parent=self.container, controller=self)
        self.home.grid(row=0, column=0, sticky="nsew")
        self.home.tkraise()


    def load(self):
        infile = open("database.txt", "r")
        lineNum = 0
        num_entries = 0
        for item in infile:
            line = item[0:-1]
            if lineNum == 0:
                info = line.split("  ")
                name = info[0]
                self.brackets[name] = {}
                self.brackets[name]["numTeams"] = int(info[1])
                self.brackets[name]["numSeeds"] = int(info[2])
                self.brackets[name]["entries"] = []
                self.brackets[name]["actual"] = []
                num_entries = int(info[3])
                if num_entries > 0:
                    lineNum = 1
                    self.brackets[name]["entries"].append(StringVar(value=""))
                    temp_entries = num_entries
            elif lineNum == 1:
                temp_entries -= 1
                if temp_entries == 0:
                    temp_entries = num_entries
                    lineNum = 2
                    self.brackets[name]["actual"].append(StringVar(value=""))

                self.brackets[name]["entries"].append(StringVar(value=line))

            elif lineNum == 2:
                temp_entries -= 1
                if temp_entries == 0:
                    lineNum = 0

                self.brackets[name]["actual"].append(StringVar(value=line))


        infile.close()

    def save(self):
        print_var = ""
        for key, value in self.brackets.iteritems():
            print_var += key + "  " + str(value["numTeams"]) + "  " + str(value["numSeeds"]) + "  "
            print_var += str(len(value["entries"]) - 1) + "\n"
            for i in range(1, len(value["entries"]), 1):
                 print_var += str(value["entries"][i].get()) + "\n"

            for i in range(1, len(value["actual"]), 1):
                print_var += str(value["actual"][i].get()) + "\n"

        outfile = open("database.txt", "w")
        outfile.write(print_var)
        outfile.close()


class Bracket(tk.Frame):

    def __init__(self, parent, controller, numTeams, type, name, draw):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.type = type
        self.draw = draw
        self.numTeams = numTeams

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
        self.canvas.bind_all("<MouseWheel>", self.mouse)

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
        score = 0
        ppp = 10

        for c in range(cols):
            prev = sum
            if c != 0:
                sum = 2 ** (c - 1) + prev
            for r in range(rows):
                if r % 2 ** c == 0:
                    self.canvas.create_line(10 + (c * 140), 30 + (30 * r) + 15 * (sum), 10 + (c + 1) * 140,
                                            30 + (30 * r) + 15 * (sum))
                    if type == "view":
                        label = Label(self.canvas, text=self.controller.brackets[name][draw][ind].get(), font="bold")
                        # Color coordination and scoring for correct picks
                        if (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() != ""
                            and self.controller.brackets[name]["entries"][ind].get() ==
                            self.controller.brackets[name]["actual"][ind].get()):

                            score += ppp
                            label["background"] = "spring green"

                        # Color coordination for incorrect picks
                        elif (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() != ""
                            and self.controller.brackets[name]["entries"][ind].get() !=
                            self.controller.brackets[name]["actual"][ind].get()):

                            label["background"] = "tomato"

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
                        self.labels[ind] = Label(self.canvas, text=self.controller.brackets[name][draw][ind].get(), font="bold")
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

            if c > 0:
                ppp *= 2


        if type == "view":
            l = Label(self.canvas, text="Score:", font="bold")
            l.pack()
            self.canvas.create_window(600, 15, window=l)
            scoreLabel = Label(self.canvas, text=str(score) + " / " + str(numTeams * 5 * (cols - 1)), font="bold")
            scoreLabel.pack()
            self.canvas.create_window(600, 40, window=scoreLabel)
        if type == "edit" or type == "entry":
            button = Button(self.canvas, text="Submit")
            button.bind("<Button-1>", self.submit_entries)
            button.pack()
            self.canvas.create_window(800, 15, window=button)
        else:
            button = Button(self.canvas, text="Done Viewing")
            button.bind("<Button-1>", self.submit_entries)
            button.pack()
            self.canvas.create_window(800, 15, window=button)

        self.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def submit_entries(self, event):
        if self.type == "entry":
            for i in range(len(self.labels) - self.numTeams, len(self.labels), 1):
                self.controller.brackets[self.name]["actual"][i] = self.controller.brackets[self.name]["entries"][i]

        self.controller.save()
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()

    def advance(self, event, ind):
        if ind != 1:
            self.labels[int(math.floor(ind / 2))]["text"] = self.labels[ind]["text"]
            self.controller.brackets[self.name][self.draw][int(math.floor(ind / 2))] = StringVar(value=self.labels[ind]["text"])
        self.controller.save()

    def mouse(self, event):
        self.canvas.yview_scroll(-1 * (event.delta / 120), "units")


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        # Create bracket button
        Label(self, text="Bracket City", font=36).grid()
        self.create = Button(self, text="Create Tournament")
        self.create.bind("<Button-1>", self.create_tourney)
        self.create.grid(sticky="we")

        # Load bracket button
        self.load = Button(self, text="Load Tournament")
        self.load.bind("<Button-1>", self.load_tourney)
        self.load.grid(sticky="we")

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
        entry1.grid(row=0, column=1, sticky="w")

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
        self.controller.brackets[self.name.get()]["numTeams"] = self.numTeams.get()
        self.controller.brackets[self.name.get()]["numSeeds"] = self.numSeeds.get()
        self.controller.brackets[self.name.get()]["entries"] = []
        for i in range(2 * self.numTeams.get()):
            self.controller.brackets[self.name.get()]["entries"].append(StringVar(value=""))
        self.controller.brackets[self.name.get()]["actual"] = []
        for i in range(2 * self.numTeams.get()):
            self.controller.brackets[self.name.get()]["actual"].append(StringVar(value=""))

        self.controller.save()
        self.controller.home.tkraise()


class Load_Bracket(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        Label(self, text="Select a bracket from the dropdown below:").grid()
        self.team = StringVar()
        self.box = Combobox(self, textvariable=self.team)
        self.box.bind("<<ComboboxSelected>>", self.select)
        teams = []
        for key in self.controller.brackets:
            teams.append(key)

        self.box['values'] = teams
        self.box.grid(sticky="we")

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
        self.entries = [StringVar()] * (self.numTeams * 2)
        self.actual = [StringVar()] * (self.numTeams * 2)

        Label(self, text=name, font="Bold 36").grid()

        button1 = Button(self, text="Create/Edit Original Draw")
        button1.bind("<Button-1>", self.create_button)
        button1.grid(sticky="we")

        button2 = Button(self, text="Make Picks")
        button2.bind("<Button-1>", self.make_button)
        button2.grid(sticky="we")

        button3 = Button(self, text="View Picks")
        button3.bind("<Button-1>", self.view_button)
        button3.grid(sticky="we")

        button4 = Button(self, text="Update Live Draw")
        button4.bind("<Button-1>", self.live_draw)
        button4.grid(sticky="we")

        button5 = Button(self, text="View Live Draw")
        button5.bind("<Button-1>", self.view_live)
        button5.grid(sticky="we")

    def create_button(self, event):
      #  tempList = []
       # for i in range(2 * self.numTeams.get()):
       #     tempList.append(StringVar(value=""))
       # self.controller.brackets[self.name]["entries"].append(tempList)
        self.create = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams , type="entry",
                              name=self.name, draw="entries")
        self.create.grid(row=0, column=0, sticky="nsew")
        self.create.tkraise()
    def make_button(self, event):
        self.make = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams , type="edit",
                            name=self.name, draw="entries")
        self.make.grid(row=0, column=0, sticky="nsew")
        self.make.tkraise()

    def view_button(self, event):
        self.view = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams, type="view",
                            name=self.name, draw="entries")
        self.view.grid(row=0, column=0, sticky="nsew")
        self.view.tkraise()

    def live_draw(self, event):
        self.live_entry = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams, type="edit",
                            name=self.name, draw="actual")
        self.live_entry.grid(row=0, column=0, sticky="nsew")
        self.live_entry.tkraise()

    def view_live(self, event):
        self.view_live = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams,
                                  type="view",
                                  name=self.name, draw="actual")
        self.view_live.grid(row=0, column=0, sticky="nsew")
        self.view_live.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()