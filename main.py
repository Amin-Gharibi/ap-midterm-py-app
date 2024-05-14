import customtkinter as ctk
import tkinter as tk
from modules.headerNavBar import HeaderNavBar

# app width and height
APP_WIDTH = 1200
APP_HEIGHT = 700

# set theme as dark mode
ctk.set_appearance_mode('dark')

# set the color pallet for the app
ctk.set_default_color_theme('green')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # set application title
        self.title("IMDB M.M.")
        # set application sizes
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        # config the column that the header navbar is in it
        self.grid_columnconfigure(0, weight=1)
        # define the header navbar
        header_navbar = HeaderNavBar(master=self)
        header_navbar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')


if __name__ == "__main__":
    app = App()
    app.mainloop()
