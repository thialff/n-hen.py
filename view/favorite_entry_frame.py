from tkinter import *


class FavoriteEntryFrame(Frame):

    def __init__(self, digits: str, name: str, **kw):
        super().__init__(**kw)
        label_digits = Label(master=self, text=digits, width=8, anchor=E, bg=self['bg'])
        label_digits.grid(row=0, column=0)

        label_name = Label(master=self, text=f'- "{name}"', anchor=W, bg=self['bg'])
        label_name.grid(row=0, column=1, sticky=W)

        self.columnconfigure(1, weight=1)
