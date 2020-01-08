import tkinter as tk
import os
from tkinter import messagebox
from tkinter import filedialog


class Application(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")

        # self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        # self.quit.pack(side="bottom")
        #
        #
        # self.copy_text = tk.Button(self, text="save", command=self.save_text)
        # self.copy_text.pack(side="top")

        self.text = tk.Text(width=130, height=40,  wrap=tk.WORD)
        self.text.pack(side='left')

        self.scroll = tk.Scrollbar(command=self.text.yview)
        self.scroll.pack(side='left', fill=tk.Y)
        self.text.config(yscrollcommand=self.scroll.set)

        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # file_menu.add_command(label="Save", command=self.save_text)
        # file_menu.add_command(label="Open", command=self.open_file)

        file_menu.add_command(label="Open file", command=self.open_file)
        file_menu.add_command(label="Save file as", command=self.save_file_as)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Exit", command=self.master.destroy)

    # def save_text(self):
    #     s = self.text.get(1.0, tk.END)
    #     with open("new_file.txt", "w") as new_file:
    #         new_file.write(s)
    #
    # def open_file(self):
    #     try:
    #         with open("new_file.txt") as file:
    #             print(file.read())
    #     except FileNotFoundError:
    #         messagebox.showerror("Error", "File doesn't exist!")

    def open_file(self):
        global global_file_name
        global_file_name = filedialog.askopenfilename()

        with open(global_file_name, "r") as file:
             data = file.read()

        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, data)

    def save_file_as(self):
        content = self.text.get(1.0, tk.END)
        file_name = filedialog.asksaveasfilename()
        with open(file_name, "w") as file:
            file.write(content)

    def save_file(self):
        print(global_file_name)
        content = self.text.get(1.0, tk.END)
        with open(global_file_name, "w") as file:
             file.write(content)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rizzrack editor")
    root.iconbitmap('icon.ico')
    app = Application(master=root)
    app.master.minsize(1061, 550)
    app.master.maxsize(1061, 550)
    root.mainloop()
