from Tkinter import *
import tkMessageBox
import Tkinter

def create_frames(Qdict, root):
    Qdict["Murray"] = Frame(root)
    Qdict["Nadal"] = Frame(root)
    Qdict["Federer"] = Frame(root)
    Qdict["Djokovic"] = Frame(root)



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


if __name__ == "__main__":
    root = Tk()
  #  Qdict = {}
    create_menus(root)
    #create_frames(Qdict, root)

    root.mainloop()