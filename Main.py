from Tkinter import *
import tkMessageBox
import Tkinter

def set_frame(frame, size):
    print "Work on this"

# Creating the menu at the top of the window
def create_menus(root):
    menudict = {}
    menubar = Menu(root)
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

    root.config(menu=menubar)
    return menubar

if __name__ == "__main__":
    root = Tk()

    half = Frame(root)
    full = Frame(root)
    menubar = create_menus(root)
    raw = Menu(menubar, tearoff=0)

    root.title('Bracket App')
    root.mainloop()