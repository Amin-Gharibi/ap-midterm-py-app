import customtkinter as ctk
import tkinter as tk

# app width and height and other static variables
APP_WIDTH = 1200
APP_HEIGHT = 700
APPEARANCE_MODE = 'dark'
COLOR_THEME = 'green'

# set theme as dark mode
ctk.set_appearance_mode(APPEARANCE_MODE)

# set the color pallet for the app
ctk.set_default_color_theme(COLOR_THEME)


class LogInSignUpPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        # set application title
        self.title("IMDB M.M.")
        # set application sizes
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        # config the column that the header navbar is in it
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
