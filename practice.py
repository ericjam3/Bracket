from Tkinter import *
import tkMessageBox
import Tkinter as tk
import math
from ttk import *
import ttk
import functools


def func():
    for i in range(len(list)):
        print list[i].get()

root = Tk()
button = Button(root, text="submit", command=func).pack()

list = []
for i in range(5):
    entry = Entry(root)
    entry.pack()
    list.append(entry)




root.mainloop()