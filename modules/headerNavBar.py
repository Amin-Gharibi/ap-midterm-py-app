import customtkinter as ctk
import tkinter as tk


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

        # application signup / login button
        self.signInButton = ctk.CTkButton(self, text="Sign Up / Login", height=30,
                                          font=("Arial", 16),
                                          command=self.on_btn_click_handler)
        self.signInButton.pack(side=tk.RIGHT,
                               padx=20, pady=20,
                               anchor='ne')

        # go to movies only page button
        self.goToMoviesButton = ctk.CTkButton(self, text="Movies", width=80,
                                              fg_color='transparent', hover_color=self.cget('fg_color'),
                                              font=("Arial", 18), cursor='hand2')
        self.goToMoviesButton.pack(side=tk.RIGHT,
                                   padx=10, pady=20,
                                   anchor='n')

        # go to articles only page button
        self.goToArticlesButton = ctk.CTkButton(self, text="Articles", width=80,
                                                fg_color='transparent', hover_color=self.cget('fg_color'),
                                                font=("Arial", 18), cursor='hand2')
        self.goToArticlesButton.pack(side=tk.RIGHT,
                                     padx=0, pady=20,
                                     anchor='n')

    def on_btn_click_handler(self):
        from modules.loginForm import LoginForm

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

        # load login page contents
        login_page = LoginForm(master=parent)
        login_page.grid(column=0, row=0)

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
