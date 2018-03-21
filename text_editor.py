"""Simple text editor made with tkinter.

TODO:
Figure out how to make line_numbers widget that will scoll together
    with the Text widget. It should update automaticly when the
    number of "initiated" lines change and if the line number
    should become highlited when the coursor in in this line,
    just like in Sublime;
Create a separate module make_menus that is similar in function
    to the GUIMaker module from the book. It should take a nested
    list and construct a menu that could be used in the Menubar
    as well as in ContextMenu. Should be able to pass icons and
    shortcuts as optional arguments;
Create bar for buttons that duplicates some operations from the
    menubar. Should be able to hide it;
Create a menu and develop methods for this menu:
    File:
        New file
        Open...
        Save
        Save as...

        Quit

    Edit:
        Undo

        Cut
        Copy
        Paste
        Delete

        Find...
        Find and replace...
        Find in files...
        Go to...

    Format:
        Font...

    View:
        Statusbar (check yes / no)


    Help:
        Show help...
        About;
"""

import os
import sys
import tkinter as tk
from tkinter.constants import * # pylint: disable=unused-wildcard-import
from make_menu import make_menu_button
# Program's name:
PROGRAM_NAME = "text_editor"

class TextEditor(tk.Frame):
    """Frame with a simple text editor. Main class of the programm."""
    def __init__(self, parent=None, file=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)

        # Class attributes
        self.file = file
        # Attributes for GUI widgets.
        # Assigned values during GUI construction
        self.menubar = None
        self.textspace = None
        self.text = None
        self.statusbar = None

        # GUI construction
        self.make_menubar()
        self.make_textspace()
        self.make_statusbar()

        # Other GUI related functions
        self.set_win_size()
        self.bind_keys()
        self.focus_on_text()
        # Change in a future
        # Bare bones functionality if the file -> open function
        self.open()


    # GUI construction methods
    def make_menubar(self):
        """Creates Menubar widget on the top of the parent's window."""
        self.menubar = Menubar(self)

    def make_textspace(self):
        """Creates expandable Frame widget that contains the Text
        widget."""
        self.textspace = TextSpace(self)
        self.text = self.textspace.text

    def make_statusbar(self):
        """Creates Statusbar widget on the bottom of the parent's
        window."""
        self.statusbar = Statusbar(self)
        self.update_cursor_status()

    # Additional metdods
    def set_win_size(self, size=None, ratio=None):
        """Sets size of the main application window.
        Args:
            size(tuple): two-tuple of two integer values: width and
                heing of the main application window. Defaults to None.
            ratio(tuple): two-tuple of two float values in range
                between 0 and 1: main application window size as a
                fraction of screen. If no size given default to half
                of the screen size for both width and height.
        Returns: None
        """
        default_ratio_x = 0.5
        default_ratio_y = 0.5

        if size:
            width, height = size
        else:
            if ratio:
                ratio_x, ratio_y = ratio
            else:
                ratio_x = default_ratio_x
                ratio_y = default_ratio_y
            screen_x = self.winfo_screenwidth()
            screen_y = self.winfo_screenheight()
            width = int(screen_x * ratio_x)
            height = int(screen_y * ratio_y)

        self.master.geometry('{}x{}'.format(width, height))


    def open(self):
        if self.file:
            with open(self.file, 'r') as file:
                for line in file:
                    self.text.insert(END, line)
        self.text.mark_set(INSERT, "1.0")

    def bind_keys(self):
        """Bind keys to actions bedore the program starts.
        """

        # Keybinds for corsor position indicator in statusbar.
        # Any pressed key or LMB click will update cursor position
        # white textspace is in focus.
        self.text.bind('<Key>',
                       lambda event: self.update_cursor_status())
        self.text.bind('<Button-1>',
                       lambda event: self.update_cursor_status())

    def update_cursor_status(self):
        """Updates corsor position indicator in statusbar
        """
        # after_idle method is used to get cursor position after
        # the action it is binded to were performed.
        self.after_idle(self.statusbar.update_cursor_position)

    def focus_on_text(self):
        self.text.focus()

