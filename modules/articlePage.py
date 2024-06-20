import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.commentsSection import CommentsSection
from PIL import Image
from api_services.articles import get_article_by_id
from os import getenv
from urllib.parse import urlparse
import requests
from io import BytesIO
from api_services.comment import get_page_comments


class ArticlePage(ctk.CTkScrollableFrame):
    def __init__(self, master, article_id, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.article = get_article_by_id(article_id)['targetArticle']

        self.configure(fg_color='transparent')
        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # page title
        # add space after movie title because the font is italic
        page_title = ctk.CTkLabel(self, text=self.article['title'] + ' ', font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # Load the image
        parsed_url = urlparse(getenv('BASE_URL'))
        image_url = f"{parsed_url.scheme}://{parsed_url.netloc}/articlesCovers/{self.article['cover']}"
        res = requests.get(image_url)
        image = Image.open(BytesIO(res.content))

        # Create an image label
        article_cover = ctk.CTkLabel(self, text='', image=ctk.CTkImage(dark_image=image, size=(1000, 600)))
        article_cover.grid(row=2, column=0, sticky='ew')

        # article body
        article_body = ctk.CTkLabel(self, text=self.article['body'], font=('Arial', 14), anchor='w', justify=ctk.LEFT)
        article_body.grid(row=3, column=0, sticky='w', pady=20, padx=90)

        # author label
        author_label = ctk.CTkLabel(self, text='· Author ', font=('Arial', 14, 'italic'))
        author_label.grid(row=4, column=0, sticky='w', padx=90)

        # container to hold user profile picture and user's name
        author_prof_name_frame = ctk.CTkFrame(self, fg_color='transparent')
        author_prof_name_frame.grid(row=5, column=0, sticky='w', padx=90, pady=10)

        # author profile pic
        image_url = f"{parsed_url.scheme}://{parsed_url.netloc}/usersProfilePictures/{self.article['writer']['profilePic']}"
        res = requests.get(image_url)
        author_image = Image.open(BytesIO(res.content))
        image = ctk.CTkImage(dark_image=author_image, size=(30, 30))
        author_prof_pic = ctk.CTkLabel(author_prof_name_frame, image=image, text='')
        author_prof_pic.grid(row=0, column=0)

        author_name_role_frame = ctk.CTkFrame(author_prof_name_frame, fg_color='transparent')
        author_name_role_frame.grid(row=0, column=1, padx=(10, 0))

        # author's name
        author_name = ctk.CTkLabel(author_name_role_frame, text=self.article['writer']['fullName'],
                                   font=('Arial', 14, 'bold'),
                                   height=10)
        author_name.grid(row=0, column=0)

        # author role
        author_role = ctk.CTkLabel(author_name_role_frame, text=self.article['writer']['role'], font=('Arial', 12),
                                   text_color='gray', height=10)
        author_role.grid(row=1, column=0, sticky='w')

        self.favorite_status_button = ctk.CTkButton(self, text='Remove From Favorites' if self.article['isArticleInFavorites'] else 'Add To Favorites', command=self.handle_add_remove_favorite)
        self.favorite_status_button.grid(row=6, column=0, sticky='w', padx=90, pady=(10, 0))
        if self.article['isArticleInFavorites']:
            self.favorite_status_button.configure(fg_color='#EF5350', hover_color='#C62828')

        page_comments = get_page_comments(self.article['_id'])['pageComments']

        # # comments section
        comments_container = CommentsSection(self, page_comments, page_id=self.article['_id'], page_type='Articles')
        comments_container.grid(row=7, column=0, sticky='ew')

    def handle_add_remove_favorite(self):
        from CTkMessagebox import CTkMessagebox
        from api_services.auth import get_me

        data = get_me()
        user = data['user'] if data else None
        if user is None:
            CTkMessagebox(title='Attention', message='For Adding Article To Your Favorites You Need To Login First!')
            return None

        if self.article['isArticleInFavorites']:
            from api_services.articles import delete_favorite_article
            operation_result = delete_favorite_article(self.article['_id'])
        else:
            from api_services.articles import create_favorite_article
            operation_result = create_favorite_article(self.article['_id'])

        if operation_result['ok']:
            CTkMessagebox(title='Success', message='Article Deleted From Favorites!' if self.article['isArticleInFavorites'] else 'Article Added To Favorites!', icon='check')
            if self.article['isArticleInFavorites']:
                self.favorite_status_button.configure(text='Add To Favorites', fg_color=['#2CC985', '#2FA572'], hover_color=['#0C955A', '#106A43'])
                self.article['isArticleInFavorites'] = False
            else:
                self.favorite_status_button.configure(text='Remove From Favorites', fg_color='#EF5350',
                                                      hover_color='#C62828')
                self.article['isArticleInFavorites'] = True
        else:
            CTkMessagebox(title='Error', message=operation_result['message'], icon='cancel')