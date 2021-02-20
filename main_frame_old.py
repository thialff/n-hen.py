from tkinter import *
from enum import Enum

from download.view import DownloadPage
from download.model import DownloadModel

import n_util

HEADER_FONT = "Roboto 20 bold"
TEXT_FONT = "Roboto 12"


class Destination(Enum):
    HOME = 1
    DOWNLOADS = 2
    FAVORITES = 3
    SETTINGS = 4


root = Tk()
root.title("n-hen.py")
root.geometry('{}x{}'.format(1000, 600))


def clear_navigation_frame():
    return 0


def nav_to_home():
    page_downloads.grid_forget()
    page_home.grid(row=0, column=1, sticky=E + N, padx=20, pady=20)
    print("nav to home")


def nav_to_downloads():
    page_home.grid_forget()
    page_downloads.grid(row=0, column=1, sticky=E + N, padx=20, pady=20)
    print("nav to downloads")


# navigation
navigation = Frame(root, bg="red", width=100)
navigation.grid(column=0, sticky=W + N)
navigation.pack_propagate(False)

btn_nav_home = Button(navigation, text='home', command=nav_to_home)
btn_nav_downloads = Button(navigation, text='downloads', command=nav_to_downloads)

btn_nav_home.grid(row=0)
btn_nav_downloads.grid(row=1)

# content

# frame
page_frame = Frame(root, bg='cyan', width=600, height=400)
page_frame.grid(row=0, column=1, sticky=E + N, padx=20, pady=20)

# home
page_home = Frame(page_frame, bg='cyan', width=400, height=400)

ph_header = Label(page_home, text='Home', bg='cyan', font=HEADER_FONT)
ph_header.grid(row=0)


def search(user_input: str):
    n_digit = n_util.parse_to_n_digit(user_input)
    n_entry = n_util.get_n_entry(n_digit)
    if n_entry is not None:
        download_model.setTitle(n_entry.digits)
        download_model.setArtist(n_entry.gallery_id)
        download_model.setPageCount(n_entry.page_count)
        download_model.setTags(n_entry.image_url_list)
        page_downloads.updateView(download_model)


download_model = DownloadModel()
page_downloads = DownloadPage(page_frame, download_model)
page_downloads.input_entry.insert(0, '144725')
page_downloads.set_input_button_action(search)

root.mainloop()
