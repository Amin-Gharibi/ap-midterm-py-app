import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from api_services.movies import get_all_movies
from modules.sectionTitle import SectionTitle
from modules.itemBox import ItemBox
from modules.moviePage import MoviePage
from math import floor


class AllMoviesPage(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.all_movies = get_all_movies()['allMovies']

        self.configure(fg_color=self.cget('bg_color'))
        self.grid_columnconfigure((0, 1), weight=1)

        # header navbar
        self.header = HeaderNavBar(self, parent_count=4)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        SectionTitle(self, text='Movies').grid(row=1, column=0, sticky="w", padx=10, pady=(30, 20))

        search_options_frame = ctk.CTkFrame(self, fg_color='transparent')
        search_options_frame.grid(row=1, column=1, sticky="e", padx=15, pady=(30, 20))

        self.search_filter = ctk.CTkComboBox(search_options_frame, values=['Latest Added', 'Top Rated', 'Low Rated'])
        self.search_filter.set('Latest Added')
        self.search_filter.grid(row=0, column=0)

        self.search_query = ctk.CTkEntry(search_options_frame, placeholder_text='Search...', width=150)
        self.search_query.grid(row=0, column=1, padx=10)

        ctk.CTkButton(search_options_frame, text='Go...', width=60, command=self.handle_searching).grid(row=0, column=2)

        self.movies_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.movies_frame.grid(row=2, column=0, columnspan=2, sticky='ew')

        self.load_movies_to_frame()

    def load_movies_to_frame(self):
        for widget in self.movies_frame.winfo_children():
            widget.destroy()

        for index, movie in enumerate(self.all_movies):
            ItemBox(self.movies_frame, target_fg_color=self.header.get_fg_color(), details_page=MoviePage, item=movie, target_page_id='Movies').grid(row=floor(index / 4) + 1, column=(index % 4), padx=(50, 0), pady=(50, 0))

    def handle_searching(self):
        from api_services.movies import search_in_movies

        filter = None
        match self.search_filter.get():
            case 'Latest Added':
                filter = 'LATEST'
            case 'Top Rated':
                filter = 'TOPRATED'
            case 'Low Rated':
                filter = 'LOWRATED'

        self.all_movies = search_in_movies(q=self.search_query.get(), filter=filter)['result']
        self.load_movies_to_frame()