from Tkinter import *
import tkMessageBox
import Tkinter as tk
import math
from ttk import *
import ttk
import functools
from random import *

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

        self.leagues = {}
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
        infile = open("leagueDB.txt", "r")
        lineNum = 0
        num_entries = 0
        for item in infile:
            line = item[0:-1]
            if lineNum == 0:
                info = line.split("  ")
                name = info[0]
                self.brackets[name] = {}
                self.brackets[name]["numTeams"] = int(info[1])
                self.brackets[name]["edit"] = int(info[2])
                self.brackets[name]["entries"] = {}
                self.brackets[name]["actual"] = []
                num_entries = int(info[3])
                num_picks = int(info[4])
                self.brackets[name]["num_picks"] = num_picks
                if num_picks > 0:
                    lineNum = 1
                else:
                    lineNum = 3
                    self.brackets[name]["actual"].append(StringVar(value=""))
                temp_entries = num_entries
            elif lineNum == 1:
                picks_name = line
                self.brackets[name]["entries"][picks_name] = []
                self.brackets[name]["entries"][picks_name].append(StringVar(value=""))
                lineNum = 2
            elif lineNum == 2:
                temp_entries -= 1
                if temp_entries == 0:
                    num_picks -= 1
                    if num_picks == 0:
                        temp_entries = num_entries
                        lineNum = 3
                        self.brackets[name]["actual"].append(StringVar(value=""))
                    else:
                        temp_entries = num_entries
                        lineNum = 1

                self.brackets[name]["entries"][picks_name].append(StringVar(value=line))

            elif lineNum == 3:
                temp_entries -= 1
                if temp_entries == 0:
                    lineNum = 0

                self.brackets[name]["actual"].append(StringVar(value=line))
        infile.close()

    def save(self):
        print_var = ""
        for key, value in self.brackets.iteritems():
            print_var += key + "  " + str(value["numTeams"]) + "  " + str(value["edit"]) + "  "
            print_var += str(len(value["actual"]) - 1) + "  " + str(value["num_picks"]) + "\n"
            for entry in value["entries"]:
                print_var += entry + "\n"
                for i in range(1, len(value["entries"][entry]), 1):
                    print_var += str(value["entries"][entry][i].get()) + "\n"

            for i in range(1, len(value["actual"]), 1):
                print_var += str(value["actual"][i].get()) + "\n"

        outfile = open("leagueDB.txt", "w")
        outfile.write(print_var)
        outfile.close()


