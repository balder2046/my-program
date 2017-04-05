#!/usr/bin/python
# coding = utf-8
from tkinter import *
root = Tk()
frame = Frame(root, bd=2, relief=SUNKEN)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Text(frame, bd=0)
listbox.pack()
for i in range(1,100):
    listbox.insert(END,"%d\n" % i)


scrollbar.config(command=listbox.yview)

frame.pack()
root.mainloop()