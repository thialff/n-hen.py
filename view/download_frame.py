import threading
from time import sleep
from tkinter import *
from tkinter import filedialog

from PIL import ImageTk, Image
from view import view_constants as vc
import os
from urllib.request import urlopen
import io
from util import dir_util as du, n_download_util as ndu, n_util


class DownloadFrame(Frame):

    def __init__(self, **kw):
        super().__init__(**kw)

        # model
        self.n_entry = None
        # --

        label_headline = Label(master=self, text='Downloads', font=vc.HEADER_FONT)
        label_headline.pack()

        frame_digit_entry = Frame(master=self)
        frame_digit_entry.pack()

        self.entry_digits = Entry(master=frame_digit_entry)
        self.entry_digits.grid(column=0, row=0, columnspan=2)

        self.button_digits = Button(master=frame_digit_entry, text='Search')
        self.button_digits.grid(column=2, row=0)

        frame_info = Frame(master=self)
        frame_info.pack()

        frame_info_left = Frame(master=frame_info)
        frame_info_left.pack(side=LEFT)

        self.thumbnail = Image.open('thumb.jpg').resize((200, 300), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(self.thumbnail)
        self.label_image_info = Label(master=frame_info_left, image=self.thumbnail, width=200, height=300)
        self.label_image_info.pack()

        frame_info_right = Frame(master=frame_info)
        frame_info_right.pack(side=TOP)

        label_name = Label(master=frame_info_right, text='Name', font=vc.LABEL_FONT)
        label_name.grid(row=0, column=0, sticky=W)
        label_digits = Label(master=frame_info_right, text='Digits', font=vc.LABEL_FONT)
        label_digits.grid(row=1, column=0, sticky=W)
        label_artists = Label(master=frame_info_right, text='Artists', font=vc.LABEL_FONT)
        label_artists.grid(row=2, column=0, sticky=W)
        label_tags = Label(master=frame_info_right, text='Tags', font=vc.LABEL_FONT)
        label_tags.grid(row=3, column=0, sticky=W)
        label_pages = Label(master=frame_info_right, text='Pages', font=vc.LABEL_FONT)
        label_pages.grid(row=4, column=0, sticky=W)

        self.label_name_value = Label(master=frame_info_right, width=35, text='Nekopara', anchor=W, font=vc.TEXT_FONT)
        self.label_name_value.grid(row=0, column=1, columnspan=2, sticky=W)
        self.label_digits_value = Label(master=frame_info_right, width=35, text='144725', anchor=W, font=vc.TEXT_FONT)
        self.label_digits_value.grid(row=1, column=1, columnspan=2, sticky=W)
        self.label_artists_value = Label(master=frame_info_right, width=35, text='sayori', anchor=W, font=vc.TEXT_FONT,
                                         wraplength=200)
        self.label_artists_value.grid(row=2, column=1, columnspan=2, sticky=W)
        self.label_tags_value = Label(master=frame_info_right, width=35, text='nekomini, maid, 2girls', anchor=W,
                                      font=vc.TEXT_FONT, wraplength=300)
        self.label_tags_value.grid(row=3, column=1, columnspan=2, sticky=W)
        self.label_pages_value = Label(master=frame_info_right, width=35, text='24', anchor=W, font=vc.TEXT_FONT)
        self.label_pages_value.grid(row=4, column=1, columnspan=2, sticky=W)

        # ---

        frame_directory = Frame(master=self)
        frame_directory.pack(fill=X)

        self.entry_directory_value = StringVar()
        self.entry_directory_value.set(os.path.join(os.getcwd(), 'saves'))
        entry_directory = Entry(master=frame_directory, state=DISABLED, textvariable=self.entry_directory_value)
        entry_directory.grid(row=0, column=0, columnspan=2, sticky='ew')

        label_separator = Label(master=frame_directory, text=os.path.sep, font=vc.TEXT_FONT)
        label_separator.grid(row=0, column=2)

        self.entry_file_name_value = StringVar()
        entry_file_name = Entry(master=frame_directory, state=DISABLED, textvariable=self.entry_file_name_value)
        entry_file_name.grid(row=0, column=3)

        self.btn_choose_dir = Button(master=frame_directory, text='Choose')
        self.btn_choose_dir.grid(row=0, column=4)

        frame_directory.grid_columnconfigure(0, weight=1)
        # ---

        frame_download = Frame(master=self)
        frame_download.pack()

        self.btn_download = Button(master=frame_download, text='Download')
        self.btn_download.pack()

        self.label_status_value = StringVar()
        self.label_status_value.set('')
        self.label_status = Label(master=frame_download, textvariable=self.label_status_value, anchor=E)
        self.label_status.pack()

        self.setSearchButtonCommand(lambda: onSearch(self))
        self.setChooseDirButtonCommand(lambda: onChoose(self))
        self.setDownloadButtonCommand(lambda: onDownload(self))

        self.pack_propagate(0)

    def updateDownloadView(self, entry: n_util.NEntry):
        self.label_name_value.configure(text=entry.title)
        self.label_digits_value.configure(text=entry.digits)
        self.label_artists_value.configure(text=', '.join(entry.artists))
        self.label_tags_value.configure(text=', '.join(entry.tags))
        self.label_pages_value.configure(text=entry.page_count)

        raw_data = urlopen(entry.cover_url).read()

        self.thumbnail = Image.open(io.BytesIO(raw_data)).resize((200, 300), Image.ANTIALIAS)
        self.thumbnail = ImageTk.PhotoImage(self.thumbnail)
        self.label_image_info.configure(image=self.thumbnail)

        self.entry_file_name_value.set(entry.digits)

    def setSearchButtonCommand(self, command):
        self.button_digits.configure(command=command)

    def setDownloadButtonCommand(self, command):
        self.btn_download.configure(command=command)

    def setChooseDirButtonCommand(self, command):
        self.btn_choose_dir.configure(command=command)

    def setStatusLabelText(self, text: str):
        self.label_status_value.set(text)
        self.label_status.update_idletasks()

    def setStatusLabelTextAsProgress(self, current, total):
        if current <= total:
            self.setStatusLabelText(f'Downloading... {current}/{total}')
            if current == total:
                sleep(1)
                self.setStatusLabelText('')


def onSearch(download_panel: DownloadFrame):
    print('onSearch')
    digits = n_util.parse_to_n_digit(download_panel.entry_digits.get())
    if digits is None:
        return
    download_panel.n_entry = n_util.get_n_entry(digits)
    print(download_panel.n_entry)
    download_panel.updateDownloadView(download_panel.n_entry)


def onDownload(download_panel: DownloadFrame):
    print('onDownload')
    if download_panel.n_entry is None:
        return
    du.create_dir_if_not_exists(download_panel.entry_directory_value.get())
    save_dir = os.path.join(download_panel.entry_directory_value.get(), download_panel.entry_file_name_value.get())
    du.create_dir_if_not_exists(save_dir)
    t = threading.Thread(target=ndu.save_files_to_dir,
                         kwargs=dict(file_url_list=download_panel.n_entry.image_url_list, path=save_dir,
                                     update=download_panel.setStatusLabelTextAsProgress, thread_count=8), daemon=True)
    t.start()


def onChoose(download_panel: DownloadFrame):
    current_dir_name = download_panel.entry_directory_value.get()
    du.create_dir_if_not_exists(current_dir_name)
    print('onChoose')
    filename = filedialog.askdirectory(initialdir=current_dir_name, mustexist=True)
    print(f'directory with path {filename} selected')
    if len(filename) != 0:
        download_panel.entry_directory_value.set(filename)