class Bracket(tk.Frame):

    def __init__(self, parent, controller, numTeams, type, name, Lname):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.type = type
        self.Lname = Lname
        self.numTeams = numTeams

        # Determining how many rounds (columns) there will be
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
        wrongo = {}

        for c in range(cols):
            prev = sum
            if c != 0:
                sum = 2 ** (c - 1) + prev
            for r in range(rows):
                if r % 2 ** c == 0:
                    self.canvas.create_line(10 + (c * 140), 30 + (30 * r) + 15 * (sum), 10 + (c + 1) * 140,
                                            30 + (30 * r) + 15 * (sum))
                    if type == "view":
                        if draw == "actual":
                            team = self.controller.brackets[name][draw][ind].get()
                        else:
                            team = self.controller.brackets[name][draw][picks][ind].get()
                        if len(team) > 0 and team[0].isalpha():
                            team = "".ljust(4) + team
                        label = Label(self.canvas, text=team, font="bold")
                        if draw == "entries":
                            # Color coordination and scoring for correct picks
                            if (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() != ""
                                and self.controller.brackets[name]["entries"][picks][ind].get() ==
                                self.controller.brackets[name]["actual"][ind].get()):

                                score += ppp
                                label["background"] = "spring green"

                            # Color coordination for incorrect picks
                            if c > 0 and self.controller.brackets[name]["entries"][picks][ind].get() in wrongo:
                                label["background"] = "tomato"
                            elif (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() != ""
                                and self.controller.brackets[name]["entries"][picks][ind].get() !=
                                self.controller.brackets[name]["actual"][ind].get()):
                                wrongo[self.controller.brackets[name]["entries"][picks][ind].get()] = 1
                                label["background"] = "tomato"


                        label.pack()
                        self.canvas.create_window(30 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=SW, window=label)
                        if ind >= end:
                            end = ((ind + 1) / 2) - 1
                            ind = (ind + 1) / 4
                            ind -= 1
                        ind += 1

                    elif type == "entry" and c == 0:
                        entry = Entry(self.canvas, textvariable=self.controller.brackets[name]["actual"][ind])
                        entry.pack()
                        ind += 1
                        self.canvas.create_window(80 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=entry)

                    elif type == "edit":
                        if draw == "actual":
                            team = self.controller.brackets[name][draw][ind].get()
                        else:
                            team = self.controller.brackets[name][draw][picks][ind].get()
                        if len(team) > 0 and team[0].isalpha():
                            team = "".ljust(4) + team
                        self.labels[ind] = Label(self.canvas, text=team, font="bold")
                        self.labels[ind].bind("<Button-1>", functools.partial(self.advance, ind=ind))
                        self.labels[ind].pack()
                        self.canvas.create_window(30 + (c * 140), 25 + (30 * r) + 15 * (sum),
                                                  anchor=SW, window=self.labels[ind])
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


        if type == "view" and draw != "actual":
            l = Label(self.canvas, text="Score:", font="bold")
            l.pack()
            self.canvas.create_window(600, 15, window=l)
            scoreLabel = Label(self.canvas, text=str(score) + " / " + str(numTeams * 5 * (cols - 1)), font="bold")
            scoreLabel.pack()
            self.canvas.create_window(600, 40, window=scoreLabel)
        if type == "edit" or type == "entry":
            button = Button(self.canvas, text="Submit")
            button.bind("<Button-1>", functools.partial(self.submit_entries, rando=0))
            button.pack()
            self.canvas.create_window(800, 15, window=button)
            if type == "entry":
                lbl = Label(self.canvas, text="Enter the rest of the teams to be placed randomly")
                lbl.pack()
                button2 = Button(self.canvas, text="Randomize")
                button2.bind("<Button-1>", functools.partial(self.submit_entries, rando=1))
                button2.pack()
                self.canvas.create_window(800, 40, window=button2)
                self.canvas.create_window(850, 40, window= lbl, anchor="w")
        else:
            button = Button(self.canvas, text="Done Viewing")
            button.bind("<Button-1>", functools.partial(self.submit_entries, rando=0))
            button.pack()
            self.canvas.create_window(800, 15, window=button)

        self.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    def submit_entries(self, event, rando):
        if self.type == "entry":
            for i in range(len(self.labels) - self.numTeams, len(self.labels), 1):
                if self.controller.brackets[self.name]["actual"][i].get() == StringVar(value="").get():
                    self.controller.brackets[self.name]["actual"][i] = StringVar(value="BYE")

                for pick in self.controller.brackets[self.name]["entries"]:
                    self.controller.brackets[self.name]["entries"][pick][i] = self.controller.brackets[self.name]["actual"][i]

            for i in range(len(self.labels) - 1, 2, -2):
                if ((self.controller.brackets[self.name]["actual"][i].get() !=
                    self.controller.brackets[self.name]["actual"][int(math.floor(i/2))].get()) and
                   (self.controller.brackets[self.name]["actual"][i - 1].get() !=
                    self.controller.brackets[self.name]["actual"][int(math.floor(i / 2))].get())):
                    self.controller.brackets[self.name]["actual"][int(math.floor(i / 2))] = StringVar(value="")

            for pick in self.controller.brackets[self.name]["entries"]:
                for i in range(len(self.labels) - 1, 2, -2):
                    if ((self.controller.brackets[self.name]["entries"][pick][i].get() !=
                        self.controller.brackets[self.name]["entries"][pick][int(math.floor(i/2))].get()) and
                       (self.controller.brackets[self.name]["entries"][pick][i - 1].get() !=
                        self.controller.brackets[self.name]["entries"][pick][int(math.floor(i / 2))].get())):
                        self.controller.brackets[self.name]["entries"][pick][int(math.floor(i / 2))] = StringVar(value="")

        self.controller.save()
        if rando == 1:
            rFrame = Random_Frame(parent=self.parent, controller=self.controller, name=self.name)
            rFrame.grid(row=0, column=0, sticky="nsew")
            rFrame.tkraise()
        else:
            bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
            bhome.grid(row=0, column=0, sticky="nsew")
            bhome.tkraise()

    def advance(self, event, ind):
        picks = self.picks
        if ind != 1:
            self.labels[int(math.floor(ind / 2))]["text"] = self.labels[ind]["text"]
            if self.draw == "actual":
                self.controller.brackets[self.name][self.draw][int(math.floor(ind / 2))] = StringVar(
                    value=self.labels[ind]["text"])
            else:
                self.controller.brackets[self.name][self.draw][picks][int(math.floor(ind / 2))] = StringVar(
                    value=self.labels[ind]["text"])

            while ind > 3:
                ind = int(math.floor(ind / 2))
                pair = ind + 1
                if ind % 2 == 1:
                    pair -= 2

                if self.draw == "actual":
                    if ((self.controller.brackets[self.name][self.draw][int(math.floor(ind / 2))].get() !=
                        self.controller.brackets[self.name][self.draw][ind].get()) and
                        (self.controller.brackets[self.name][self.draw][int(math.floor(ind / 2))].get() !=
                        self.controller.brackets[self.name][self.draw][pair].get())):
                        self.controller.brackets[self.name][self.draw][int(math.floor(ind / 2))] = StringVar(value="")
                        self.labels[int(math.floor(ind / 2))]["text"] = ""
                else:
                    if ((self.controller.brackets[self.name][self.draw][picks][int(math.floor(ind / 2))].get() !=
                        self.controller.brackets[self.name][self.draw][picks][ind].get()) and
                        (self.controller.brackets[self.name][self.draw][picks][int(math.floor(ind / 2))].get() !=
                        self.controller.brackets[self.name][self.draw][picks][pair].get())):
                        self.controller.brackets[self.name][self.draw][picks][int(math.floor(ind / 2))] = StringVar(value="")
                        self.labels[int(math.floor(ind / 2))]["text"] = ""

        self.controller.save()

    def mouse(self, event):
        self.canvas.yview_scroll(-1 * (event.delta / 120), "units")


