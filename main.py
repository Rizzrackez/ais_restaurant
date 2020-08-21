import tkinter as tk
from tkinter import filedialog
from tkinter.font import Font
import ctypes
from tkinter import messagebox

from EditorServices import read_config_app, write_config_app


FILE_FORMATS = [('All Files', '*.*'),
                ('Text Documents', '*.txt'),
                ('HTML Documents', '*.html'),
                ('Python Files', '*.py'),
                ('JavaScript Files', '*.js')]

FONT_SIZE = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]


class Editor(tk.Frame):
    """
    Window for creating, editing, saving files.
    Contains a Text widget with a bound Scrollbar and Menu widget with File, Formats, Help fields.
    """
    def __init__(self, master=None, font_family='Constantia', font_size=11):
        super().__init__(master)
        self.open_file_name = ''

        self.font_family = font_family
        self.font_size = font_size

        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.scroll.grid(row=0, column=1, sticky=tk.NW + tk.S)

        self.text = tk.Text(wrap=tk.WORD, yscrollcommand=self.scroll.set)
        self.text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)

        my_font = Font(self.master, family=self.font_family, size=self.font_size)
        self.text.configure(font=my_font)

        self.scroll['command'] = self.text.yview

        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu = tk.Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Create                                  CTRL+N", command=self.create_file)
        file_menu.add_command(label="Open file...                          CTRL+O", command=self.open_file)
        file_menu.add_command(label="Save file as...           CTRL+SHIFT+S", command=self.save_file_as)
        file_menu.add_command(label="Save                                      CTRL+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)

        menu_bar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font...", command=lambda: self.createFontWindow(FontWindow))

        menu_bar.add_command(label="Help", command=self.help_window)

    def createFontWindow(self, _class):
        """Creates a window for setting fonts (class FontWindow)."""
        self.font_window = tk.Toplevel(self.master)
        _class(self.font_window)

    def create_file(self, *args):
        """File creation."""
        current_file_name = filedialog.asksaveasfilename(filetypes=FILE_FORMATS, defaultextension=FILE_FORMATS)
        if current_file_name:
            self.open_file_name = current_file_name
            self.text.delete(1.0, tk.END)
            self.master.title(f"{self.open_file_name.split('/')[-1]} \u2013 AbyssEditor")

            with open(self.open_file_name, "w") as file:
                pass

    def open_file(self, *args):
        """Opens an existing file."""
        current_file_name = filedialog.askopenfilename()
        if current_file_name:
            self.open_file_name = current_file_name
            self.master.title(f"{self.open_file_name.split('/')[-1]} \u2013 AbyssEditor")

        if self.open_file_name:
            with open(self.open_file_name, "r") as file:
                data = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, data)

    def save_file_as(self, *args):
        """Creates a new file and copies the text from Text widget in new file."""
        content = self.text.get(1.0, tk.END)
        current_file_name = filedialog.asksaveasfilename(filetypes=FILE_FORMATS, defaultextension=FILE_FORMATS)
        if current_file_name:
            self.open_file_name = current_file_name
            self.master.title(f"{self.open_file_name.split('/')[-1]} \u2013 AbyssEditor")

        if self.open_file_name:
            with open(self.open_file_name, "w") as file:
                file.write(content)

    def save_file(self, *args):
        """Saves the Text widget value to the current file (self.open_file_name)."""
        if self.open_file_name:
            content = self.text.get(1.0, tk.END)
            with open(self.open_file_name, "w") as file:
                file.write(content)
        else:
            self.save_file_as()

    def help_window(self):
        """Calls up information window."""
        messagebox.showinfo(title='AbyssEditor: information', message=f"Application Information: "
                                                                      f"\n\nFont family: {self.font_family}"
                                                                      f"\nFont size: {self.font_size}"
                                                                      f"\nWindow size (width, height): {self.master.winfo_width()}x{self.master.winfo_height()} px")

    def exit_program(self):
        """Destroy the Editor window and save width, height window and font family, size in config file."""
        write_config_app(self.master.winfo_width(), self.master.winfo_height(), self.font_family, self.font_size)
        self.master.destroy()


