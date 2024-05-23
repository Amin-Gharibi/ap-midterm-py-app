import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.moviePage import MoviePage
from modules.articlePage import ArticlePage
from modules.castPage import CastPage


class SearchResultsPage(ctk.CTkScrollableFrame):
    def __init__(self, master, searching_text, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.searching_text = searching_text

        self.configure(fg_color=self.cget('bg_color'))
        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        # add space after movie title because the font is italic
        page_title = ctk.CTkLabel(self, text=f'Search Results For:\n{self.searching_text}', font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # example results
        self.movie_results = [
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

        self.article_results = [
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

        self.actor_results = [
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
            }
        ]

        # place movie results
        movie_results_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                                     title='Movies',
                                                     items=self.movie_results,
                                                     details_page=MoviePage)
        movie_results_container.section_title.grid(pady=(20, 0))
        movie_results_container.configure(fg_color='transparent')
        movie_results_container.grid(row=2, column=0, sticky='ew')

        # place article results
        article_results_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                                       title='Articles',
                                                       items=self.article_results,
                                                       details_page=ArticlePage)
        article_results_container.section_title.grid(pady=(20, 0))
        article_results_container.grid(row=3, column=0, sticky='ew', pady=20)

        # place actor results
        actor_results_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                                     title='Actors',
                                                     items=self.actor_results,
                                                     details_page=CastPage)
        actor_results_container.section_title.grid(pady=(20, 0))
        actor_results_container.grid(row=4, column=0, sticky='ew')