class Random_Frame(tk.Frame):

    def __init__(self, parent, controller, name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.teams = []

        Button(self, text="Submit", command=self.pressed).grid()

        self.byes = []
        row = 3
        col = 0
        for i in range(len(self.controller.brackets[name]["entries"])):
            if self.controller.brackets[name]["entries"][i].get() == "BYE":
                entry = Entry(self)
                entry.grid(row=row, column=col, padx=5, pady=5)
                row += 1
                if row > 18:
                    row = 3
                    col += 1
                self.teams.append(entry)
                self.byes.append(i)

    def pressed(self):
        for i in range(len(self.byes) - 1, -1, -1):
            ind = randint(0, i)
            ind = self.byes.pop(ind)
            if self.teams[i].get() != "":
                self.controller.brackets[self.name]["entries"][ind] = StringVar(value=self.teams[i].get())
                self.controller.brackets[self.name]["actual"][ind] = StringVar(value=self.teams[i].get())
            else:
                self.controller.brackets[self.name]["entries"][ind] = StringVar(value="BYE")
                self.controller.brackets[self.name]["actual"][ind] = StringVar(value="BYE")

        self.controller.save()
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()

# Updated
class Create_Tournament(tk.Frame):

    def __init__(self, parent, controller, Lname):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.Lname = Lname

        Label(self, text="Bracket Name: ").grid(sticky="w")
        self.name = StringVar()
        entry1 = Entry(self, textvariable=self.name)
        entry1.grid(row=0, column=1, sticky="we")

        Label(self, text="Draw size: ").grid(row=1, column=0, sticky="w")
        self.numTeams = IntVar()
        entry2 = Combobox(self, textvariable=self.numTeams)
        entry2['values'] = [2,4,8,16,32,64,128]
        entry2.grid(row=1, column=1, sticky="we")

        Label(self, text="Number of seeds: ").grid(row=2, column=0, sticky="w")
        self.numSeeds = IntVar()
        entry3 = Entry(self, textvariable=self.numSeeds)
        entry3.grid(row=2, column=1, sticky="we")

        button = Button(self, text="Done")
        button.bind("<Button-1>", self.done_button)
        button.grid()

    def done_button(self, event):
        self.controller.leagues["Brackets"][self.name.get()] = {}
        self.controller.leagues["Brackets"][self.name.get()]["numSeeds"] = 0
        self.controller.leagues["Brackets"][self.name.get()]["numTeams"] = self.numTeams.get()
        self.controller.leagues["Brackets"][self.name.get()]["actual"] = []

        for i in range(2 * self.numTeams.get()):
            self.controller.leagues["Brackets"][self.name.get()]["actual"].append(StringVar(value=""))

        self.controller.save()
        self.create = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams.get() , type="entry",
                              name=self.name.get(), Lname=self.Lname)
        self.create.grid(row=0, column=0, sticky="nsew")
        self.create.tkraise()


