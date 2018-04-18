#!/usr/bin/env python
"""Simple text editor made with tkinter.

TODO:
Figure out how to make line_numbers widget that will scroll together
    with the Text widget. It should update automatically when the
    number of "initiated" lines change and if the line number
    should become highlighted when the cursor in in this line,
    just like in Sublime;
Create a separate module make_menus that is similar in function
    to the GUIMaker module from the book. It should take a nested
    list and construct a menu that could be used in the Menubar
    as well as in ContextMenu. Should be able to pass icons and
    shortcuts as optional arguments;
Create bar for buttons that duplicates some operations from the
    menubar. Should be able to hide it;
The program should remember some options set by the user
    previously and store them for future use;
The program should be able to support opening multiple text
    files at once and give user an ability to freely switch
    between them. The ttk.Notebook widget should do the trick;
"""

import os
import sys
import tkinter as tk
from tkinter.constants import * # pylint: disable=unused-wildcard-import
import tkinter.messagebox
import tkinter.filedialog
from make_menu import make_menu_button

# Program's name:
PROGRAM_NAME = "text_editor"

class TextEditor(tk.Frame):
    """Frame with a simple text editor. Main class of the program."""
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
        self.menubar._get_text()
        self.set_win_size()
        self.bind_keys()
        self._focus_on_text()
        # TODO:
        # Change in future
        # Bare bones functionality if the file -> open function
        if self.file:
            MenuMethods.open(self.text, self, self.file)
        # Used so undo method won't delete inserted text
        # should add this line in the actual
        # EditMenuMethods.open method
        self.text.edit_reset()
        self._update_window_title()

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
        self._update_cursor_status()

    # Additional methods
    def set_win_size(self, size=None, ratio=None):
        """Sets size of the main application window.
        Args:
            size(tuple): two-tuple of two integer values: width and
                height of the main application window. Defaults to None.
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

    def bind_keys(self):
        """Bind keys to actions bedfore the program starts.
        """

        # Keybinds for cursor position indicator in statusbar.
        # Any pressed key or LMB click will update cursor position
        # white textspace is in focus.
        self.text.bind('<Key>',
                       lambda event: self._update_cursor_status())
        self.text.bind('<Button-1>',
                       lambda event: self._update_cursor_status())
        # self.textspace.bind_all('<MouseWheel>',
        #     lambda event:self.update_line_numbers())

    def _update_cursor_status(self):
        """Updates cursor position indicator in statusbar
        """
        # after_idle method is used to get cursor position after
        # the action it is binded to were performed.
        self.after_idle(self.statusbar._update_cursor_position)

    # def update_line_numbers(self):
    #     self.textspace.line_numbers.write_numbers()

    def _focus_on_text(self):
        """Sets focus on the text widget."""
        self.text.focus()

    def _update_window_title(self):
        """Updates main window title in the '{filepath} {program_name}'
        format. Filepath substituted for 'untitled' if no file were
        given."""
        if self.file is None:
            filename = "untitled"
        else:
            filename = self.file
        program = PROGRAM_NAME

        title = "{0} - {1}".format(filename, program)
        self.master.title(title)

class FileMenuMethods:
    """Container class for File menu methods"""
    def new_file(text, parent):
        """Creates new file. If contents of the text widget were
        modified, calls AskSave message dialog, execution of the
        function stops in the option "Cancel" were chosen.
        Args:
            text (tk.Text): instance of a tk.Text widget that used
                as the textspace of the editor;
            parent: supposedly the second topmost parent class of the
                program, one below the tk.Tk;
        Returns:
            None
        """
        if FileMenuMethods._save_modified(text, parent) is None:
            return
        text.delete("1.0", END)

        file = None
        FileMenuMethods._set_current_file(file, parent)

        parent._update_window_title()

    def open(text, parent, file=None, **options):
        if FileMenuMethods._save_modified(text, parent) is None:
            return
        FileMenuMethods._open_file(text, parent, file, **options)


    def save(text, parent):
        # not finished
        file = parent.file
        if not file:
            FileMenuMethods.save_as(text, parent)
        else:
            if not FileMenuMethods._is_modified(text):
                pass
            else:
                FileMenuMethods._save_file(text, file)

    def save_as(text, parent):
        # defaultextention="*.*" means that returned path will
        # have an extension chosen from the filetypes list
        # automatically added to it

        # TODO:
        # Improve saving process. Learn about conventional way to
        # implement save_as interface and make it like that.
        # When filetype is "All files" writing a filename like,
        # for example "cat.py", will be met with a messagebox
        # "Unacceptable filename", but choosing an existing file
        # will work without problems
        file = tkinter.filedialog.asksaveasfilename(filetypes=[
            ("All files", '*.*'), ("Text file", '.txt'), ("Python", ".py")],
             defaultextension="*.*")
        if file:
            FileMenuMethods._save_file(text, file)
            FileMenuMethods._set_current_file(file, parent)

    def exit(text, parent):
        if FileMenuMethods._save_modified(text, parent) is None:
            return
        parent.master.destroy()

    # Service methods

    def _open_file(text, parent, file=None, **options):
        # TODO:
        # Make something that will remember user's last opened directory
        # so on the next open or save initial the saved path will be
        # used as initialdir
        file = file or tkinter.filedialog.Open(**options).show()
        if not file:
            return

        text.delete("1.0", END)
        with open(file, 'r') as work_file:
            for line in work_file:
                text.insert(END, line)
        text.mark_set(INSERT, "1.0")
        text.edit_reset()
        text.edit_modified("False")
        FileMenuMethods._set_current_file(file, parent)


    def _save_file(text, file):
        with open(file, 'w') as file:
            # TODO:
            # Taking all of the text at once will cause problems
            # when dealing with big files;

            # END+"-1line" used to avoid automatically adding a
            # newline at the end of the file when saving
            for line in text.get("1.0", END+"-1line"):
                file.write(line)
        text.edit_modified(False)

    def _message_ask_save(file=None):
        if file:
            filename = os.path.basename(filename)
        else:
            filename = "The file"
        title = "Save changes?"
        message = "{} has been modified, save changes?".format(filename)

        return tkinter.messagebox.askyesnocancel(title=title, message=message)

    def _is_modified(text):
        """Checks if text were modified.
        Args:
            text (tk.Text or None): Instance of the tkinter class Text;
                None is passed during the construction of the interface
                if the program were given a file to open on launch.
        Returns:
            (bool): """
        # if text is None:
        #     modified = False
        # else:
        modified = text.edit_modified()
        return modified

    def _save_modified(text, parent):
        """If contents of "text" were modified asks user whether
        or not changes should be saved. Saves changes if user answers
        positively.
        Args:
            text (tk.Text): Instance of the tkinter class Text;
            parent (class): Parent of the class from where this method
                were called;
        Returns:
            (bool or None): If text is not modified this function
                returns False, otherwise returns an answer that user
                gives to the "ask save" message.

                If the answer is "Yes" the contents of text will be
                saved. This function will return True.
                If the answer is "No" this function returns False.
                If the answer is "Cancel" returns None and it is
                assumed that further execution of function from where
                it was called will stop.
            """
        if FileMenuMethods._is_modified(text):
            save_before_action = FileMenuMethods._message_ask_save()
            if save_before_action:
                FileMenuMethods.save(text, parent)
        else:
            save_before_action = False

        return save_before_action

    def _set_current_file(file, parent):
        """Sets attribute file of the parent's master to the value file.
        Args:
            file (str or None): Path to the file being loaded into the
                text editor;
            parent: (class): Parent of the class from where this method
                were called;
        Returns:
            None
        """
        parent.file = file


class EditMenuMethods:
    """Container class for Edit menu methods"""
    # TODO:
    # Some Edit methods should be grayed out if no text is selected
    # or undo/redo stuck is empty
    def undo(text):
        text.edit_undo()

    def redo(text):
        text.edit_redo()

    def cut(text):
        EditMenuMethods.copy(text)
        EditMenuMethods.delete(text)

    def copy(text):
        # TODO:
        # When selected text is copied into the clipboard and then
        # the program window is closed the clipboard becomes empty.
        if EditMenuMethods._text_selected(text):
            text.clipboard_clear()
            text.clipboard_append(text.selection_get())

    def paste(text):
        try:
            clipboard_content = text.clipboard_get()
        except TclError:
            return

        EditMenuMethods.delete(text)
        text.insert(INSERT, clipboard_content)

    def delete(text):
        if EditMenuMethods._text_selected(text):
            text.delete(SEL_FIRST, SEL_LAST)

    def find():
        pass

    def find_and_replace():
        pass

    def find_in_files():
        pass

    def go_to():
        pass

    def _text_selected(text):
        return text.tag_ranges(SEL)


class FormatMenuMethods:
    """Container class for Format menu methods"""
    pass


class ViewMenuMethods:
    """Container class for View menu methods"""
    pass


class HelpMenuMethods:
    """Container class for Help menu methods"""
    def show_help():
        pass
    def about():
        tkinter.messagebox.showinfo(title=PROGRAM_NAME, message=__doc__)


class MenuMethods(FileMenuMethods, EditMenuMethods,
                  FormatMenuMethods, ViewMenuMethods, HelpMenuMethods):
    """Mix-in class for menu methods"""
    pass


class MenuContents():
    def __init__(self):
        self.menus = []
        # File menu
        self.file_menu_content = ('File', [
            dict(label="New file", entry_type="command",
                 accelerator="Ctrl+N",
                 command=lambda: MenuMethods.new_file(self.text, self.parent)),
            dict(label= "Open...", entry_type="command",
                 accelerator="Ctrl+O",
                 command=lambda: MenuMethods.open(self.text, self.parent)),
            dict(label="Save", entry_type="command", accelerator="Ctrl+S",
                 command=lambda: MenuMethods.save(self.text, self.parent)),
            dict(label="Save as...", entry_type="command",
                 accelerator="Ctrl+Shift+S",
                 command=lambda:MenuMethods.save_as(self.text, self.parent)),
            SEPARATOR,
            dict(label="Exit", entry_type="command",
                 command=lambda:MenuMethods.exit(self.text, self.parent))])
        self.menus.append(self.file_menu_content)
        # Edit menu
        self.edit_menu_content = ("Edit", [
            dict(label="Undo", entry_type="command", accelerator="Ctrl+Z",
                 command=lambda: MenuMethods.undo(self.text)),
            dict(label="Redo", entry_type="command", accelerator="Ctrl+Y",
                 command=lambda: MenuMethods.redo(self.text)),
            SEPARATOR,
            dict(label="Cut", entry_type="command", accelerator="Ctrl+X",
                 command=lambda: MenuMethods.cut(self.text)),
            dict(label="Copy", entry_type="command", accelerator="Ctrl+C",
                 command=lambda: MenuMethods.copy(self.text)),
            dict(label="Paste", entry_type="command", accelerator="Ctrl+V",
                 command=lambda: MenuMethods.paste(self.text)),
            dict(label="Delete", entry_type="command", accelerator="Del",
                 command=lambda: MenuMethods.delete(self.text)),
            SEPARATOR,
            dict(label="Find...", entry_type="command", accelerator="Ctrl+F"),
            dict(label="Find and replace...", entry_type="command",
                 accelerator="Ctrl+Shift+F"),
            dict(label="Find in files...", entry_type="command"),
            dict(label="Go to...", entry_type="command")])
        self.menus.append(self.edit_menu_content)
    # Format menu:
        self.format_menu_content = ("Format", [
            dict(label="Wrap words", entry_type="checkbutton"),
            dict(label="Font...", entry_type="command"),])
        self.menus.append(self.format_menu_content)
    # View menu:
        # TODO
        # Statusbar should be a checkbutton
        self.view_menu_content = ("View", [
            dict(label="Statusbar", entry_type="command")])
        self.menus.append(self.view_menu_content)

    # Help menu
        self.help_menu_content = ("Help", [
            dict(label="Show help...", entry_type="command",
                 command=MenuMethods.show_help),
            dict(label="About", entry_type="command",
                 command=MenuMethods.about)])
        self.menus.append(self.help_menu_content)

        # Lists of commands that should be disabled in
        # specific circumstances
        # TODO:
        # Use build in "postcommand" attribute of the Menu class
        # to configure disabled menu entries when the menu is clicked
        self.disable_on_empty_stack = ["Undo"]
        self.disable_on_empty_selection = ["Cut", "Copy", "Delete"]
        self.disable_on_empty_clipboard = ["Paste"]


class Menubar(tk.Frame, MenuContents):
    """Frame containing menus."""
    # TODO:
    # Menes should "roll" when you click
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        MenuContents.__init__(self)
        # The text attribute from the parent.text assignment is None
        # because menubar created and packed before textspace
        # So self.text will be assigned later by calling _get_text
        # method from the parent class
        self.text = None
        self.parent = parent

        # self.menus inherited from the class MenuContents
        for menu in self.menus:
            make_menu_button(self, menu).pack(side=LEFT)
        self.pack(side=TOP, fill=X)

    def _get_text(self):
        self.text = self.parent.text


class TextSpace(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=YES)

        # Class attributes

        # Attributes for GUI widgets.
        # Assigned values during GUI construction
        self.text = None
        # self.line_numbers = None
        self.x_scrollbar = None
        self.y_scrollbar = None

        self.make_widgits()
        self.config_grid()
        self.config_text()

    def make_widgits(self):
        self.make_text()
        # Currently line numbers disabled
        # self.make_line_numbers()
        self.make_scrollbars()

    def make_line_numbers(self):
        self.line_numbers = LineNumbers(self)
        self.line_numbers.grid(row=0, column=0, sticky=N+S)

    def make_text(self):
        # Should make a class in a future for a text widget
        self.text = tk.Text(self, undo=YES)
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

        self.set_width(30)
        self.write_numbers()

    def set_width(self, width):
        self.config(width=width)

    def write_numbers(self):
        # num_of_lines = self.get_num_of_lines()
        # if num_of_lines > self.num_of_lines:
        self.num_of_lines = self.get_num_of_lines()
        self.text.update()
        self.delete(ALL)

        for n in range(1, self.num_of_lines+1):
            i = "{0}.0".format(n)
            dline = self.text.dlineinfo(i)
            if dline:
                y_pos = dline[1]
                self.create_text(1, y_pos, anchor=N+W, text=n)

        # num_of_digits = len(str(self.num_of_lines))
        # i = self.text.index('@0,0')
        # self.text.update()
        # self.delete(ALL)
        # # Lines indexed from 1, not from 0, that is why the range
        # # function called with (1, n+1)
        # while True:
        #     dline = self.text.dlineinfo(i)
        #     if dline:
        #         y = dline[1]
        #         linenum = i.split('.')[0]
        #         # Rjust doesn't work for some reason
        #         # linenum = linenum.rjust(num_of_digits)
        #         self.create_text(1, y, anchor=N+W, text=linenum)
        #         i = self.text.index('{0}+1line'.format(i))
        #     else:
        #         break

    def get_num_of_lines(self):
        num_of_lines = int(self.text.index(END+'-1l').split('.')[0])
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

    def _update_cursor_position(self):
        """Update cursor position display.
        """
        cursor_pos = self.get_cursor_pos()
        cursor_pos_text = "line {} col {}".format(*cursor_pos)
        self.cursor_position.config(text=cursor_pos_text)


class ContextMenu(tk.Menu):
    def __init__(self, parent=None):
        tk.Menu.__init__(self, parent)
        self.make_context_menu()

        self.context_menu_content = []


if __name__ == '__main__':
    FILENAME = os.path.abspath(__file__)
    TextEditor(file=FILENAME).mainloop()
