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

        outfile = open("database.txt", "w")
        outfile.write(print_var)
        outfile.close()


class Bracket(tk.Frame):

    def __init__(self, parent, controller, numTeams, type, name, draw, picks="NONE"):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.name = name
        self.type = type
        self.draw = draw
        self.numTeams = numTeams
        self.picks = picks

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
        ppr = 0
        ppp = 10
        wrongo = {}
        round_num = 2

        for c in range(cols):
            prev = sum
            current_points = 0
            if c != 0:
                sum = 2 ** (c - 1) + prev
            for r in range(rows):
                if r % 2 ** c == 0:
                    self.canvas.create_line(10 + (c * 140), 120 + (30 * r) + 15 * (sum), 10 + (c + 1) * 140,
                                            120 + (30 * r) + 15 * (sum))
                    if type == "view":
                        if draw == "actual":
                            team = self.controller.brackets[name][draw][ind].get()
                        else:
                            team = self.controller.brackets[name][draw][picks][ind].get()
                        if len(team) > 0 and team[0].isalpha():
                            team = "".ljust(4) + team
                        label = Label(self.canvas, text=team, font="none, 8")
                        if draw == "entries":
                            # Color coordination and scoring for correct picks
                            if (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() != ""
                                and self.controller.brackets[name]["entries"][picks][ind].get() ==
                                self.controller.brackets[name]["actual"][ind].get()):

                                score += ppp
                                current_points += ppp
                                label["background"] = "spring green"

                            # Color coordination for incorrect picks
                            if c > 0 and self.controller.brackets[name]["entries"][picks][ind].get() in wrongo:
                                label["background"] = "tomato"
                            elif (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() != ""
                                and self.controller.brackets[name]["entries"][picks][ind].get() !=
                                self.controller.brackets[name]["actual"][ind].get()):
                                wrongo[self.controller.brackets[name]["entries"][picks][ind].get()] = 1
                                label["background"] = "tomato"

                            # Points remaining calculation
                            if (c > 0 and draw == "entries" and self.controller.brackets[name]["actual"][ind].get() == ""
                                and self.controller.brackets[name]["entries"][picks][ind].get() not in wrongo):
                                ppr += ppp


                        label.pack()
                        self.canvas.create_window(11 + (c * 140), 115 + (30 * r) + 15 * (sum),
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
                        self.canvas.create_window(80 + (c * 140), 115 + (30 * r) + 15 * (sum),
                                                  anchor=S, window=entry)

                    elif type == "edit":
                        if draw == "actual":
                            team = self.controller.brackets[name][draw][ind].get()
                        else:
                            team = self.controller.brackets[name][draw][picks][ind].get()
                        if len(team) > 0 and team[0].isalpha():
                            team = "".ljust(4) + team
                        self.labels[ind] = Label(self.canvas, text=team, font="bold, 8")
                        self.labels[ind].bind("<Button-1>", functools.partial(self.advance, ind=ind))
                        self.labels[ind].pack()
                        self.canvas.create_window(30 + (c * 140), 115 + (30 * r) + 15 * (sum),
                                                  anchor=SW, window=self.labels[ind])
                        if ind >= end:
                            end = ((ind + 1) / 2) - 1
                            ind = (ind + 1) / 4
                            ind -= 1
                        ind += 1


                if (r % 2 ** (c + 1) == 0) and (c < cols - 1):
                    self.canvas.create_line(10 + (140 * (c + 1)), 120 + (30 * r) + 15 * (sum), 10 + (140 * (c + 1)),
                                            120 + (30 * r) + 15 * (sum + (2 ** (c + 1))))

            if c > 0 and type == "view" and draw != "actual":
                ppp *= 2
                if round_num == cols - 3:
                    round = "Quarters:"
                elif round_num == cols - 2:
                    round = "Semis:"
                elif round_num == cols - 1:
                    round = "Finals:"
                elif round_num == cols:
                    round = "Champion:"
                else:
                    round = "Round " + str(round_num) + ":"

                l2 = Label(self.canvas, text=round)
                l2.pack()
                self.canvas.create_window(65 + (c * 140), 15, window=l2)
                slabel = Label(self.canvas, text=str(current_points) + " / " + str(numTeams * 5))
                slabel.pack()
                self.canvas.create_window(65 + (c * 140), 40, window=slabel)
                round_num += 1

        if draw == "actual":
            nameLabel = Label(self.canvas, text="OFFICIAL", font="Bold 16")
            nameLabel.pack()
            self.canvas.create_window(5, 10, window=nameLabel, anchor="w")
        else:
            nameLabel = Label(self.canvas, text=picks, font="Bold 16")
            nameLabel.pack()
            self.canvas.create_window(5, 10, window=nameLabel, anchor="w")

        if type == "view" and draw != "actual":
            l = Label(self.canvas, text="Score:", font="Bold 10")
            l.pack()
            self.canvas.create_window(35, 30, window=l)
            scoreLabel = Label(self.canvas, text=str(score) + " / " + str(numTeams * 5 * (cols - 1)), font="Bold 10")
            scoreLabel.pack()
            self.canvas.create_window(35, 50, window=scoreLabel)

            l1 = Label(self.canvas, text="PPR:", font="bold 10")
            l1.pack()
            self.canvas.create_window(100, 30, window=l1)
            pprLabel = Label(self.canvas, text=str(ppr), font="bold 10")
            pprLabel.pack()
            self.canvas.create_window(100, 50, window=pprLabel)
        if type == "edit" or type == "entry":
            button = Button(self.canvas, text="Submit")
            button.bind("<Button-1>", functools.partial(self.submit_entries, rando=0))
            button.pack()
            self.canvas.create_window(40, 75, window=button)
        else:
            button = Button(self.canvas, text="Done")
            button.bind("<Button-1>", functools.partial(self.submit_entries, rando=0))
            button.pack()
            self.canvas.create_window(40, 75, window=button)

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
                if ((self.controller.brackets[self.name]["actual"][i].get().lstrip() !=
                    self.controller.brackets[self.name]["actual"][int(math.floor(i/2))].get().lstrip()) and
                   (self.controller.brackets[self.name]["actual"][i - 1].get().lstrip() !=
                    self.controller.brackets[self.name]["actual"][int(math.floor(i / 2))].get().lstrip())):
                    self.controller.brackets[self.name]["actual"][int(math.floor(i / 2))] = StringVar(value="")

            for pick in self.controller.brackets[self.name]["entries"]:
                for i in range(len(self.labels) - 1, 2, -2):
                    if ((self.controller.brackets[self.name]["entries"][pick][i].get().lstrip() !=
                        self.controller.brackets[self.name]["entries"][pick][int(math.floor(i/2))].get().lstrip()) and
                       (self.controller.brackets[self.name]["entries"][pick][i - 1].get().lstrip() !=
                        self.controller.brackets[self.name]["entries"][pick][int(math.floor(i / 2))].get().lstrip())):
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


class Home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        # Create bracket button
        self.create = Button(self, text="Create Tournament")
        self.create.bind("<Button-1>", self.create_tourney)
        self.create.grid(sticky="we", columnspan=2)

        Label(self, text="").grid()
        # Load bracket button
        Label(self, text="Select Tournament: ").grid()
        self.tourney = StringVar()
        self.box = Combobox(self, textvariable=self.tourney)
        self.box.bind("<<ComboboxSelected>>", self.load_tourney)
        tourneys = []
        for key in self.controller.brackets:
            tourneys.append(key)

        self.box['values'] = tourneys
        self.box.grid(row=2, column=1)

        Label(self, text="").grid()
        # Delete bracket button
        Label(self, text="Delete Tournament: ").grid()
        self.dtourney = StringVar()
        self.dbox = Combobox(self, textvariable=self.dtourney)
        self.dbox.bind("<<ComboboxSelected>>", self.delete_tourney)
        self.dbox['values'] = tourneys
        self.dbox.grid(row=4, column=1)

    def create_tourney(self, event):
        self.destroy()
        createTeam = Create_Tournament(parent=self.parent, controller=self.controller)
        createTeam.grid(row=0, column=0, sticky="nsew")
        createTeam.tkraise()

    def load_tourney(self, event):
        self.destroy()
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.tourney.get())
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()

    def delete_tourney(self, event):
        button1 = Button(self, text="Delete " + self.dtourney.get())
        button1.bind("<Button-1>", self.delete)
        button1.grid()

        button2 = Button(self, text="Just Kidding")
        button2.bind("<Button-1>", self.jk)
        button2.grid()

    def delete(self, event):
        del self.controller.brackets[self.dtourney.get()]
        self.controller.save()
        self.destroy()
        self.home = Home(parent=self.parent, controller=self.controller)
        self.home.grid(row=0, column=0, sticky="nsew")
        self.home.tkraise()

    def jk(self, event):
        self.destroy()
        self.home = Home(parent=self.parent, controller=self.controller)
        self.home.grid(row=0, column=0, sticky="nsew")
        self.home.tkraise()


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