class Bracket_Home(tk.Frame):

    def __init__(self, parent, controller, name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.numTeams = self.controller.brackets[name]["numTeams"]
        self.entries = [StringVar()] * (self.numTeams * 2)
        self.actual = [StringVar()] * (self.numTeams * 2)

        Label(self, text=name, font="Bold 36").grid(padx=10)

        button1 = Button(self, text="Edit Original Draw")
        button1.bind("<Button-1>", self.create_button)
        button1.grid(sticky="we", row=0, column=1)

        button8 = Button(self, text="Create New Picks")
        button8.bind("<Button-1>", self.create_picks)
        button8.grid(sticky="we", row=0, column=2)

        button4 = Button(self, text="Update Live Draw")
        button4.bind("<Button-1>", self.live_draw)
        button4.grid(sticky="we", row=0, column=3)

        button5 = Button(self, text="View Live Draw")
        button5.bind("<Button-1>", self.view_live)
        button5.grid(sticky="we", row=0, column=4)

        if self.controller.brackets[name]["edit"] == 1:
            button6 = Button(self, text="Close editing")
            button6.bind("<Button-1>", self.close)
            button6.grid(sticky="we", row=0, column=5)
        else:
            button7 = Button(self, text="Open editing")
            button7.bind("<Button-1>", self.open)
            button7.grid(sticky="we", row=0, column=5)


        leaderboard = {}
        backup = {}
        noPicks = 1
        for pick in self.controller.brackets[name]["entries"]:
            noPicks = 0
            score = 0
            points = 10 * self.numTeams / 2
            next = 2
            for i in range(1, self.numTeams, 1):
                if i >= next:
                    next *= 2
                    points /= 2
                if (self.controller.brackets[name]["entries"][pick][i].get() != "" and
                    self.controller.brackets[name]["entries"][pick][i].get() ==
                    self.controller.brackets[name]["actual"][i].get()):
                    score += points
            leaderboard[pick] = score
            backup[pick] = score
        if (noPicks == 0):
            self.brackets = []
            for i in range(len(backup)):
                max = -1
                place = ""
                for pick in leaderboard:
                    if leaderboard[pick] > max:
                        max = leaderboard[pick]
                        place = pick
                self.brackets.append(place)
                del leaderboard[place]

            Label(self, text="BRACKET:").grid(row=2, padx=10)
            Label(self, text="SCORE:").grid(row=2, column=1, padx=10)
            for i in range(len(self.brackets)):
                label = Label(self, text=self.brackets[i], foreground="blue")
                if self.controller.brackets[name]["edit"] == 0:
                    Label(self, text=str(backup[self.brackets[i]])).grid(row=i+3, column=1)
                    label.bind("<Button-1>", self.view_button)
                else:
                    Label(self, text="0").grid(row=i + 3, column=1)
                    label.bind("<Button-1>", self.make_button)
                label.grid(row=i+3)
                self.brackets.append(label)

    def create_button(self, event):
        self.create = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams , type="entry",
                              name=self.name, draw="entries")
        self.create.grid(row=0, column=0, sticky="nsew")
        self.create.tkraise()
    def make_button(self, event):
        self.make = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams , type="edit",
                            name=self.name, draw="entries", picks=event.widget["text"])
        self.make.grid(row=0, column=0, sticky="nsew")
        self.make.tkraise()

    def view_button(self, event):
        self.view = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams, type="view",
                            name=self.name, draw="entries", picks=event.widget["text"])
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

    def close(self, event):
        self.controller.brackets[self.name]["edit"] = 0
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        self.controller.save()
        bhome.tkraise()
    def open(self, event):
        self.controller.brackets[self.name]["edit"] = 1
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        self.controller.save()
        bhome.tkraise()

    def create_picks(self, event):
        create = Create_Picks(parent=self.parent, controller=self.controller, name=self.name)
        create.grid(row=0, column=0, sticky="nsew")
        self.controller.save()
        create.tkraise()


class Create_Picks(tk.Frame):
    def __init__(self, parent, controller, name):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.numTeams = self.controller.brackets[name]["numTeams"]

        Label(self, text="Name of Picks: ").grid()
        self.entry = Entry(self)
        self.entry.grid(row=0, sticky="we", column=1)

        button = Button(self, text="Submit")
        button.bind("<Button-1>", self.submit)
        button.grid(sticky="we")

    def submit(self, event):
        self.controller.brackets[self.name]["entries"][self.entry.get()] = []

        for i in range(2 * self.numTeams):
            if i < self.numTeams:
                self.controller.brackets[self.name]["entries"][self.entry.get()].append(StringVar(value=""))
            else:
                self.controller.brackets[self.name]["entries"][self.entry.get()].append(
                    self.controller.brackets[self.name]["actual"][i])

        self.controller.brackets[self.name]["num_picks"] += 1
        self.controller.save()
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()


######################### Below is for League Classes, above is Tournament ###############################

