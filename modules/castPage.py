from math import ceil
import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.imageSlider import ImageSlider
from modules.sectionTitle import SectionTitle
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.commentsSection import CommentsSection
from api_services.cast import get_one_cast, get_cast_movies
from api_services.comment import get_page_comments


class CastPage(ctk.CTkScrollableFrame):
    def __init__(self, master, cast_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.cast = get_one_cast(cast_id)['targetCast']

        self.configure(fg_color='transparent')

        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        page_title = ctk.CTkLabel(self, text=self.cast['fullName'], font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # image slider
        image_slider = ImageSlider(self, self.cast['photos'], image_folder='moviesPictures')
        image_slider.grid(row=2, column=0)

        user_details_title = SectionTitle(self, 'Cast Details')
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
                                       text=self.cast['biography'],
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
        birth_date_label = ctk.CTkLabel(birth_date_frame, text=self.cast['birthDate'], justify='left', anchor='w')
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
        birth_place_label = ctk.CTkLabel(birth_place_frame, text=self.cast['birthPlace'], justify='left', anchor='w')
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
        height_label = ctk.CTkLabel(height_frame, text=f"{self.cast['height']} cm", justify='left',
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
        rate_label = ctk.CTkLabel(rate_frame, text=f"{self.cast['rate']} {'⭐' * ceil(self.cast['rate'])}", font=('Arial', 14, 'italic'), justify='left',
                                  anchor='w', text_color='yellow')
        rate_label.grid(row=2, column=1, sticky="w", padx=(5, 0))

        from modules.moviePage import MoviePage
        cast_movies = get_cast_movies(self.cast['_id'])['castMovies']
        latest_movies_container = ItemBoxesContainer(master=self, target_fg_color=header.get_fg_color(),
                                                     title=f'Movies Acted In',
                                                     items=cast_movies,
                                                     details_page=MoviePage)
        latest_movies_container.grid(row=6, column=0, sticky='ew')

        # comments section
        page_comments = get_page_comments(self.cast['_id'])['pageComments']
        comments_container = CommentsSection(self, page_comments, page_id=self.cast['_id'], page_type='CastUsers')
        comments_container.grid(row=7, column=0, sticky='ew')
