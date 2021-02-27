import io
import os
from time import sleep
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from urllib.request import urlopen
import dir_util as du
import n_download_util as ndu

import n_util

MENU_WIDTH = 75

label_font = "Roboto 12 bold"

text_font = "Roboto 12"

root = Tk()
root.geometry('700x600')

# sidebar
menu_frame = Frame(master=root, width=MENU_WIDTH)
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

# --

n_entry = None

display_frame = Frame(master=root)
display_frame.pack_propagate(0)
display_frame.pack(expand=True, fill=BOTH, side=LEFT)

label_headline = Label(master=display_frame, text='Downloads')
label_headline.pack()

frame_digit_entry = Frame(master=display_frame)
frame_digit_entry.pack()

entry_digits = Entry(master=frame_digit_entry)
entry_digits.grid(column=0, row=0, columnspan=2)

button_digits = Button(master=frame_digit_entry, text='Search')
button_digits.grid(column=2, row=0)

frame_info = Frame(master=display_frame)
frame_info.pack()

frame_info_left = Frame(master=frame_info)
frame_info_left.pack(side=LEFT)

thumbnail = Image.open('thumb.jpg').resize((200, 300), Image.ANTIALIAS)
thumbnail = ImageTk.PhotoImage(thumbnail)
label_image_info = Label(master=frame_info_left, image=thumbnail, width=200, height=300)
label_image_info.pack()

frame_info_right = Frame(master=frame_info)
frame_info_right.pack(side=TOP)

label_name = Label(master=frame_info_right, text='Name', font=label_font)
label_name.grid(row=0, column=0, sticky=W)
label_digits = Label(master=frame_info_right, text='Digits', font=label_font)
label_digits.grid(row=1, column=0, sticky=W)
label_artists = Label(master=frame_info_right, text='Artists', font=label_font)
label_artists.grid(row=2, column=0, sticky=W)
label_tags = Label(master=frame_info_right, text='Tags', font=label_font)
label_tags.grid(row=3, column=0, sticky=W)
label_pages = Label(master=frame_info_right, text='Pages', font=label_font)
label_pages.grid(row=4, column=0, sticky=W)

label_name_value = Label(master=frame_info_right, width=35, text='Nekopara', anchor=W, font=text_font)
label_name_value.grid(row=0, column=1, columnspan=2, sticky=W)
label_digits_value = Label(master=frame_info_right, width=35, text='144725', anchor=W, font=text_font)
label_digits_value.grid(row=1, column=1, columnspan=2, sticky=W)
label_artists_value = Label(master=frame_info_right, width=35, text='sayori', anchor=W, font=text_font, wraplength=200)
label_artists_value.grid(row=2, column=1, columnspan=2, sticky=W)
label_tags_value = Label(master=frame_info_right, width=35, text='nekomini, maid, 2girls', anchor=W, font=text_font, wraplength=300)
label_tags_value.grid(row=3, column=1, columnspan=2, sticky=W)
label_pages_value = Label(master=frame_info_right, width=35, text='24', anchor=W, font=text_font)
label_pages_value.grid(row=4, column=1, columnspan=2, sticky=W)

# ---

frame_directory = Frame(master=display_frame)
frame_directory.pack(fill=X)

entry_directory_value = StringVar()
entry_directory_value.set(os.path.join(os.getcwd(), 'saves'))
entry_directory = Entry(master=frame_directory, state=DISABLED, textvariable=entry_directory_value)
entry_directory.grid(row=0, column=0, columnspan=2, sticky='ew')

label_separator = Label(master=frame_directory, text=os.path.sep, font=text_font)
label_separator.grid(row=0, column=2)

entry_file_name_value = StringVar()
entry_file_name = Entry(master=frame_directory, state=DISABLED, textvariable=entry_file_name_value)
entry_file_name.grid(row=0, column=3)

btn_choose_dir = Button(master=frame_directory, text='Choose')
btn_choose_dir.grid(row=0, column=4)

frame_directory.grid_columnconfigure(0, weight=1)
# ---

frame_download = Frame(master=display_frame)
frame_download.pack()

btn_download = Button(master=frame_download, text='Download')
btn_download.pack()

label_status_value = StringVar()
label_status_value.set('')
label_status = Label(master=frame_download, textvariable=label_status_value, anchor=E)
label_status.pack()


def updateDownloadView(entry: n_util.NEntry):
    label_name_value.configure(text=entry.title)
    label_digits_value.configure(text=entry.digits)
    label_artists_value.configure(text=', '.join(entry.artists))
    label_tags_value.configure(text=', '.join(entry.tags))
    label_pages_value.configure(text=entry.page_count)

    raw_data = urlopen(entry.cover_url).read()
    global thumbnail
    thumbnail = Image.open(io.BytesIO(raw_data)).resize((200, 300), Image.ANTIALIAS)
    thumbnail = ImageTk.PhotoImage(thumbnail)
    label_image_info.configure(image=thumbnail)

    entry_file_name_value.set(entry.digits)


def onSearch():
    print('onSearch')
    digits = n_util.parse_to_n_digit(entry_digits.get())
    if digits is None:
        return
    global n_entry
    n_entry = n_util.get_n_entry(digits)
    print(n_entry)
    updateDownloadView(n_entry)


def updateStatusLabel(current, total):
    label_status_value.set(f'Downloading... {current}/{total}')
    global label_status
    label_status.update_idletasks()
    if current == total:
        sleep(1)
        label_status_value.set('')
        label_status.update_idletasks()


def onDownload():
    print('onDownload')
    global n_entry
    if n_entry is None:
        return
    du.create_dir_if_not_exists(entry_directory_value.get())
    save_dir = os.path.join(entry_directory_value.get(), entry_file_name_value.get())
    du.create_dir_if_not_exists(save_dir)
    global label_status_value
    ndu.save_files_to_dir(n_entry.image_url_list, save_dir, updateStatusLabel)


def onChoose():
    print('onChoose')
    filename = filedialog.askdirectory(initialdir=os.path.join(os.getcwd(), 'saves'))
    print(f'directory with path {filename} selected')
    global entry_directory_value
    entry_directory_value.set(filename)


button_digits.configure(command=onSearch)
btn_download.configure(command=onDownload)
btn_choose_dir.configure(command=onChoose)

root.mainloop()
