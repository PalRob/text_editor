"""Automation of the menu construction.

TODO:
    Add docstrings to functions"""

import tkinter as tk
from tkinter.constants import *



def make_menu(parent, menu_content, tearoff=NO):
    menu = tk.Menu(parent, tearoff=tearoff)

    for command in menu_content:
        if type(command) == dict:
            menu.add_command(**command)
        elif type(command) == tuple:
            submenu = make_menu(menu, command[1])
            menu.add_cascade(label=command[0], menu=submenu)
        elif command == SEPARATOR:
            menu.add_separator()

    return menu

def make_menu_button(parent, menu_button_content, tearoff=NO):
    menu_button_label = menu_button_content[0]
    menu_content = menu_button_content[1]

    menubutton = tk.Menubutton(parent, text=menu_button_label)
    menu = make_menu(menubutton, menu_content, tearoff=tearoff)
    menubutton.config(menu=menu)

    return menubutton


if __name__ == '__main__':
    menu_content = ('File', [
            {"label": "New file"},
            {"label": "Open..."},
            {"label": "Save"},
            {"label": "Save as..."},
            SEPARATOR,
            ('Cats',
                [{"label": "White"},
                {"label": "Black"},
                {"label": "Brown"}]),
            {"label": "Quit"}])

    root = tk.Tk()
    menu = make_menu_button(root, menu_content)
    menu.pack()
    root.mainloop()