class FontWindow:
    """
    Font settings window. Called from Editor.
    Contains a two Listbox widgets with a bound Scrollbar for setting font size and family.
    """
    def __init__(self, master=None):
        self.current_font_family = app.font_family
        self.current_font_size = app.font_size

        self.master = master

        self.master.maxsize(width=370, height=249)  # fixed window size
        self.master.minsize(width=370, height=249)

        self.master.title(f"Font settings")
        self.master.iconbitmap('media/font_settings_icon.ico')
        self.create_widgets()

    def create_widgets(self):
        self.LEFT_INDENT = tk.Label(self.master, text="")
        self.LEFT_INDENT.grid(row=0, column=0, padx=8)

        self.RIGHT_INDENT = tk.Label(self.master, text="")
        self.RIGHT_INDENT.grid(row=0, column=5, padx=8)

        self.font_family_label = tk.Label(self.master, text="Font:")
        self.font_family_label.grid(row=0, column=1, sticky="W", pady=4)

        self.font_family_scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.font_family_scroll.grid(row=1, column=2, sticky=tk.NW + tk.S)

        self.font_size_scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        self.font_size_scroll.grid(row=1, column=4, sticky=tk.NW + tk.S)

        self.font_family_listbox = tk.Listbox(self.master, yscrollcommand=self.font_family_scroll.set)
        self.font_family_listbox.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        font_family_list = tk.font.families()
        self.font_family_listbox.insert(tk.END, *font_family_list)

        self.font_size_label = tk.Label(self.master, text="Size:")
        self.font_size_label.grid(row=0, column=3, sticky="W", pady=4)

        self.font_size_listbox = tk.Listbox(self.master, yscrollcommand=self.font_size_scroll.set)
        self.font_size_listbox.grid(row=1, column=3, sticky=tk.N + tk.S + tk.E + tk.W)
        self.font_size_listbox.insert(tk.END, *FONT_SIZE)

        self.save_font_button_border = tk.Frame(self.master,
                                                highlightbackground="#289BBB",
                                                highlightcolor="#289BBB",
                                                highlightthickness=1,
                                                bd=0)
        self.save_font_button_border.grid(row=2, column=2, pady=14)

        self.cancel_button_border = tk.Frame(self.master,
                                             highlightbackground="#BB4533",
                                             highlightcolor="#BB4533",
                                             highlightthickness=1,
                                             bd=0)
        self.cancel_button_border.grid(row=2, column=3, pady=14)

        self.save_font_button = tk.Button(self.save_font_button_border, text="Save", width=7, height=1, command=self.save_font)
        self.save_font_button.grid(row=2, column=2)

        self.cancel_button = tk.Button(self.cancel_button_border, text='Cancel', width=7, height=1, command=self.destroy_font_window)
        self.cancel_button.grid(row=2, column=3)

        self.font_family_listbox.bind("<<ListboxSelect>>", self.save_font_family)
        self.font_size_listbox.bind("<<ListboxSelect>>", self.save_font_size)
        self.font_family_scroll['command'] = self.font_family_listbox.yview
        self.font_size_scroll['command'] = self.font_size_listbox.yview

    def save_font_family(self, event):
        """Saves the selected value from the font family list (font.families())."""
        try:
            font_list = list(tk.font.families())
            self.current_font_family = font_list[event.widget.curselection()[0]]
        except IndexError:
            pass

    def save_font_size(self, event):
        """Saves the selected value from the font size list (FONT_SIZE)."""
        try:
            self.current_font_size = FONT_SIZE[event.widget.curselection()[0]]
        except IndexError:
            pass

    def save_font(self):
        """Saving the selected font size and family to Editor.font_size, Editor.font_family"""
        app.font_family = self.current_font_family
        app.font_size = self.current_font_size
        my_font = Font(self.master, family=self.current_font_family, size=self.current_font_size)
        app.text.configure(font=my_font)
        self.master.destroy()

    def destroy_font_window(self):
        self.master.destroy()


if __name__ == "__main__":
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    root = tk.Tk()
    root.title(f"Untitled \u2013 AbyssEditor")
    root.iconbitmap('media/editor_icon.ico')

    config_data = read_config_app()  # data from config file
    root.geometry(f"{config_data['window']['width']}x{config_data['window']['height']}")  # resize the editor window to fit the configuration file

    app = Editor(master=root, font_family=config_data["text"]["font_family"], font_size=config_data["text"]["font_size"])

    # configuring Hotkeys
    root.bind('<Control-n>', app.create_file)
    root.bind('<Control-N>', app.create_file)

    root.bind('<Control-o>', app.open_file)
    root.bind('<Control-O>', app.open_file)

    root.bind('<Control-Shift-s>', app.save_file_as)
    root.bind('<Control-Shift-S>', app.save_file_as)

    root.bind('<Control-s>', app.save_file)
    root.bind('<Control-S>', app.save_file)

    root.protocol("WM_DELETE_WINDOW", app.exit_program)

    root.mainloop()
