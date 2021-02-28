from functools import partial
from tkinter import *
from PIL import ImageTk, Image as PIL_Image

from tkinter import filedialog
from download.model import DownloadModel

HEADER_FONT = "Roboto 20 bold"
TEXT_FONT = "Roboto 12"


class DownloadPage(Frame):
    def __init__(self, master, init_model):
        super().__init__(master, bg='cyan')

        # --

        header = Label(self, text='Downloads', bg='cyan', font=HEADER_FONT)
        header.grid(row=0, sticky=W)

        # --

        _input = Frame(self, bg='blue')
        _input.grid(row=1, pady=10)

        self.input_entry = Entry(_input)
        self.input_entry.grid(row=0, column=0)

        self.input_btn = Button(_input, text='search')
        self.input_btn.grid(row=0, column=1, sticky=W)

        # --

        info = Frame(self, bg='blue')
        info.grid(row=2, pady=10)

        self.info_title = Label(info, text='<title>', font=TEXT_FONT)
        self.info_title.grid(row=0, column=0, sticky=W)

        self.info_artist = Label(info, text='<artist>', font=TEXT_FONT)
        self.info_artist.grid(row=1, column=0, sticky=W)

        self.info_tags = Label(info, text='<tag1>, <tag2>...', font=TEXT_FONT, wraplength=300, justify='left')
        self.info_tags.grid(row=2, column=0, sticky=W)

        self.info_page_count = Label(info, text='24', font=TEXT_FONT)
        self.info_page_count.grid(row=3, column=0, sticky=W)

        # 250w x 328h
        image = ImageTk.PhotoImage(PIL_Image.open('thumb.jpg').resize((250, 350), PIL_Image.ANTIALIAS))
        self.info_cover = Label(info, image=image, bg='red', width=250, height=325)
        self.info_cover.grid(row=0, column=1, rowspan=4, sticky=E)

        # --

        dir_select = Frame(self, bg='blue')
        dir_select.grid(row=3, pady=10)

        self.dir_select_entry_text = StringVar()
        self.dir_select_entry = Entry(dir_select, state='disabled', textvariable=self.dir_select_entry_text)
        self.dir_select_entry.grid(row=0, column=0, sticky=E)

        def open_dir_dialog():
            path = filedialog.askdirectory()
            print(f"path selected {path}")
            self.dir_select_entry_text.set(path)

        self.dir_select_btn = Button(dir_select, text='change', command=open_dir_dialog)
        self.dir_select_btn.grid(row=0, column=1, sticky=W)

        self.updateView(init_model)

    def __setTitle(self, title):
        self.info_title.config(text=title)

    def __setArtist(self, artist):
        self.info_artist.config(text=artist)

    def __setTags(self, tags):
        self.info_tags.config(text=', '.join(tags))

    def __setPageCount(self, count):
        self.info_page_count.config(text=count)

    def __setImage(self, path):
        if path is not None:
            image = ImageTk.PhotoImage(PIL_Image.open(path).resize((250, 350), PIL_Image.ANTIALIAS))
            self.info_cover.config(image=image)

    def getInput(self):
        return self.input_entry.get()

    def getDirectoryPath(self):
        return self.dir_select_entry.get()

    def updateView(self, model: DownloadModel):
        self.__setTitle(model.title)
        self.__setArtist(model.artist)
        self.__setTags(model.tags)
        self.__setPageCount(model.page_count)
        self.__setImage(model.image_path)

    def set_input_button_action(self, action):
        def wrapper_function():
            action(self.getInput())

        self.input_btn.config(command=wrapper_function)

