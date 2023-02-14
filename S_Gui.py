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
from concurrent.futures import ThreadPoolExecutor, wait
import re
import traceback

price_match_regex = "(\d+\.\d{2})\d+"
bs_1 = '24-238304'
bs_2 = '24-186728'
bs_3 = '47-310971'

ks_1 = '25001-397A'
fs_1 = '883-06-132'
print(re.search(price_match_regex, "$94.120000").group(1))


favorites = [bs_1, bs_2, bs_3, ks_1, fs_1]

# fav_list = []

filename = 'Favorites.pk'

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

heart_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "white_heart.png")), size=(26, 26))
unfave_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "heart_x.png")), size=(26, 26))
excel_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Excel-Logo.png")), size=(360, 136))

try:
    with open(filename, 'rb+') as fav_parts:
        fav_list = pickle.load(fav_parts)

except FileNotFoundError:
    pass

# loginFutures = []
# with ThreadPoolExecutor() as executor:    
#     #loginFutures.append(executor.submit(bilstein.loginBilstein))
#     loginFutures.append(executor.submit(meyer.loginMeyer))
#     loginFutures.append(executor.submit(turn14.loginTurn14))
# wait(loginFutures)

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


tree_width = 150

height_var = 50
width_var = 60

x_pad_1 = 5
y_pad_1 = 10


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

        combobox_var = StringVar(value="Search Part Number")

        shocks_tree = ttk.Treeview(self)

        def search_part(num):
            if (len(num) == 0) :
                return
            results = []
            print(num)
            try:
                bilstein_output = bilstein.search(num)
                print(bilstein_output)
                if (not "error" in bilstein_output.keys()):
                    bilstein_output_tuple = (
                        bilstein_output.get("distributor"),
                        bilstein_output.get("price"),
                        bilstein_output.get("stock"),
                        bilstein_output.get("link"))
                    results.append(bilstein_output_tuple)
                else:
                    results.append(("Bilstein", "--", "--", bilstein_output.get("error")))
            except Exception as e:
                results.append(("Bilstein", "--", "--", str(e) + e.__traceback__.__str__()))
                traceback.print_exc()

            try:
                meyer_output = meyer.search(num)
                print(meyer_output)
                if (not "error" in meyer_output.keys()):
                    meyer_output_tuple = (
                        meyer_output.get("distributor"),
                        meyer_output.get("price"),
                        meyer_output.get("stock"),
                        meyer_output.get("link"))
                    results.append(meyer_output_tuple)
                else:
                    results.append(("Meyer", "--", "--", meyer_output.get("error")))
            except Exception as e:
                results.append(("Meyer", "--", "--", str(e) + str(e.__traceback__)))
                traceback.print_exc()
            try:
                turn14_output = turn14.search(num)
                print(turn14_output)
                if (not "error" in turn14_output.keys()):
                    turn14_output_tuple = (
                        turn14_output.get("distributor"),
                        turn14_output.get("price"),
                        turn14_output.get("stock"),
                        turn14_output.get("link"))
                    results.append(turn14_output_tuple)
                else:
                    results.append(("Turn14", "--", "--", turn14_output.get("error")))
            except Exception as e:
                results.append(("Turn14", "--", "--", str(e) + str(e.__traceback__)))
                traceback.print_exc()
            clear_treeview(shocks_tree)

            for result in range(len(results)):
                # cleanPrice = results[result][1]
                # print(cleanPrice)
                # cleanPrice = re.search(price_match_regex, cleanPrice).group(1)
                # print(cleanPrice)
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

        link_button = CTkButton(link_frame, height=height_var, width=60, text='Save link to clipboard',
                                command=lambda: clipboard_link(shocks_tree, self))

        openpage_button = CTkButton(link_frame, height=height_var, width=60, text='Open Selected Webpage',
                                    command=lambda: open_product_link())

        link_button.grid(row=0, column=0, padx=20, pady=20, sticky="e")
        openpage_button.grid(row=0, column=1, padx=20, pady=20, sticky="e")

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

bilstein.cleanup()
meyer.cleanup()
turn14.cleanup()
with open(filename, 'wb') as fav_parts:
    pickle.dump(fav_list, fav_parts)

