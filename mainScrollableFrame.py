import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.searchBox import SearchBox
from modules.moviePage import MoviePage
from modules.castPage import CastPage
from modules.articlePage import ArticlePage
from api_services.movies import get_latest_movies, get_random_genre_top_rated
from api_services.cast import get_top_rated_cast
from api_services.articles import get_latest_articles


class MainScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master

        # configure background color, so it wouldn't change to a color like navbar fg color
        self.configure(fg_color="gray14")

        # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # define the header navbar
        header_navbar = HeaderNavBar(master=self, parent_count=2)
        header_navbar.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # search section
        search_box = SearchBox(master=self)
        search_box.grid(row=1, column=0, sticky='ew', pady=(30, 10))

        self.latest_movies = get_latest_movies()['latestMovies']
        self.latest_articles = get_latest_articles()['latestArticles']
        result = get_random_genre_top_rated()
        self.random_genre_top_list = result['topMovies']
        self.random_genre_top_list_genre = result.get('genre', None)
        self.top_artists = get_top_rated_cast()['topRated']

        # create latest movies section
        latest_movies_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                     title='Latest Movies',
                                                     items=self.latest_movies,
                                                     details_page=MoviePage)
        latest_movies_container.grid(row=2, column=0, sticky='ew')

        # create random genre top movies section
        random_genre_top_rate_movies_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                                    title=f'{self.random_genre_top_list_genre or '?'} Top Rated Movies',
                                                                    items=self.random_genre_top_list,
                                                                    details_page=MoviePage)
        random_genre_top_rate_movies_container.grid(row=3, column=0, sticky='ew')

        # create latest articles section
        latest_articles_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                       title='Latest Articles',
                                                       items=self.latest_articles,
                                                       details_page=ArticlePage)  # this must be changed later
        latest_articles_container.grid(row=4, column=0, sticky='ew')

        # create top artists section
        top_artists_container = ItemBoxesContainer(master=self, target_fg_color=header_navbar.get_fg_color(),
                                                   title='Top Artists',
                                                   items=self.top_artists,
                                                   details_page=CastPage)
        top_artists_container.grid(row=5, column=0, sticky='ew')
