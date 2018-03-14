"""Simple text editor made with tkinter.
"""

import os
import sys
import tkinter as tk
from tkinter.constants import *

class TextEditor(tk.Frame):
    """Frame with a simple text editor. Main class of the programm."""
    def __init__(self, parent=None, file=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)

        # Class attributes
        self.file = file

        # GUI construction
        self.make_menubar()
        self.make_textspace()
        self.make_statusbar()

        # Other GUI related functions
        self.set_win_size()

    # GUI construction methods
    def make_menubar(self):
        self.menubar = Menubar(self)

    def make_textspace(self):
        self.textspace = TextSpace(self)

    def make_statusbar(self):
        self.statusbar = Statusbar(self)

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


class Menubar(tk.Frame):
    """Frame containing menus."""
    pass

class TextSpace(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=YES)

        #self.line_numbers = None
        self.text = ScrolledText(self)


class ScrolledText(tk.Text):
    def __init__(self, parent=None):
        tk.Text.__init__(self, parent)
        self.make_scrollbars()
        self.config_scrollbars()
        self.config_text()
        self.pack(fill=BOTH, expand=YES)

    def make_scrollbars(self):
        self.y_scrollbar = tk.Scrollbar(self, orient=VERTICAL)
        self.y_scrollbar.config(command=self.yview)
        self.config(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)

        self.x_scrollbar = tk.Scrollbar(self, orient=HORIZONTAL)
        self.x_scrollbar.config(command=self.xview)
        self.config(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.pack(side=BOTTOM, fill=X)


    def config_scrollbars(self):
        pass

    def config_text(self):
        self.config(wrap=NONE)


class Statusbar(tk.Frame):
    pass


if __name__ == '__main__':
    FILENAME = os.path.abspath(__file__)
    TextEditor(file=FILENAME).mainloop()