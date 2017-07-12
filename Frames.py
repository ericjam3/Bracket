from Tkinter import *

def raise_frame(frame):
    frame.tkraise()

def donothing():
    print ""

def balls(event):
    print "Holy Cat balls"

root = Tk()

f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

Label(f1, text="FRAME 1").pack()
Button(f1, text="Go to frame 2", command=lambda:raise_frame(f2)).pack()

Label(f2, text="FRAME 2").pack()
Button(f2, text="Go to frame 3", command=lambda:raise_frame(f3)).pack()

Label(f3, text="FRAME 3").pack()
Button(f3, text="Go to frame 4", command=lambda:raise_frame(f4)).pack()

Label(f4, text="FRAME 4").pack()
Button(f4, text="Go to frame 1", command=lambda:raise_frame(f1)).pack()

label = Label(f1, text="Touch Me")
label.bind("<Button-1>", balls)
label.pack()


menubar = Menu(root)
teammenu = Menu(menubar, tearoff=0)
teammenu.add_command(label="Select Team", command = donothing)
teammenu.add_command(label="Add Team", command = donothing)
teammenu.add_command(label="Remove Team", command = donothing)

menubar.add_cascade(label="Team", menu=teammenu)

playermenu = Menu(menubar, tearoff=0)
playermenu.add_command(label="Select Player", command = donothing)
playermenu.add_command(label="Add Player", command = donothing)
playermenu.add_command(label="Remove Player", command = donothing)

menubar.add_cascade(label="Player", menu=playermenu)
root.config(menu=menubar)
raise_frame(f1)
root.mainloop()
