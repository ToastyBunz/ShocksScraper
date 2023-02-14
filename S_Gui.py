import tkinter
from tkinter import Tk
from tkinter import messagebox
import pandas as pd
import sqlite3
import os
from pathlib import Path
# from tkinter import *
from PIL import Image
from tkinter import ttk
import pickle
import customtkinter
from customtkinter import *
import bilstein
import meyer
import turn14
from dotenv import set_key

tree_width = 150

height_var = 50
width_var = 60

x_pad_1 = 5
y_pad_1 = 10

question_width = 400
h_font = ('Helvetica', 15)

bs_1 = '24-238304'
bs_2 = '24-186728'
bs_3 = '47-310971'

ks_1 = '25001-397A'
fs_1 = '883-06-132'

favorites = [bs_1, bs_2, bs_3, ks_1, fs_1]

# fav_list = []

filename = 'Favorites.pk'

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

heart_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "white_heart.png")), size=(26, 26))
unfave_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "heart_x.png")), size=(26, 26))
excel_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Excel-Logo-WEB.png")), size=(360, 136))

try:
    with open(filename, 'rb+') as fav_parts:
        fav_list = pickle.load(fav_parts)

except FileNotFoundError:
    pass


def add_fav(num):
    fav_list.append(num)
    print(fav_list)
    # update_fave()


def sub_fav(num):
    try:
        fav_list.remove(num)

    except ValueError:
        pass
    # update_fave()


def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)


def clipboard_link(tree, self):
    y = tree.focus()
    values = tree.item(y, 'values')
    link = values[3]
    tkinter.Tk.clipboard_clear(self)
    tkinter.Tk.clipboard_append(self, string=link)
    tkinter.Tk.update(self)


def open_product_link():
    messagebox.showerror(title='Missing Field ', message="No internet")

def update_credentials(bil_l, bil_p, mey_l, mey_p, t14_l, t14_p):
    envpath = os.path.abspath('.env')
    new_creds = {'bilstein_user': bil_l, 'bilstein_pass': bil_p, 'meyer_user': mey_l,
                 'meyer_pass': mey_p, 'turn14_user': t14_l, 'turn14_pass': t14_p }

    cred_tokens = {'bilstein_user': 'BILSTEIN_USER', 'bilstein_pass': 'BILSTEIN_PASS', 'meyer_user': 'MEYER_USER',
                 'meyer_pass': 'MEYER_PASS', 'turn14_user': 'TURN14_USER', 'turn14_pass': 'TURN14_PASS'}

    for key in new_creds:
        if new_creds[key] == '':
            pass
        else:
            print('replace', os.getenv(cred_tokens[key]), 'with', new_creds[key])
            set_key(envpath, cred_tokens[key], new_creds[key])



def combine_funcs(*funcs):
    def inner_combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return inner_combined_func

def login_window():
    window = CTkToplevel()
    window.title("Credentials update")
    window.geometry('1366x768')

    # label = CTkLabel(window, text='Login Credentials', font=h_font)

    bilstein_frame = CTkFrame(window, fg_color='transparent')
    bilstein_label = CTkLabel(bilstein_frame, width=tree_width, text="Bilstein Credentials", font=h_font)
    bilstein_user = CTkEntry(bilstein_frame, width=question_width, placeholder_text="Bilstein Username")
    bilstein_pass = CTkEntry(bilstein_frame, width=question_width, placeholder_text="Bilstein Password")

    bilstein_label.grid(row=0, column=0)
    bilstein_user.grid(row=1, column=0)
    bilstein_pass.grid(row=2, column=0)


    meyer_frame = CTkFrame(window, fg_color='transparent')
    meyer_label = CTkLabel(meyer_frame, width=tree_width, text="Meyer Credentials", font=h_font)
    meyer_user = CTkEntry(meyer_frame, width=question_width, placeholder_text="Meyer Username")
    meyer_pass = CTkEntry(meyer_frame, width=question_width, placeholder_text="Meyer Password")

    meyer_label.grid(row=0, column=0)
    meyer_user.grid(row=1, column=0)
    meyer_pass.grid(row=2, column=0)


    t14_frame = CTkFrame(window, fg_color='transparent')
    t14_label = CTkLabel(t14_frame, width=tree_width, text="Turn14 Credentials", font=h_font)
    t14_user = CTkEntry(t14_frame, width=question_width, placeholder_text="Turn14 Username")
    t14_pass = CTkEntry(t14_frame, width=question_width, placeholder_text="Turn14 Password")

    t14_label.grid(row=0, column=0)
    t14_user.grid(row=1, column=0)
    t14_pass.grid(row=2, column=0)


    close_frame = CTkFrame(window, fg_color='transparent')
    exit_button = CTkButton(close_frame, text='Cancel', width=100, command=lambda: window.destroy())
    save_button = CTkButton(close_frame, text='Save', width=100,
                     command= combine_funcs(lambda: update_credentials(bilstein_user.get(), bilstein_pass.get(), meyer_user.get(), meyer_pass.get(), t14_user.get(), t14_pass.get()), lambda: window.destroy()))

    exit_button.grid(row=2, column=0, sticky='sw', pady=10, padx=(0, 720))
    save_button.grid(row=2, column=2, sticky='se', pady=10, padx=(0, 0))

    # label.pack()
    bilstein_frame.pack(pady=60, padx=100)
    meyer_frame.pack(pady=60, padx=100)
    t14_frame.pack(pady=60, padx=100)
    close_frame.pack(side=BOTTOM)