class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        # Create league button
        self.create = Button(self, text="Create League")
        self.create.bind("<Button-1>", self.create_league)
        self.create.grid(sticky="we", columnspan=2)

        # Load league button
        Label(self, text="Select League: ").grid()
        self.league = StringVar()
        self.box = Combobox(self, textvariable=self.league)
        self.box.bind("<<ComboboxSelected>>", self.load_league)
        leagues = []
        for key in self.controller.leagues:
            leagues.append(key)

        self.box['values'] = leagues
        self.box.grid(row=1, column=1)

    def create_league(self, event):
        createLeague = Create_League(parent=self.parent, controller=self.controller)
        createLeague.grid(row=0, column=0, sticky="nsew")
        createLeague.tkraise()

    def load_league(self, event):
        loadTeam = League_Home(parent=self.parent, controller=self.controller, Lname=self.league)
        loadTeam.grid(row=0, column=0, sticky="nsew")
        loadTeam.tkraise()


class League_Home(tk.Frame):

    def __init__(self, parent, controller, Lname):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.Lname = Lname

        Label(self, text=Lname, font=36).grid()
        # Add players button
        button = Button(self, text="Add players")
        button.bind("<Button-1>", self.add)
        button.grid(sticky="we")

        # Create bracket button
        self.create = Button(self, text="Create Tournament")
        self.create.bind("<Button-1>", self.create_tourney)
        self.create.grid(sticky="we")

        # Load bracket button
        Label(self, text="Select Tournament: ").grid()
        self.tourney = StringVar()
        self.box = Combobox(self, textvariable=self.tourney)
        self.box.bind("<<ComboboxSelected>>", self.load_tourney)
        tourneys = []
        for key in self.controller.leagues[Lname]["Brackets"]:
            tourneys.append(key)

        self.box['values'] = tourneys
        self.box.grid(row=3, column=1)

    def create_tourney(self, event):
        createTeam = Create_Tournament(parent=self.parent, controller=self.controller, Lname=self.Lname)
        createTeam.grid(row=0, column=0, sticky="nsew")
        createTeam.tkraise()

    def load_tourney(self, event):
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.tourney.get())
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()

    def add(self, event):
        loadTeam = Add_Players(parent=self.parent, controller=self.controller, Lname=self.Lname)
        loadTeam.grid(row=0, column=0, sticky="nsew")
        loadTeam.tkraise()


class Create_League(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        Label(self, text="Name of League: ").grid()
        self.Lname = StringVar()
        self.entry = Entry(self, textvariable=self.Lname).grid(row=0, column=1)
        button = Button(self, text="Submit")
        button.bind("<Button-1>", self.pressed)
        button.grid()

    def pressed(self, event):
        self.controller.leagues[self.Lname.get()] = {}
        self.controller.leagues[self.Lname.get()]["rankings"] = {}
        self.controller.leagues[self.Lname.get()]["rankings"]["official"] = {}
        self.controller.leagues[self.Lname.get()]["numPlayers"] = 0
        self.controller.leagues[self.Lname.get()]["numBrackets"] = 0
        self.controller.leagues[self.Lname.get()]["numGames"] = 0
        self.controller.leagues[self.Lname.get()]["Players"] = {}
        self.controller.leagues[self.Lname.get()]["Brackets"] = {}
        self.controller.leagues[self.Lname.get()]["Games"] = {}

        loadTeam = League_Home(parent=self.parent, controller=self.controller, Lname=self.Lname.get())
        loadTeam.grid(row=0, column=0, sticky="nsew")
        loadTeam.tkraise()


class Add_Players(tk.Frame):
    def __init__(self, parent, controller, Lname):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.Lname = Lname

        Label(self, text="Number of players to add: ").grid()
        self.numPlayers = IntVar()
        self.entry = Entry(self)
        button = Button(self, text="Ready")
        button.bind("<Button-1>", self.add)
        button.grid()

    def add(self, event):
        self.players = []
        for i in range(self.numPlayers.get()):
            entry = Entry(self).grid(pady=5)
            self.players.append(entry)

        button = Button(self, text="Submit")
        button.bind("<Button-1>", self.submit)
        button.grid()

    def submit(self, event):
        for i in range(self.numPlayers.get()):
            pname = self.players[i]["text"].get()
            if pname != "":
                self.controller.leagues[self.Lname]["numPlayers"] += 1
                self.controller.leagues[self.Lname]["Players"][pname] = {}
                self.controller.leagues[self.Lname]["rankings"]["official"] = (
                    self.controller.leagues[self.Lname]["numPlayers"])

        loadTeam = League_Home(parent=self.parent, controller=self.controller, Lname=self.Lname)
        loadTeam.grid(row=0, column=0, sticky="nsew")
        loadTeam.tkraise()







if __name__ == "__main__":
    app = App()
    app.mainloop()