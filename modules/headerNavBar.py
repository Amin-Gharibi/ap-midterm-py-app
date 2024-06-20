import customtkinter as ctk
import tkinter as tk
from api_services.auth import get_me


class HeaderNavBar(ctk.CTkFrame):
    def __init__(self, master, parent_count, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.parent_count = parent_count

        # application name title label
        self.titleLabel = ctk.CTkButton(self, text="IMDB M.M.", font=("Arial", 28),
                                        fg_color='transparent', hover_color=self.cget('fg_color'),
                                        cursor='hand2', command=self.go_to_home_page_handler)
        self.titleLabel.pack(side=tk.LEFT,
                             padx=20, pady=20,
                             anchor='nw')

        self.data = get_me()

        # application signup / login button
        self.signInButton = ctk.CTkButton(self, text=(self.data and self.data['user']['fullName']) or "Sign Up / Login",
                                          height=30,
                                          font=("Arial", 16),
                                          command=self.on_btn_click_handler)
        self.signInButton.pack(side=tk.RIGHT,
                               padx=20, pady=20,
                               anchor='ne')

        # go to movies only page button
        self.goToMoviesButton = ctk.CTkButton(self, text="Movies", width=80,
                                              fg_color='transparent', hover_color=self.cget('fg_color'),
                                              font=("Arial", 18), cursor='hand2', command=lambda: self.go_to_all_one_type_page('movie'))
        self.goToMoviesButton.pack(side=tk.RIGHT,
                                   padx=10, pady=20,
                                   anchor='n')

        # go to articles only page button
        self.goToArticlesButton = ctk.CTkButton(self, text="Articles", width=80,
                                                fg_color='transparent', hover_color=self.cget('fg_color'),
                                                font=("Arial", 18), cursor='hand2', command=lambda: self.go_to_all_one_type_page('article'))
        self.goToArticlesButton.pack(side=tk.RIGHT,
                                     padx=0, pady=20,
                                     anchor='n')

        # go to casts only page button
        self.goToCastsPageButton = ctk.CTkButton(self, text="Casts", width=80,
                                                 fg_color='transparent', hover_color=self.cget('fg_color'),
                                                 font=("Arial", 18), cursor='hand2', command=lambda: self.go_to_all_one_type_page('cast'))
        self.goToCastsPageButton.pack(side=tk.RIGHT,
                                      padx=0, pady=20,
                                      anchor='n')

    def on_btn_click_handler(self):
        # because the . layout in each page is different, so I get the count that gets me to . and loop over it
        parent = None
        for i in range(self.parent_count):
            if parent:
                parent = parent.master
            else:
                parent = self.master

        # destroy current contents
        for widget in parent.winfo_children():
            widget.destroy()

        if self.data:
            # load profile page
            if self.data['user']['role'] == 'ADMIN':
                from modules.adminDashboard import AdminDashboard

                # load admin dashboard
                AdminDashboard(master=parent).grid(column=0, row=0, sticky='nsew')
            else:
                from modules.userDashboard import UserDashboard

                # load user and critic dashboard
                UserDashboard(master=parent).grid(column=0, row=0, sticky='nsew')

        else:
            from modules.loginForm import LoginForm

            # load login page contents
            LoginForm(master=parent).grid(column=0, row=0)

    def go_to_home_page_handler(self):
        from mainScrollableFrame import MainScrollableFrame

        # because the . layout in each page is different so i get the count that gets me to . and loop over it
        parent = None
        for i in range(self.parent_count):
            if parent:
                parent = parent.master
            else:
                parent = self.master

        # destroy current contents
        for widget in parent.winfo_children():
            widget.destroy()

        home_page = MainScrollableFrame(master=parent)
        home_page.grid(column=0, row=0, sticky='nsew')

    def get_fg_color(self):
        return self.cget('fg_color')


    def go_to_all_one_type_page(self, page_type):
        from modules.allOneTypePage import AllOneTypePage
        parent = None
        # because the . layout in each page is different, so I get the count that gets me to . and loop over it
        for i in range(self.parent_count):
            if parent:
                parent = parent.master
            else:
                parent = self.master

        # destroy current contents
        for widget in parent.winfo_children():
            widget.destroy()

        get_all_items_func = None
        get_all_items_param = None
        search_func = None
        page_title = None
        items_details_page = None
        if page_type == 'movie':
            from api_services.movies import get_all_movies, search_in_movies
            from modules.moviePage import MoviePage
            get_all_items_func = get_all_movies
            get_all_items_param = 'allMovies'
            search_func = search_in_movies
            page_title = 'Movies'
            items_details_page = MoviePage
        elif page_type == 'article':
            from api_services.articles import get_all_published_articles, search_in_articles
            from modules.articlePage import ArticlePage
            get_all_items_func = get_all_published_articles
            get_all_items_param = 'publishedArticles'
            search_func = search_in_articles
            page_title = 'Articles'
            items_details_page = ArticlePage
        elif page_type == 'cast':
            from api_services.cast import get_all_casts, search_cast
            from modules.castPage import CastPage
            get_all_items_func = get_all_casts
            get_all_items_param = 'allCast'
            search_func = search_cast
            page_title = 'Casts'
            items_details_page = CastPage

        AllOneTypePage(parent, get_all_items_func, get_all_items_param, search_func, page_title, items_details_page).grid(row=0, column=0, sticky='nsew')

