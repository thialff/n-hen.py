from tkinter import *
from view.download_frame import DownloadFrame


MENU_WIDTH = 75


class MainFrame(Tk):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.geometry('700x600')

        # sidebar
        menu_frame = Frame(master=self, width=MENU_WIDTH)
        menu_frame.pack_propagate(0)
        menu_frame.pack(fill=Y, side=LEFT)

        frame_1 = Frame(master=menu_frame, height=MENU_WIDTH)
        frame_1.propagate(0)
        frame_1.pack(fill=X)
        btn_1 = Button(master=frame_1, text='Home')
        btn_1.pack(fill=BOTH, expand=1)

        frame_2 = Frame(master=menu_frame, height=MENU_WIDTH)
        frame_2.propagate(0)
        frame_2.pack(fill=X)
        btn_2 = Button(master=frame_2, text='Download')
        btn_2.pack(fill=BOTH, expand=1)

        frame_3 = Frame(master=menu_frame, height=MENU_WIDTH)
        frame_3.propagate(0)
        frame_3.pack(fill=X)
        btn_3 = Button(master=frame_3, text='Favorites')
        btn_3.pack(fill=BOTH, expand=1)

        # display frame
        display_frame = Frame(master=self)
        display_frame.pack_propagate(0)
        display_frame.pack(expand=True, fill=BOTH, side=LEFT)

        # navigation
        self.download_panel = DownloadFrame(master=display_frame)
        self.download_panel.pack()

        self.mainloop()
