from tkinter import *

root = Tk()
label = Label(root, text="Hello World")
label.grid(row=0, column=0)
label2 = Label(root, text="My second label")
label2.grid(row=1, column=1)

root.mainloop()
