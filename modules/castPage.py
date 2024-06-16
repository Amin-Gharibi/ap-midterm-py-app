from math import ceil
import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.imageSlider import ImageSlider
from modules.sectionTitle import SectionTitle
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.commentsSection import CommentsSection


class CastPage(ctk.CTkScrollableFrame):
    def __init__(self, master, user, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.user = user

        self.configure(fg_color='transparent')

        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        page_title = ctk.CTkLabel(self, text=user['fullName'], font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # image slider
        image_slider = ImageSlider(self, ['images/imdb_logo.png'])
        image_slider.grid(row=2, column=0)

        user_details_title = SectionTitle(self, 'User Details')
        user_details_title.grid(row=3, column=0, sticky='w', padx=(35, 0), pady=(50, 0))

        # user details frame
        user_details_frame = ctk.CTkFrame(self, fg_color='transparent')
        user_details_frame.grid(row=4, column=0, sticky='ew', padx=50, pady=(30, 50))
        user_details_frame.grid_columnconfigure(0, weight=1)

        # biography title
        biography_title_label = ctk.CTkLabel(user_details_frame, text='Biography:', font=('Arial', 16, 'bold'),
                                             text_color='#78909C')
        biography_title_label.grid(row=0, column=0, sticky='w')

        # biography body label
        biography_label = ctk.CTkLabel(user_details_frame,
                                       text=self.user['biography'],
                                       justify='left', anchor='w')
        biography_label.grid(row=1, column=0, sticky="ew", pady=(5, 0))

        # birth_date temp frame
        birth_date_frame = ctk.CTkFrame(user_details_frame)
        birth_date_frame.configure(fg_color='transparent')
        birth_date_frame.grid(row=2, column=0, sticky='w', pady=(10, 0))

        # birth_date title
        birth_date_title_label = ctk.CTkLabel(birth_date_frame, text='Birth Date:', font=('Arial', 16, 'bold'),
                                              text_color='#78909C')
        birth_date_title_label.grid(row=2, column=0, sticky='w')

        # birth_date body
        birth_date_label = ctk.CTkLabel(birth_date_frame, text=self.user['birthDate'], justify='left', anchor='w')
        birth_date_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # birth_place temp frame
        birth_place_frame = ctk.CTkFrame(user_details_frame)
        birth_place_frame.configure(fg_color='transparent')
        birth_place_frame.grid(row=3, column=0, sticky='w', pady=(10, 0))

        # birth_place title
        birth_place_title_label = ctk.CTkLabel(birth_place_frame, text='Birth Place:', font=('Arial', 16, 'bold'),
                                               text_color='#78909C')
        birth_place_title_label.grid(row=2, column=0, sticky='w')

        # birth_place body
        birth_place_label = ctk.CTkLabel(birth_place_frame, text=self.user['birthPlace'], justify='left', anchor='w')
        birth_place_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # height temp frame
        height_frame = ctk.CTkFrame(user_details_frame)
        height_frame.configure(fg_color='transparent')
        height_frame.grid(row=4, column=0, sticky='w', pady=(10, 0))

        # height title
        height_title_label = ctk.CTkLabel(height_frame, text='Height:', font=('Arial', 16, 'bold'),
                                             text_color='#78909C')
        height_title_label.grid(row=2, column=0, sticky='w')

        # height body
        height_label = ctk.CTkLabel(height_frame, text=f"{self.user['height']} cm", justify='left',
                                       anchor='w')
        height_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        # rate temp frame
        rate_frame = ctk.CTkFrame(user_details_frame)
        rate_frame.configure(fg_color='transparent')
        rate_frame.grid(row=5, column=0, sticky='w', pady=(10, 0))

        # rate title
        rate_title_label = ctk.CTkLabel(rate_frame, text='Rate:', font=('Arial', 16, 'bold'), text_color='yellow')
        rate_title_label.grid(row=2, column=0, sticky='w')

        # rate body
        rate_label = ctk.CTkLabel(rate_frame, text=f"{self.user['rate']} {'⭐' * ceil(self.user['rate'])}", font=('Arial', 14, 'italic'), justify='left',
                                  anchor='w', text_color='yellow')
        rate_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        movies_details = [
            {
                "id": 0,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            },
            {
                "id": 1,
                "title": "After Zendegi",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie.",
                "cover": "images/imdb_logo.png",
                "rate": 4.5
            },
            {
                "id": 2,
                "title": "After Jendegi",
                "description": "This movie is so amazing.",
                "cover": "images/imdb_logo.png",
                "rate": 1.2
            }
        ]

        # format descriptions to add \n each 100 char
        for item in movies_details:
            item["description"] = format_description(item["description"])

        # create latest movies section
        from modules.moviePage import MoviePage
        latest_movies_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                                     title=f'Movies',
                                                     items=movies_details,
                                                     details_page=MoviePage)
        latest_movies_container.grid(row=6, column=0, sticky='ew')

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
        comments_container.grid(row=7, column=0, sticky='ew')
