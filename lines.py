from Tkinter import *
import tkMessageBox
import Tkinter

def func():
    print ""

root = Tk()
scrollbar = Scrollbar(root)
canvas = Canvas(root, yscrollcommand = scrollbar.set)
scrollbar.config( command = canvas.yview )
scrollbar.pack(side=RIGHT, fill=Y)
frame = Frame(canvas)
canvas.pack(side="left", fill="both", expand=True)

canvas.create_window(0,0,window=frame,anchor="nw")

# First round
for i in range(32):
    canvas.create_line(10,30*i + 30,150,30*i + 30)

for i in range(31):
    if i % 2 == 0:
        canvas.create_line(150, 30*i + 30,150,30*i + 60)

# Second round
for i in range(32):
    if i % 2 == 0:
        canvas.create_line(150,30*i + 45,290,30*i + 45)

for i in range(31):
    if i % 4 == 0:
        canvas.create_line(290, 30*i + 45,290,30*i + 105)

# Third round
for i in range(32):
    if i % 4 == 0:
        canvas.create_line(290,30*i + 75,430,30*i + 75)

for i in range(31):
    if i % 8 == 0:
        canvas.create_line(430, 30*i + 75,430,30*i + 195)

# Fourth round
for i in range(32):
    if i % 8 == 0:
        canvas.create_line(430,30*i + 135,570,30*i + 135)

for i in range(31):
    if i % 16 == 0:
        canvas.create_line(570, 30*i + 135,570,30*i + 375)

# Fifth round
for i in range(32):
    if i % 16 == 0:
        canvas.create_line(570,30*i + 255,710,30*i + 255)

for i in range(31):
    if i % 32 == 0:
        canvas.create_line(710, 30*i + 255,710,30*i + 735)

canvas.create_line(710,495 ,850,495
                   )

root.update()
canvas.config(scrollregion=canvas.bbox("all"))


w = Canvas(root, width=200, height=100)
f1 = Frame(w)
w.pack()

w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

w.create_rectangle(50, 25, 150, 75, fill="blue")
frame.destroy()
#w.create_window(0,0,window=frame,anchor="nw")


root.mainloop()