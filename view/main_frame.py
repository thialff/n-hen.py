from enum import Enum
from tkinter import *
from view.download_frame import DownloadFrame
from view.home_frame import HomeFrame
from view.favorties_frame import FavoritesFrame
from view.settings_frame import SettingsFrame

MENU_WIDTH = 75


class Navigation(Enum):
    HOME = 1
    DOWNLOAD = 2
    FAVORITES = 3
    SETTINGS = 4


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
        btn_1 = Button(master=frame_1, text='Home', command=lambda: self.navigate(Navigation.HOME))
        btn_1.pack(fill=BOTH, expand=1)

        frame_2 = Frame(master=menu_frame, height=MENU_WIDTH)
        frame_2.propagate(0)
        frame_2.pack(fill=X)
        btn_2 = Button(master=frame_2, text='Download', command=lambda: self.navigate(Navigation.DOWNLOAD))
        btn_2.pack(fill=BOTH, expand=1)

        frame_3 = Frame(master=menu_frame, height=MENU_WIDTH)
        frame_3.propagate(0)
        frame_3.pack(fill=X)
        btn_3 = Button(master=frame_3, text='Favorites', command=lambda: self.navigate(Navigation.FAVORITES))
        btn_3.pack(fill=BOTH, expand=1)

        frame_4 = Frame(master=menu_frame, height=MENU_WIDTH)
        frame_4.propagate(0)
        frame_4.pack(fill=X)
        btn_4 = Button(master=frame_4, text='Settings', command=lambda: self.navigate(Navigation.SETTINGS))
        btn_4.pack(fill=BOTH, expand=1)

        # display frame
        display_frame = Frame(master=self)
        display_frame.pack_propagate(0)
        display_frame.pack(expand=True, fill=BOTH, side=LEFT)

        # navigation
        self.home_frame = HomeFrame(master=display_frame)
        self.download_frame = DownloadFrame(master=display_frame)
        self.favorites_frame = FavoritesFrame(master=display_frame)
        self.settings_frame = SettingsFrame(master=display_frame)

        self.navigate(Navigation.HOME)

        self.mainloop()

    def navigate(self, destination: Navigation):
        if destination not in list(Navigation):
            return

        self.home_frame.pack_forget()
        self.download_frame.pack_forget()
        self.favorites_frame.pack_forget()
        self.settings_frame.pack_forget()

        if destination == Navigation.HOME:
            self.home_frame.pack(fill=X)
        elif destination == Navigation.DOWNLOAD:
            self.download_frame.pack(expand=True, fill=BOTH, side=LEFT)
        elif destination == Navigation.FAVORITES:
            self.favorites_frame.pack(fill=X)
        elif destination == Navigation.SETTINGS:
            self.settings_frame.pack(fill=X)
