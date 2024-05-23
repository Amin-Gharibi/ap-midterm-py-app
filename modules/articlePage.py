import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.commentsSection import CommentsSection
from PIL import Image


class ArticlePage(ctk.CTkScrollableFrame):
    def __init__(self, master, article, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.article = article

        self.configure(fg_color='transparent')
        self.grid_columnconfigure(0, weight=1)

        # header navbar
        header = HeaderNavBar(self, parent_count=4)
        header.grid(row=0, column=0, sticky="ew")

        # page title
        # add space after movie title because the font is italic
        page_title = ctk.CTkLabel(self, text=self.article['title'] + ' ', font=('Arial', 36, 'italic'))
        page_title.grid(row=1, column=0, sticky="ew", pady=(50, 30))

        # Load the image
        image = Image.open(self.article['cover'])

        # Create an image label
        article_cover = ctk.CTkLabel(self, text='', image=ctk.CTkImage(dark_image=image, size=(1000, 600)))
        article_cover.grid(row=2, column=0, sticky='ew')

        # article body
        article_body = ctk.CTkLabel(self, text=self.article['body'], font=('Arial', 14))
        article_body.grid(row=3, column=0, sticky='w', pady=20, padx=90)

        # author label
        author_label = ctk.CTkLabel(self, text='Author', font=('Arial', 14, 'italic'))
        author_label.grid(row=4, column=0, sticky='w', padx=90)

        # container to hold user profile picture and user's name
        author_prof_name_frame = ctk.CTkFrame(self, fg_color='transparent')
        author_prof_name_frame.grid(row=5, column=0, sticky='w', padx=90, pady=10)

        # author profile pic
        image = ctk.CTkImage(dark_image=Image.open(self.article['author']['profilePic']), size=(30, 30))
        author_prof_pic = ctk.CTkLabel(author_prof_name_frame, image=image, text='')
        author_prof_pic.grid(row=0, column=0)

        author_name_role_frame = ctk.CTkFrame(author_prof_name_frame, fg_color='transparent')
        author_name_role_frame.grid(row=0, column=1, padx=(10, 0))

        # author's name
        author_name = ctk.CTkLabel(author_name_role_frame, text=self.article['author']['fullName'],
                                   font=('Arial', 14, 'bold'),
                                   height=10)
        author_name.grid(row=0, column=0)

        # author role
        author_role = ctk.CTkLabel(author_name_role_frame, text=self.article['author']['role'], font=('Arial', 12),
                                   text_color='gray', height=10)
        author_role.grid(row=1, column=0, sticky='w')

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
