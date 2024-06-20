import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.moviePage import MoviePage
from modules.articlePage import ArticlePage
from modules.castPage import CastPage
from api_services.universalSearch import universal_search


class SearchResultsPage(ctk.CTkScrollableFrame):
    def __init__(self, master, searching_text, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.searching_text = searching_text
        results = universal_search(self.searching_text)
        self.movie_results = results['movies']
        self.article_results = results['articles']
        self.cast_results = results['castUsers']

        self.configure(fg_color=self.cget('bg_color'))
        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # page title
        # add space after movie title because the font is italic
        page_title = ctk.CTkLabel(self, text=f'Search Results For:\n{self.searching_text}',
                                  font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

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

        # place casts results
        cast_results_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                                    title='Casts',
                                                    items=self.cast_results,
                                                    details_page=CastPage)
        cast_results_container.section_title.grid(pady=(20, 0))
        cast_results_container.grid(row=4, column=0, sticky='ew')
