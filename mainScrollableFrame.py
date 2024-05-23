import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.searchBox import SearchBox
from utils.util import format_description
from modules.moviePage import MoviePage
from modules.castPage import CastPage
from modules.articlePage import ArticlePage


class MainScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master

        # configure background color, so it wouldn't change to a color like navbar fg color
        self.configure(fg_color=master.cget("bg"))

        # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # define the header navbar
        header_navbar = HeaderNavBar(master=self, parent_count=2)
        header_navbar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # search section
        search_box = SearchBox(master=self)
        search_box.grid(row=1, column=0, sticky='ew', pady=(30, 10))

        # sample movies details
        movies_details = [
            {
                "id": 0,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 5
            },
            {
                "id": 1,
                "title": "After Zendegi",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie.",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 4.5
            },
            {
                "id": 2,
                "title": "After Jendegi",
                "description": "This movie is so amazing.",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 1.2
            },
            {
                "id": 3,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 5
            },
            {
                "id": 4,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 5
            },
            {
                "id": 5,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 5
            },
            {
                "id": 6,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 5
            },
            {
                "id": 7,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "genre": "romance, comedy",
                "releaseDate": "23/05/2024",
                "countries": "United States Of America, United Arab Emirates",
                "languages": "English(US)",
                "budget": 100_000_000,
                "rate": 5
            }
        ]

        # format descriptions to add \n each 100 char
        for item in movies_details:
            item["description"] = format_description(item["description"])

        # create latest movies section
        latest_movies_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                     title='Latest Movies',
                                                     items=movies_details,
                                                     details_page=MoviePage)
        latest_movies_container.grid(row=2, column=0, sticky='ew')

        articles = [
            {
                "id": 0,
                "title": "Article 1",
                "cover": "images/imdb_logo.png",
                "body": "this is bullshit body dude",
                "author": {
                    "id": 0,
                    "fullName": "MohamadAmin Gharibi",
                    "profilePic": "images/imdb_logo.png",
                    "role": "User"
                },
                "rate": 2
            },
            {
                "id": 0,
                "title": "Article 2",
                "cover": "images/imdb_logo.png",
                "body": "this is kossher body dude",
                "author": {
                    "id": 0,
                    "fullName": "MohamadAmin Gharibi",
                    "profilePic": "images/imdb_logo.png",
                    "role": "User"
                },
                "rate": 4.5
            }
        ]

        # create latest articles section
        latest_articles_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                       title='Latest Articles',
                                                       items=articles,
                                                       details_page=ArticlePage)  # this must be changed later
        latest_articles_container.grid(row=3, column=0, sticky='ew')

        artists_details = [
            {
                "id": 0,
                "profilePic": "images/imdb_logo.png",
                "fullName": "MohamadAmin Gharibi",
                "biography": "",
                "rate": 4.5,
                "height": 178,
                "birthDate": "14/07/2005",
                "birthPlace": "Minab, Hormozgan, Iran"
            },
            {
                "id": 1,
                "profilePic": "images/imdb_logo.png",
                "fullName": "MohamadAmin Gharibi",
                "biography": "",
                "rate": 4.5,
                "height": 178,
                "birthDate": "14/07/2005",
                "birthPlace": "Minab, Hormozgan, Iran"
            },
            {
                "id": 2,
                "profilePic": "images/imdb_logo.png",
                "fullName": "MohamadAmin Gharibi",
                "biography": "",
                "rate": 4.5,
                "height": 178,
                "birthDate": "14/07/2005",
                "birthPlace": "Minab, Hormozgan, Iran"
            },
            {
                "id": 3,
                "profilePic": "images/imdb_logo.png",
                "fullName": "MohamadAmin Gharibi",
                "biography": "",
                "rate": 4.5,
                "height": 178,
                "birthDate": "14/07/2005",
                "birthPlace": "Minab, Hormozgan, Iran"
            }
        ]

        # create top artists section
        top_artists_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                   title='Top Artists',
                                                   items=artists_details,
                                                   details_page=CastPage)
        top_artists_container.grid(row=4, column=0, sticky='ew')
