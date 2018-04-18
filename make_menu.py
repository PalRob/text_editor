# -*- coding: utf-8 -*-
"""This module automates construction of tk.Menu and tk.Menubutton
    widgets.

"""

import tkinter as tk
from tkinter.constants import * # pylint: disable=unused-wildcard-import


def make_menu(parent, menu_content):
    """Creates an instance of tkinter Menu class with given content.
    Args:
        parent (Class): parent class that menu widget attached to;
        menu_content (list): list of dictionaries. Every dict is a
            separate command that would be added to the menu. Type of
            command determined by the "entry_type". Structure of the
            list:
                [dict(entry_type="command/cascade/checkbutton/
                    radiobutton", other keywords arguments for the
                    specific menu being created (for cascade keyword
                    argument menu=menu_content for the submenu)),
                    or SEPARATOR]
        **options: keyword arguments for the tk.Menu widget. Listed in
            documentation for tkinter.
    Returns:
        menu (tk.Menu): An instance of a Menu class filled with
            menu_content.

    """
    # Originally "tearoff" defaults to True.
    # Lines below set it to False by default.
    options = dict(tearoff=NO)

    menu = tk.Menu(parent, **options)

    commands = {"command": menu.add_command,
                "separator": menu.add_separator,
                "cascade": menu.add_cascade,
                "checkbutton": menu.add_checkbutton,
                "radiobutton": menu.add_radiobutton,
                "options": menu.config}

    # Special cases for "separator" and "cascade".
    for menu_entry in menu_content:
        if menu_entry == SEPARATOR:
            commands[SEPARATOR]()
            continue

        entry = menu_entry
        entry_type = entry["entry_type"].lower()
        del entry["entry_type"]

        if entry_type == "cascade":
            entry["menu"] = make_menu(menu, entry["menu"])

        if entry_type == "options":
            # dummy_options - placeholder in caise the enty options
            # passed two or more times for some reason
            dummy_options = options
            # Clashing keys in options overwrited by respective
            # keys in entry
            dummy_options.update(entry)
            entry = options

        commands[entry_type](**entry)

    return menu

def make_menu_button(parent, menu_button_content, **options):
    """Creates an instance of tkinter Menubutton class with given content.
    Args:
        parent (Class): parent class that menubutton widget attached to;
        menu_button_content (2-tuple): ("menu_button_label",
            [menu_content]). Description of a menu_content given in
            a docstring of the make_menu function.
        **options: keyword arguments for the tk.Menu widget. Listed in
            documentation for tkinter.
    Returns:
        menubutton(tk.Menubutton): An instance of a Menu class filled
            with menu_button_content.
    """
    menu_button_label = menu_button_content[0]
    menu_content = menu_button_content[1]

    menubutton = tk.Menubutton(parent, text=menu_button_label, **options)
    menu = make_menu(menubutton, menu_content, **options)
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
                    label="100", variable=var_3, value=100),
                dict(entry_type="options", bg='red')]),
            dict(entry_type="command", label="Print radio",
                command=lambda:print(var_3.get()))])

    menu = make_menu_button(root, menu_content)
    menu.pack()
    root.mainloop()
