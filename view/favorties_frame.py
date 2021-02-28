from tkinter import *
from view import view_constants as vc


class FavoritesFrame(Frame):

    def __init__(self, **kw):
        super().__init__(**kw)

        label_headline = Label(master=self, text='Favorites', font=vc.HEADER_FONT)
        label_headline.pack()
