import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.imageSlider import ImageSlider


class MoviePage(ctk.CTkScrollableFrame):
    def __init__(self, master, movie, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.movie = movie

        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        page_title = ctk.CTkLabel(self, text=movie['title'], font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # image slider
        image_slider = ImageSlider(self, ['images/imdb_logo.png'])
        image_slider.grid(row=2, column=0)


