from math import ceil
import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.imageSlider import ImageSlider
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.castPage import CastPage
from modules.sectionTitle import SectionTitle
from modules.commentsSection import CommentsSection


class MoviePage(ctk.CTkScrollableFrame):
    def __init__(self, master, movie, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.movie = movie

        self.configure(fg_color='transparent')
        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        # add space after movie title because the font is italic
        page_title = ctk.CTkLabel(self, text=self.movie['title'] + ' ', font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # image slider
        image_slider = ImageSlider(self, ['images/imdb_logo.png'])
        image_slider.grid(row=2, column=0)

        movie_details_title = SectionTitle(self, 'Movie Details')
        movie_details_title.grid(row=3, column=0, sticky='w', padx=(35, 0), pady=(50, 0))

        # movie details frame
        movie_details_frame = ctk.CTkFrame(self, fg_color='transparent')
        movie_details_frame.grid(row=4, column=0, sticky='ew', padx=50, pady=(30, 50))
        movie_details_frame.grid_columnconfigure(0, weight=1)

        # summary title
        summary_title_label = ctk.CTkLabel(movie_details_frame, text='Movie Summary:', font=('Arial', 16, 'bold'),
                                           text_color='#78909C')
        summary_title_label.grid(row=0, column=0, sticky='w')

        # summary body label
        summary_label = ctk.CTkLabel(movie_details_frame,
                                     text=self.movie['description'],
                                     justify='left', anchor='w')
        summary_label.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        # genre temp frame
        genre_frame = ctk.CTkFrame(movie_details_frame)
        genre_frame.configure(fg_color='transparent')
        genre_frame.grid(row=2, column=0, sticky='w', pady=(10, 0))

        # genre title
        genre_title_label = ctk.CTkLabel(genre_frame, text='Genre:', font=('Arial', 16, 'bold'), text_color='#78909C')
        genre_title_label.grid(row=2, column=0, sticky='w')

        # genre body
        genre_label = ctk.CTkLabel(genre_frame, text=self.movie['genre'], justify='left', anchor='w')
        genre_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # release date temp frame
        release_date_frame = ctk.CTkFrame(movie_details_frame)
        release_date_frame.configure(fg_color='transparent')
        release_date_frame.grid(row=3, column=0, sticky='w', pady=(10, 0))

        # release date title
        release_date_title_label = ctk.CTkLabel(release_date_frame, text='Release Date:', font=('Arial', 16, 'bold'),
                                                text_color='#78909C')
        release_date_title_label.grid(row=2, column=0, sticky='w')

        # release date body
        release_date_label = ctk.CTkLabel(release_date_frame, text=self.movie['releaseDate'], justify='left', anchor='w')
        release_date_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # countries temp frame
        countries_frame = ctk.CTkFrame(movie_details_frame)
        countries_frame.configure(fg_color='transparent')
        countries_frame.grid(row=4, column=0, sticky='w', pady=(10, 0))

        # countries title
        countries_title_label = ctk.CTkLabel(countries_frame, text='Countries:', font=('Arial', 16, 'bold'),
                                             text_color='#78909C')
        countries_title_label.grid(row=2, column=0, sticky='w')

        # countries body
        countries_label = ctk.CTkLabel(countries_frame, text=self.movie['countries'], justify='left',
                                       anchor='w')
        countries_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # language temp frame
        language_frame = ctk.CTkFrame(movie_details_frame)
        language_frame.configure(fg_color='transparent')
        language_frame.grid(row=5, column=0, sticky='w', pady=(10, 0))

        # language title
        language_title_label = ctk.CTkLabel(language_frame, text='Languages:', font=('Arial', 16, 'bold'),
                                            text_color='#78909C')
        language_title_label.grid(row=2, column=0, sticky='w')

        # language body
        language_label = ctk.CTkLabel(language_frame, text=self.movie['languages'], justify='left',
                                      anchor='w')
        language_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # budget temp frame
        budget_frame = ctk.CTkFrame(movie_details_frame)
        budget_frame.configure(fg_color='transparent')
        budget_frame.grid(row=6, column=0, sticky='w', pady=(10, 0))

        # budget title
        budget_title_label = ctk.CTkLabel(budget_frame, text='Budget:', font=('Arial', 16, 'bold'),
                                          text_color='#78909C')
        budget_title_label.grid(row=2, column=0, sticky='w')

        # budget body
        budget_label = ctk.CTkLabel(budget_frame, text=f"{'{:,}'.format(self.movie['budget'])} $", justify='left',
                                    anchor='w')
        budget_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # rate temp frame
        rate_frame = ctk.CTkFrame(movie_details_frame)
        rate_frame.configure(fg_color='transparent')
        rate_frame.grid(row=7, column=0, sticky='w', pady=(10, 0))

        # rate title
        rate_title_label = ctk.CTkLabel(rate_frame, text='Rate:', font=('Arial', 16, 'bold'), text_color='yellow')
        rate_title_label.grid(row=2, column=0, sticky='w')

        # rate body
        rate_label = ctk.CTkLabel(rate_frame, text=f"{self.movie['rate']} {'⭐' * ceil(self.movie['rate'])}", font=('Arial', 14, 'italic'), justify='left',
                                  anchor='w', text_color='yellow')
        rate_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        artists_details = [
            {
                "id": 0,
                "cover": "images/imdb_logo.png",
                "title": "MohamadAmin Gharibi",
                "description": "",
                "rate": 4.5
            },
            {
                "id": 1,
                "cover": "images/imdb_logo.png",
                "title": "MohamadAmin Gharibi",
                "description": "",
                "rate": 4.5
            },
            {
                "id": 2,
                "cover": "images/imdb_logo.png",
                "title": "MohamadAmin Gharibi",
                "description": "",
                "rate": 4.5
            },
            {
                "id": 3,
                "cover": "images/imdb_logo.png",
                "title": "MohamadAmin Gharibi",
                "description": "",
                "rate": 4.5
            },
            {
                "id": 2,
                "cover": "images/imdb_logo.png",
                "title": "MohamadAmin Gharibi",
                "description": "",
                "rate": 4.5
            },
            {
                "id": 3,
                "cover": "images/imdb_logo.png",
                "title": "MohamadAmin Gharibi",
                "description": "",
                "rate": 4.5
            }
        ]

        # cast section
        cast_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                            title='Cast',
                                            container_bg_color=rate_frame.cget('bg_color'),
                                            items=artists_details,
                                            details_page=CastPage)
        cast_container.grid(row=5, column=0, sticky='ew')
        cast_container.section_title.grid(pady=0)

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

        # comments section
        comments_container = CommentsSection(self, comments)
        comments_container.grid(row=6, column=0, sticky='ew')
