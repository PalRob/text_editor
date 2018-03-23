"""Automation of the menu construction.

TODO:
    Add docstrings to functions;"""

import tkinter as tk
from tkinter.constants import *



def make_menu(parent, menu_content, tearoff=NO):
    menu = tk.Menu(parent, tearoff=tearoff)

    commands = {"command": menu.add_command,
                "separator": menu.add_separator,
                "cascade": menu.add_cascade,
                "checkbutton": menu.add_checkbutton,
                "radiobutton": menu.add_radiobutton}

    for menu_entry in menu_content:
        if menu_entry == SEPARATOR:
            commands[SEPARATOR]()
            continue

        entry = menu_entry
        entry_type = entry["entry_type"]
        del entry["entry_type"]

        if entry_type == "cascade":
            entry["menu"] = make_menu(menu, entry["menu"])

        commands[entry_type](**entry)

    return menu

def make_menu_button(parent, menu_button_content, tearoff=NO):
    menu_button_label = menu_button_content[0]
    menu_content = menu_button_content[1]

    menubutton = tk.Menubutton(parent, text=menu_button_label)
    menu = make_menu(menubutton, menu_content, tearoff=tearoff)
    menubutton.config(menu=menu)

    return menubutton


if __name__ == '__main__':
    root = tk.Tk()
    var_1 = tk.IntVar()
    var_2 = tk.IntVar()
    var_3 = tk.IntVar()

    menu_content = ('Test_button', [
            dict(entry_type="command", label="Command"),
            SEPARATOR,
            dict(entry_type='cascade', label='Cascade of cats', menu=[
                dict(entry_type="command", label="White"),
                dict(entry_type="command", label="Black"),
                dict(entry_type="command", label="Brown")]),
            dict(entry_type='cascade', label='Checkbuttons', menu=[
                dict(entry_type="checkbutton",
                    label="Button_1", variable=var_1),
                dict(entry_type="checkbutton",
                    label="Button_2", variable=var_2)]),
            dict(entry_type='cascade', label='Radiobuttons', menu=[
                dict(entry_type='radiobutton',
                    label="10", variable=var_3, value=10),
                dict(entry_type='radiobutton',
                    label="100", variable=var_3, value=100)]),
            dict(entry_type="command", label="Print radio",
                command=lambda:print(var_3.get()))])

    menu = make_menu_button(root, menu_content)
    menu.pack()
    root.mainloop()