class Shock_Search(CTk):
    def __init__(self, *args, **kwargs):
        CTk.__init__(self, *args, **kwargs)

        # Root Frame
        self.title('Shock Search')
        self.geometry('1366x768')
        # customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

        logo_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')
        quasar_label = CTkLabel(logo_frame, text="In collaboration with QUASAR", compound="left",
                                font=CTkFont(size=15, weight="bold"))

        excel_label = customtkinter.CTkLabel(logo_frame, text="", image=excel_image)

        excel_label.pack()
        quasar_label.pack()
        logo_frame.pack(pady=(30, 0))

        search_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')
        search_frame.pack(pady=30)

        combobox_var = StringVar(value="")

        shocks_tree = ttk.Treeview(self)

        def search_part(num):
            results = []
            hasBilstein = False
            hasMeyer = False
            hasTurn14 = False
            print(num)
            bilstein_output = bilstein.searchBilstein(num)
            print(bilstein_output)
            if (not "error" in bilstein_output.keys()):
                bilstein_output_tuple = (
                    bilstein_output.get("distributor"),
                    bilstein_output.get("price"),
                    bilstein_output.get("stock"),
                    bilstein_output.get("link"))
                results.append(bilstein_output_tuple)

            meyer_output = meyer.searchMeyer(num)
            print(meyer_output)
            if (not "error" in meyer_output.keys()):
                meyer_output_tuple = (
                    meyer_output.get("distributor"),
                    meyer_output.get("price"),
                    meyer_output.get("stock"),
                    meyer_output.get("link"))
                results.append(meyer_output_tuple)
            turn14_output = turn14.searchTurn14(num)
            print(turn14_output)
            if (not "error" in turn14_output.keys()):
                turn14_output_tuple = (
                    turn14_output.get("distributor"),
                    turn14_output.get("price"),
                    turn14_output.get("stock"),
                    turn14_output.get("link"))
                results.append(turn14_output_tuple)

            clear_treeview(shocks_tree)

            for result in range(len(results)):
                shocks_tree.insert(parent='', index='end', iid=str(result), text='', values=results[result])

            print(num)

        search_unfavorite = CTkButton(search_frame, height=height_var, width=60, text='', image=unfave_image,
                                      command=lambda: sub_fav(search_combo.get()))
        search_favorite = CTkButton(search_frame, height=height_var, width=60, text='', image=heart_image,
                                    command=lambda: add_fav(search_combo.get()))
        search_combo = CTkComboBox(search_frame, values=fav_list, height=height_var, width=550, variable=combobox_var)
        search_button = CTkButton(search_frame, height=height_var, width=100, text='Search', font=('Helvetica', 15),
                                  command=lambda: search_part(search_combo.get()))  # search_combo.get()))

        search_unfavorite.grid(row=0, column=0, padx=x_pad_1)
        search_favorite.grid(row=0, column=1, padx=x_pad_1)
        search_combo.grid(row=0, column=2, padx=x_pad_1)
        search_button.grid(row=0, column=3, padx=x_pad_1)

        shocks_tree['columns'] = ('Distributor', 'Price', "In Stock", 'Link')

        shocks_tree.column('#0', width=0, stretch=NO)
        shocks_tree.column("Distributor", anchor='w', width=tree_width)
        shocks_tree.column("Price", anchor='w', width=tree_width)
        shocks_tree.column("In Stock", anchor='w', width=280)
        shocks_tree.column("Link", anchor='w', width=380)

        shocks_tree.heading("#0", text="", anchor='w')
        shocks_tree.heading("Distributor", text="Distributor", anchor='w')
        shocks_tree.heading("Price", text="Price", anchor='w')
        shocks_tree.heading("In Stock", text="In Stock", anchor='w')
        shocks_tree.heading("Link", text="Link", anchor='w')

        shocks_tree.pack()

        # link frame
        link_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')
        link_frame.pack()

        credentials_button = CTkButton(link_frame, height=height_var, width=135, text='Update Credentials',
        command=lambda: login_window())

        link_button = CTkButton(link_frame, height=height_var, width=60, text='Save link to clipboard',
                                command=lambda: clipboard_link(shocks_tree, self))

        openpage_button = CTkButton(link_frame, height=height_var, width=60, text='Open Selected Webpage',
                                    command=lambda: open_product_link())

        credentials_button.grid(row=0, column=0, padx=20, pady=20, sticky="e")
        link_button.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        openpage_button.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # Theme frame
        theme_frame = CTkFrame(self, corner_radius=0, fg_color='transparent')
        theme_frame.pack(side=BOTTOM)

        appearance_mode_menu = CTkOptionMenu(theme_frame,
                                             values=["System", "Light", "Dark"],
                                             command=self.change_appearance_mode_event
                                             )
        appearance_mode_menu.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


app = Shock_Search()
app.mainloop()

with open(filename, 'wb') as fav_parts:
    pickle.dump(fav_list, fav_parts)

