from tkinter import *
from view import view_constants as vc
from util.multiline_label import MultilineLabel


class HomeFrame(Frame):

    def __init__(self, **kw):
        super().__init__(**kw)

        label_headline = Label(master=self, text='Home', font=vc.HEADER_FONT)
        label_headline.pack()

        info_text = """This is a long sample text.\nLorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."""
        label_info = MultilineLabel(master=self, font=vc.TEXT_FONT, padx=10, pady=10)
        label_info.setText(info_text)
        label_info.pack()

