import customtkinter as ctk
import tkinter as tk
from modules.headerNavBar import HeaderNavBar
from modules.itemBoxesContainer import ItemBoxesContainer
from utils.util import format_description


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # configure background color, so it wouldn't change to a color like navbar fg color
        self.configure(fg_color=master.cget("bg"))

        # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # define the header navbar
        header_navbar = HeaderNavBar(master=self)
        header_navbar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # sample movies details
        movies_details = [
            {
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            },
            {
                "title": "After Zendegi",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie.",
                "cover": "images/imdb_logo.png",
                "rate": 4.5
            },
            {
                "title": "After Jendegi",
                "description": "This movie is so amazing.",
                "cover": "images/imdb_logo.png",
                "rate": 1.2
            },
            {
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            },
            {
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            },
            {
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            },
            {
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            },
            {
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            }
        ]

        # format descriptions to add \n each 100 char
        for item in movies_details:
            item["description"] = format_description(item["description"])

        # create latest movies section
        latest_movies_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                     items=movies_details)
        latest_movies_container.grid(row=2, column=0, sticky='ew')