class Create_Tournament(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        Label(self, text="Bracket Name:").grid(sticky="w")
        self.name = StringVar()
        entry1 = Entry(self, textvariable=self.name)
        entry1.grid(row=0, column=1, sticky="we")

        Label(self, text="Draw size:").grid(row=1, column=0, sticky="w")
        self.numTeams = IntVar()
        entry2 = Combobox(self, textvariable=self.numTeams)
        entry2['values'] = [2,4,8,16,32,64,128]
        entry2.grid(row=1, column=1, sticky="we")

        button = Button(self, text="Done")
        button.bind("<Button-1>", self.done_button)
        button.grid()

    def done_button(self, event):
        self.controller.brackets[self.name.get()] = {}
        self.controller.brackets[self.name.get()]["edit"] = 1
        self.controller.brackets[self.name.get()]["numTeams"] = self.numTeams.get()
        self.controller.brackets[self.name.get()]["entries"] = {}
        self.controller.brackets[self.name.get()]["actual"] = []
        self.controller.brackets[self.name.get()]["num_picks"] = 0

        for i in range(2 * self.numTeams.get()):
            self.controller.brackets[self.name.get()]["actual"].append(StringVar(value=""))

        self.controller.save()
        self.create = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams.get() , type="entry",
                              name=self.name.get(), draw="actual")
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

        # Delete picks button
        Label(self, text="Delete Picks: ").grid(row=0, column=6)
        self.dpicks = StringVar()
        self.dbox = Combobox(self, textvariable=self.dpicks)
        self.dbox.bind("<<ComboboxSelected>>", self.delete_picks)
        picks = []
        for key in self.controller.brackets[self.name]["entries"]:
            picks.append(key)

        self.dbox['values'] = picks
        self.dbox.grid(row=0, column=7)


        leaderboard = {}
        backup = {}
        # Just in case there are no picks to present (don't want it to bomb out)
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

        pprs = {}
        for pick in self.controller.brackets[name]["entries"]:
            wrongo = {}
            ppr = 0
            points = 10
            next = (self.controller.brackets[name]["numTeams"] / 2) - 1
            for i in range(self.controller.brackets[name]["numTeams"] - 1, 0, -1):
                if i == next:
                    points *= 2
                    next = (next - 1) / 2
                if (self.controller.brackets[name]["entries"][pick][i].get() !=
                        self.controller.brackets[name]["actual"][i].get() and
                        self.controller.brackets[name]["actual"][i].get() != ""):
                    wrongo[self.controller.brackets[name]["entries"][pick][i].get()] = 1
                elif self.controller.brackets[name]["actual"][i].get() == "" and (
                        self.controller.brackets[name]["entries"][pick][i].get() not in wrongo):
                    ppr += points

            pprs[pick] = ppr

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

            Label(self, text="BRACKET:").grid(row=2, padx=10, column=1)
            if self.controller.brackets[name]["edit"] == 0:
                Label(self, text="SCORE:").grid(row=2, column=2, padx=10)
                Label(self, text="RANK:").grid(row=2, column=0, sticky="E")
                Label(self, text="PPR:").grid(row=2, column=3, padx=10)
            rank = 1
            for i in range(len(self.brackets)):
                label = Label(self, text=self.brackets[i], foreground="blue")
                if self.controller.brackets[name]["edit"] == 0:
                    Label(self, text=str(backup[self.brackets[i]])).grid(row=i+3, column=2)
                    if i != 0 and (backup[self.brackets[i]] != backup[self.brackets[i-1]]):
                        rank = i + 1

                    Label(self, text=str(rank) + "    ").grid(row=i+3, column=0, sticky="E")
                    Label(self, text=str(pprs[self.brackets[i]])).grid(row=i+3, column=3)
                    label.bind("<Button-1>", self.view_button)
                else:
                    label.bind("<Button-1>", self.make_button)
                label.grid(row=i+3, column=1)
                self.brackets.append(label)

    def create_button(self, event):
        self.create = Bracket(parent=self.parent, controller=self.controller, numTeams=self.numTeams , type="entry",
                              name=self.name, draw="actual")
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

    def delete_picks(self, event):
        button1 = Button(self, text="Delete " + self.dpicks.get())
        button1.bind("<Button-1>", self.delete)
        button1.grid(row=1, column=7)

        button2 = Button(self, text="Just Kidding")
        button2.bind("<Button-1>", self.jk)
        button2.grid(row=2, column=7)

    def delete(self, event):
        del self.controller.brackets[self.name]["entries"][self.dpicks.get()]
        self.controller.brackets[self.name]["num_picks"] -= 1
        self.controller.save()
        self.destroy()
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()

    def jk(self, event):
        self.destroy()
        bhome = Bracket_Home(parent=self.parent, controller=self.controller, name=self.name)
        bhome.grid(row=0, column=0, sticky="nsew")
        bhome.tkraise()



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

if __name__ == "__main__":
    app = App()
    app.mainloop()