class Menubar(tk.Frame):
    """Frame containing menus."""
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
    # File:
    #     New file
    #     Open...
    #     Save
    #     Save as...

    #     Quit
        self.menus = []
        # File menu
        self.file_menu_content = ('File', [
            {"label": "New file"},
            {"label": "Open..."},
            {"label": "Save"},
            {"label": "Save as..."},
            SEPARATOR,
            {"label": "Quit"}])
        self.menus.append(self.file_menu_content)
        # Edit menu
        self.edit_menu_content = ("Edit",[
            {"label": "Undo"},
            SEPARATOR,
            {"label": "Cut"},
            {"label": "Copy"},
            {"label": "Paste"},
            {"label": "Delete"},
            SEPARATOR,
            {"label": "Find..."},
            {"label": "Find and replace..."},
            {"label": "Find ain files..."},
            {"label": "Go to..."}])
        self.menus.append(self.edit_menu_content)
    # Format menu:
        self.format_menu_content = ("Format", [
            {"label": "Font..."}])
        self.menus.append(self.format_menu_content)
    # View menu:
        self.view_menu_content = ("View", [
            {"label": "Statusbar"}])
        self.menus.append(self.view_menu_content)

    # Help:
    #     Show help...
    #     About;
        self.help_menu_content = ("Help", [
            {"label": "Show help..."},
            {"label": "About"}])
        self.menus.append(self.help_menu_content)

        for menu in self.menus:
            make_menu_button(self, menu).pack(side=LEFT)
        self.pack(side=TOP, fill=X)


class TextSpace(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=YES)

        # Class attributes

        # Attributes for GUI widgets.
        # Assigned values during GUI construction
        self.text = None
        self.line_numbers = None
        self.x_scrollbar = None
        self.y_scrollbar = None

        self.make_widgits()
        self.config_grid()
        self.config_text()

    def make_widgits(self):
        self.make_text()
        # Currently line numbers disabled
        #self.make_line_numbers()
        self.make_scrollbars()

    def make_line_numbers(self):
        self.line_numbers = LineNumbers(self)
        self.line_numbers.grid(row=0, column=0, sticky=N+S)

    def make_text(self):
        # Should make a class in a future for a text widgit
        self.text = tk.Text(self)
        self.text.grid(row=0, column=1, sticky=N+W+E+S)

    def make_scrollbars(self):
        self.y_scrollbar = tk.Scrollbar(self, orient=VERTICAL)
        self.y_scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.grid(row=0, column=2, sticky=N+S)

        self.x_scrollbar = tk.Scrollbar(self, orient=HORIZONTAL)
        self.x_scrollbar.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.grid(row=1, column=0, columnspan=2, sticky=W+E)

    def config_text(self):
        self.text.config(wrap=NONE)

    def config_grid(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


class LineNumbers(tk.Canvas):
    def __init__(self, parent=None):
        tk.Canvas.__init__(self, parent)
        self.parent = parent
        self.text = self.parent.text

        self.num_of_lines = self.get_num_of_lines()

        self.set_width(40)
        self.write_numbers()

    def set_width(self, width):
        self.config(width=width)

    def write_numbers(self):
        self.num_of_lines = self.get_num_of_lines()
        num_of_digits = len(str(self.num_of_lines))
        i = self.text.index('@0,0')
        self.text.update()
        # Lines indexed from 1, not from 0, that is why the range
        # function called with (1, n+1)
        while True:
            dline = self.text.dlineinfo(i)
            if dline:
                y = dline[1]
                linenum = i.split('.')[0]
                # Rjust doesn't work for some reason
                #linenum = linenum.rjust(num_of_digits)
                self.create_text(1, y, anchor=N+W, text=linenum)
                i = self.text.index('{0}+1line'.format(i))
            else:
                break

    def get_num_of_lines(self):
        num_of_lines = int(self.text.index(END+'-1c').split('.')[0])
        return num_of_lines




class Statusbar(tk.Frame):
    """Frame containing text_editor's statusbar.

    Have an indicator that displays current cursor position in
    "line" | "column" format

    TODO:
        Create "length" and "number of lines" indicator like in the
        notepad++;
        Create "sel" indicator akin to one in the notepad++;
        CursorPosition and methods related to it should be separate
        class.
    """
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack(side=BOTTOM, expand=NO, fill=X)
        self.make_cursor_position_box()

    def make_cursor_position_box(self):
        self.cursor_position = tk.Label(self, width=40)
        self.cursor_position.pack(side=RIGHT)

    def get_cursor_pos(self):
        """Get current cursor position.

        Returns:
            list: [line, column]
        """
        return self.parent.text.index(INSERT).split('.')

    def update_cursor_position(self):
        """Update Statusbar's cursor position display.
        """
        cursor_pos = self.get_cursor_pos()
        cursor_pos_text = "line {} col {}".format(*cursor_pos)
        self.cursor_position.config(text=cursor_pos_text)


if __name__ == '__main__':
    FILENAME = os.path.abspath(__file__)
    TextEditor(file=FILENAME).mainloop()
