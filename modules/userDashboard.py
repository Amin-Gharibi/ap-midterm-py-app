from tkinter import filedialog
import customtkinter as ctk
from modules.plainInput import PlainInput
from PIL import Image


class UserDashboard(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # configure page grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        welcome_label = ctk.CTkLabel(self, text="Welcome Dear MohamadAmin Gharibi ", font=("Arial", 20, "italic"))
        welcome_label.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

        # frame to hold the header navbar
        navbar_frame = ctk.CTkFrame(self)
        navbar_frame.grid(row=1, column=0, sticky='n', pady=5)

        self.my_profile_button = ctk.CTkButton(navbar_frame, text="My Profile", command=lambda: self.load_my_profile_tab(dynamic_content_frame))
        self.my_profile_button.grid(row=0, column=0, padx=20, pady=20)

        self.my_comments_button = ctk.CTkButton(navbar_frame, text="My Comments", command=lambda: self.load_my_comments_tab(dynamic_content_frame))
        self.my_comments_button.grid(row=0, column=1, padx=20, pady=20)

        self.my_favorite_movies_button = ctk.CTkButton(navbar_frame, text="My Favorite Movies", command=lambda: self.load_my_favorite_movies_tab(dynamic_content_frame))
        self.my_favorite_movies_button.grid(row=0, column=2, padx=20, pady=20)

        self.my_favorite_articles_button = ctk.CTkButton(navbar_frame, text="My Favorite Articles", command=lambda: self.load_my_favorite_articles_tab(dynamic_content_frame))
        self.my_favorite_articles_button.grid(row=0, column=3, padx=20, pady=20)

        # this frame would contain each tab's content
        dynamic_content_frame = ctk.CTkScrollableFrame(self)
        dynamic_content_frame.grid(row=3, column=0, sticky='nsew')

        # handle its grid system
        dynamic_content_frame.grid_columnconfigure(0, weight=1)
        dynamic_content_frame.grid_columnconfigure(1, weight=1)

        self.load_my_profile_tab(dynamic_content_frame)

    def select_file(self):
        file_name = filedialog.askopenfilename()
        print(file_name)
        return file_name

    def load_my_profile_tab(self, parent, btn_container=None):
        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_profile_button.configure(state='disabled')
        btn_container.my_comments_button.configure(state='normal')
        btn_container.my_favorite_movies_button.configure(state='normal')
        btn_container.my_favorite_articles_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        # frame to contain left inputs
        left_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        left_content_frame.grid(row=0, column=0, sticky='nw')

        username_entry = PlainInput(left_content_frame, "Username:", "Enter your username...")
        username_entry.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

        name_entry = PlainInput(left_content_frame, "Name:", "Enter your name...")
        name_entry.grid(row=1, column=0, sticky='nw', padx=20)

        phone_number_entry = PlainInput(left_content_frame, "Phone Number:", "Enter your phone number...")
        phone_number_entry.grid(row=2, column=0, sticky='nw', padx=20, pady=20)

        # frame to contain profile picture and its picker
        right_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        right_content_frame.grid(row=0, column=1, pady=(20, 0))
        right_content_frame.grid_columnconfigure(0, weight=1)

        # Load the image
        image = Image.open('images/imdb_logo.png')
        profile_pic_label = ctk.CTkLabel(right_content_frame, text="",
                                         image=ctk.CTkImage(dark_image=image, size=(300, 300)))
        profile_pic_label.grid(row=0, column=0)

        pick_new_profile_button = ctk.CTkButton(right_content_frame, text="Select New Profile",
                                                command=self.select_file)
        pick_new_profile_button.grid(row=1, column=0, pady=(20, 0))

    def load_my_comments_tab(self, parent, btn_container=None):
        from modules.comment import Comment
        from modules.sectionTitle import SectionTitle

        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_comments_button.configure(state='disabled')
        btn_container.my_profile_button.configure(state='normal')
        btn_container.my_favorite_movies_button.configure(state='normal')
        btn_container.my_favorite_articles_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        comments = [
            {
                'user': {
                    'name': 'MohamadAmin Gharibi',
                    'profile_pic': "images/imdb_logo.png",
                    'role': 'User'
                },
                'body': 'hello world this is test first comment',
                'rate': 7.5,
                'responds': [
                    {
                        'user': {
                            'name': 'MohamadAmin Gharibi',
                            'profile_pic': "images/imdb_logo.png",
                            'role': 'User'
                        },
                        'body': "hello world this is reply first test comment. isn't the UI beautiful? :)"
                    }
                ]
            },
            {
                'user': {
                    'name': 'RFE',
                    'profile_pic': "images/imdb_logo.png",
                    'role': 'User'
                },
                'body': 'hello world i am gay and this movie is the best of the best',
                'rate': 1,
                'responds': [
                    {
                        'user': {
                            'name': 'MohamadAmin Gharibi',
                            'profile_pic': "images/imdb_logo.png",
                            'role': 'User'
                        },
                        'body': "koskholo nega 😂"
                    }
                ]
            }
        ]

        SectionTitle(parent, 'My Comments').grid(row=0, column=0, sticky='w', padx=20)

        # create each comments template from the backend
        for index, comment in enumerate(comments):
            Comment(parent, comment, fg_color='gray23').grid(row=index+1, column=0, columnspan=2, sticky='ew', padx=40, pady=20)

    def load_my_favorite_movies_tab(self, parent, btn_container):
        from modules.itemBox import ItemBox
        from modules.moviePage import MoviePage
        from math import floor
        from modules.sectionTitle import SectionTitle

        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_favorite_movies_button.configure(state='disabled')
        btn_container.my_profile_button.configure(state='normal')
        btn_container.my_comments_button.configure(state='normal')
        btn_container.my_favorite_articles_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

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

        holder_frame = ctk.CTkFrame(parent, fg_color='transparent')
        holder_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        SectionTitle(holder_frame, text="Favorite Movies").grid(row=0, column=0, sticky='w', padx=20)

        for index, movie in enumerate(movies_details):
            ItemBox(holder_frame, target_fg_color=['gray86', 'gray17'], details_page=MoviePage, item=movie).grid(row=floor(index / 4) + 2, column=(index % 4), padx=(40 if (index % 4) == 0 or (index % 4) == 3 else 10), pady=10)

    def load_my_favorite_articles_tab(self, parent, btn_container):
        from modules.itemBox import ItemBox
        from modules.articlePage import ArticlePage
        from math import floor
        from modules.sectionTitle import SectionTitle

        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_favorite_articles_button.configure(state='disabled')
        btn_container.my_profile_button.configure(state='normal')
        btn_container.my_comments_button.configure(state='normal')
        btn_container.my_favorite_movies_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        is_admin = True

        if not is_admin:
            add_new_article_frame = ctk.CTkFrame(parent, fg_color='transparent')
            add_new_article_frame.grid_columnconfigure((0, 1, 2), weight=1)
            add_new_article_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)

            SectionTitle(add_new_article_frame, text='Add New Article').grid(row=0, column=0, sticky='w', padx=30,
                                                                             pady=(0, 20))

            title_input = PlainInput(add_new_article_frame, label_text='Article Title:',
                                     input_placeholder="Enter Article Title...")
            title_input.grid(row=1, column=0, sticky='w', padx=45)

            article_body_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
            article_body_frame.grid_columnconfigure(0, weight=1)
            article_body_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=45, pady=10)
            ctk.CTkLabel(article_body_frame, text='Article Body:', text_color='gray',
                         font=("Arial", 12, 'italic')).grid(
                row=0, column=0, sticky='w')
            article_body_input = ctk.CTkTextbox(article_body_frame)
            article_body_input.grid(row=1, column=0, sticky='ew')

            article_cover = None
            article_cover_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
            article_cover_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
            ctk.CTkLabel(article_cover_frame, text='Article Cover:', text_color='gray',
                         font=("Arial", 12, "italic")).grid(
                row=0, column=0, sticky='w')
            ctk.CTkButton(article_cover_frame, text='Add Cover', command=self.select_file).grid(row=1, column=0,
                                                                                                sticky='w')
            selected_cover_count_label = ctk.CTkLabel(article_cover_frame,
                                                      text=article_cover and 'Article Cover Has Been Selected!' or 'Please Select Article Cover')
            selected_cover_count_label.grid(row=0, column=1, padx=20)

            submit_form_buttons_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
            submit_form_buttons_frame.grid(row=4, column=0, columnspan=3, pady=40)
            ctk.CTkButton(submit_form_buttons_frame, text='Create').grid(row=0, column=0)
            ctk.CTkButton(submit_form_buttons_frame, text='Save As Draft', fg_color='#EF5350',
                          hover_color='#C62828').grid(
                row=0, column=1, padx=30)

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

        holder_frame = ctk.CTkFrame(parent, fg_color='transparent')
        holder_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        SectionTitle(holder_frame, text="Favorite Articles").grid(row=0, column=0, sticky='w', padx=20)

        for index, article in enumerate(articles):
            ItemBox(master=holder_frame, target_fg_color=['gray86', 'gray17'], details_page=ArticlePage, item=article).grid(row=floor(index / 4) + 2, column=(index % 4), padx=(40 if (index % 4) == 0 or (index % 4) == 3 else 10), pady=10)
