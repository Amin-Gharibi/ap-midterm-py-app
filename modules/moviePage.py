from math import ceil
import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.imageSlider import ImageSlider
from modules.itemBoxesContainer import ItemBoxesContainer
from modules.castPage import CastPage
from modules.sectionTitle import SectionTitle
from modules.commentsSection import CommentsSection
from api_services.movies import get_movie_by_id
from api_services.comment import get_page_comments


class MoviePage(ctk.CTkScrollableFrame):
    def __init__(self, master, movie_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.movie = get_movie_by_id(movie_id)['targetMovie']

        self.configure(fg_color='transparent')
        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        # add space after movie title because the font is italic
        page_title = ctk.CTkLabel(self, text=self.movie['fullName'] + ' ', font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # image slider
        image_slider = ImageSlider(self, self.movie['medias'], 'moviesPictures')
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
                                     text=self.movie['summary'],
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
        genre_label = ctk.CTkLabel(genre_frame, text=', '.join(self.movie['genre']), justify='left', anchor='w')
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
        language_label = ctk.CTkLabel(language_frame, text=self.movie['movieLanguage'], justify='left',
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

        self.favorite_status_button = ctk.CTkButton(movie_details_frame, text='Remove From Favorites' if self.movie['isMovieInFavorites'] else 'Add To Favorites', command=self.handle_add_remove_favorite)
        self.favorite_status_button.grid(row=8, column=0, sticky='w', pady=(10, 0))
        if self.movie['isMovieInFavorites']:
            self.favorite_status_button.configure(fg_color='#EF5350', hover_color='#C62828')

        # cast section
        cast_container = ItemBoxesContainer(master=self, target_fg_color=['gray86', 'gray17'],
                                            title='Cast',
                                            container_bg_color=rate_frame.cget('bg_color'),
                                            items=self.movie['cast'],
                                            details_page=CastPage,
                                            target_page_id_container='cast',
                                            base_frame_count=5)
        cast_container.grid(row=5, column=0, sticky='ew')
        cast_container.section_title.grid(pady=0)

        movie_comments = get_page_comments(self.movie['_id'])['pageComments']
        # comments section
        comments_container = CommentsSection(self, movie_comments, page_id=self.movie['_id'], page_type='Movies')
        comments_container.grid(row=6, column=0, sticky='ew')

    def handle_add_remove_favorite(self):
        from CTkMessagebox import CTkMessagebox
        from api_services.auth import get_me

        data = get_me()
        user = data['user'] if data else None
        if user is None:
            CTkMessagebox(title='Attention', message='For Adding Movie To Your Favorites You Need To Login First!')
            return None

        if self.movie['isMovieInFavorites']:
            from api_services.movies import delete_favorite_movie
            operation_result = delete_favorite_movie(self.movie['_id'])
        else:
            from api_services.movies import add_favorite_movie
            operation_result = add_favorite_movie(self.movie['_id'])

        if operation_result['ok']:
            CTkMessagebox(title='Success', message='Movie Deleted From Favorites!' if self.movie['isMovieInFavorites'] else 'Movie Added To Favorites!', icon='check')
            if self.movie['isMovieInFavorites']:
                self.favorite_status_button.configure(text='Add To Favorites', fg_color=['#2CC985', '#2FA572'], hover_color=['#0C955A', '#106A43'])
                self.movie['isMovieInFavorites'] = False
            else:
                self.favorite_status_button.configure(text='Remove From Favorites', fg_color='#EF5350',
                                                      hover_color='#C62828')
                self.movie['isMovieInFavorites'] = True
        else:
            CTkMessagebox(title='Error', message=operation_result['message'], icon='cancel')
