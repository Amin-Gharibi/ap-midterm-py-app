import customtkinter as ctk
from dotenv import load_dotenv
import utils.util
from mainScrollableFrame import MainScrollableFrame
from modules.userDashboard import UserDashboard
from modules.adminDashboard import AdminDashboard
from api_services.auth import login, validate_login_otp

# static variables
APPEARANCE_MODE = 'dark'
COLOR_THEME = 'green'

# set theme as dark mode
ctk.set_appearance_mode(APPEARANCE_MODE)

# set the color pallet for the app
ctk.set_default_color_theme(COLOR_THEME)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        load_dotenv()

        # set application title
        self.title("IMDB M.M.")
        # make application full size
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        # config the column that the header navbar is in it
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # contents must scroll, so they all are in the main scrollable frame
        self.main_page_content = MainScrollableFrame(master=self)
        self.main_page_content.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()
