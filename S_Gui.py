import tkinter
import pandas as pd
import sqlite3
import os
from pathlib import Path
# from tkinter import *
from tkinter import ttk
import pickle
import customtkinter
from customtkinter import *

bs_1 = '24-238304'
bs_2 = '24-186728'
bs_3 = '47-310971'

ks_1 = '25001-397A'

fs_1 = '883-06-132'

favorites = [bs_1, bs_2, bs_3, ks_1, fs_1]

filename = 'Favorites.pk'



# def update_fave():
#     with open(filename, 'wb') as fi:
#         # dump your data into the file
#         pickle.dumps(favorites, fi)
#
#
# update_fave()


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


def search_part(num):
    print(num)

def add_fav(num):
    favorites.append(num)
    # update_fave()

def sub_fav(num):
    favorites.remove(num)
    # update_fave()

height_var = 50
width_var = 60

x_pad_1 = 5
y_pad_1 = 10

class Shock_Search(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)

        # def search_part():
        #     num = search_combo.get()
        #     print(num)
        #
        # def add_favorite():


        # Root Frame
        self.title('Shock Search')
        self.geometry('1100x600')
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        search_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')
        search_frame.pack(pady=60)

        combobox_var = StringVar(value="Search Part Number")

        search_favorite = CTkButton(search_frame, height=height_var, width=60, text='heart', command=lambda: add_fav(search_combo.get()))
        search_unfavorite = CTkButton(search_frame, height=height_var, width=60, text='unheart', command=lambda: sub_fav(search_combo.get()))
        search_combo = CTkComboBox(search_frame, values=favorites, height=height_var, width=550, variable=combobox_var)
        search_button = CTkButton(search_frame, height=height_var, width=100, text='Search', command=lambda: search_part(search_combo.get()))

        search_favorite.grid(row=0, column=0, padx=x_pad_1)
        search_unfavorite.grid(row=0, column=1, padx=x_pad_1)
        search_combo.grid(row=0, column=2, padx=x_pad_1)
        search_button.grid(row=0, column=3, padx=x_pad_1)

        shocks_tree = ttk.Treeview(self)

        shocks_tree['columns'] = ('Distributor', 'Price', "In Stock", 'Link')


        shocks_tree.column('#0', width=0, stretch=NO)
        shocks_tree.column("Distributor", anchor='w')
        shocks_tree.column("Price", anchor='w')
        shocks_tree.column("In Stock", anchor='w')
        shocks_tree.column("Link", anchor='w')


        shocks_tree.heading("#0", text="", anchor='w')
        shocks_tree.heading("Distributor", text="Distributor", anchor='w')
        shocks_tree.heading("Price", text="Price", anchor='w')
        shocks_tree.heading("In Stock", text="In Stock", anchor='w')
        shocks_tree.heading("Link", text="Link", anchor='w')

        shocks_tree.insert(parent='', index='end', iid='0', text='', values=("Bernstein", 113, 1000, 'https://cart.bilsteinus.com'))

        shocks_tree.pack()



app = Shock_Search()
app.mainloop()