import tkinter
from tkinter import filedialog
import customtkinter as ctk
import requests
from modules.ctktable import CTkTable
from modules.plainInput import PlainInput
from PIL import Image
from api_services.auth import get_me
from api_services.user import update_user
from io import BytesIO
from CTkMessagebox import CTkMessagebox
from utils.util import log_out


class UserDashboard(ctk.CTkFrame):
    def __init__(self, master, second_parent=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # configure page grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.second_parent = second_parent

        self.data = get_me()
        if not self.data:
            from modules.loginForm import LoginForm
            self.destroy()
            LoginForm(self.master).grid(row=0, column=0)

        self.welcome_label = ctk.CTkButton(self, text=f"Welcome Dear {self.data['user']['fullName']} ",
                                           fg_color='transparent', hover_color=self.cget('fg_color'),
                                           font=("Arial", 20, "italic"), command=self.load_main_page)
        self.welcome_label.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

        ctk.CTkButton(self, text='Log Out', command=self.log_out_handler).grid(row=0, column=0, sticky='e', padx=50)

        # frame to hold the header navbar
        navbar_frame = ctk.CTkFrame(self)
        navbar_frame.grid(row=1, column=0, sticky='n', pady=5)

        self.my_profile_button = ctk.CTkButton(navbar_frame, text="My Profile",
                                               command=lambda: self.load_my_profile_tab(dynamic_content_frame))
        self.my_profile_button.grid(row=0, column=0, padx=20, pady=20)

        self.my_comments_button = ctk.CTkButton(navbar_frame, text="My Comments",
                                                command=lambda: self.load_my_comments_tab(dynamic_content_frame))
        self.my_comments_button.grid(row=0, column=1, padx=20, pady=20)

        self.my_favorite_movies_button = ctk.CTkButton(navbar_frame, text="My Favorite Movies",
                                                       command=lambda: self.load_my_favorite_movies_tab(
                                                           dynamic_content_frame, self))
        self.my_favorite_movies_button.grid(row=0, column=2, padx=20, pady=20)

        self.my_articles_button = ctk.CTkButton(navbar_frame, text="My Articles",
                                                         command=lambda: self.load_my_articles_tab(
                                                             dynamic_content_frame, self))
        self.my_articles_button.grid(row=0, column=3, padx=20, pady=20)

        # this frame would contain each tab's content
        dynamic_content_frame = ctk.CTkScrollableFrame(self)
        dynamic_content_frame.grid(row=3, column=0, sticky='nsew')

        # handle its grid system
        dynamic_content_frame.grid_columnconfigure(0, weight=1)
        dynamic_content_frame.grid_columnconfigure(1, weight=1)

        self.load_my_profile_tab(dynamic_content_frame)

    def log_out_handler(self):
        from mainScrollableFrame import MainScrollableFrame
        log_out()
        self.destroy()
        MainScrollableFrame(master=self.master).grid(row=0, column=0, sticky='nsew')

    def select_prof_pic(self):
        self.selected_profile_pic = filedialog.askopenfilename()
        self.prof_image = Image.open(self.selected_profile_pic)
        self.profile_pic_label.configure(image=ctk.CTkImage(dark_image=self.prof_image, size=(300, 300)))

    def load_main_page(self):
        from mainScrollableFrame import MainScrollableFrame
        self.destroy()
        MainScrollableFrame(self.master).grid(row=0, column=0, sticky='nsew')

    def load_my_profile_tab(self, parent, btn_container=None):
        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_profile_button.configure(state='disabled')
        btn_container.my_comments_button.configure(state='normal')
        btn_container.my_favorite_movies_button.configure(state='normal')
        btn_container.my_articles_button.configure(state='normal')
        if hasattr(btn_container, 'users_button'):
            btn_container.users_button.configure(state='normal')
        if hasattr(btn_container, 'movies_button'):
            btn_container.movies_button.configure(state='normal')
        if hasattr(btn_container, 'articles_button'):
            btn_container.articles_button.configure(state='normal')
        if hasattr(btn_container, 'comments_button'):
            btn_container.comments_button.configure(state='normal')
        if hasattr(btn_container, 'casts_button'):
            btn_container.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        # frame to contain left inputs
        left_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        left_content_frame.grid(row=0, column=0, sticky='nw')

        self.email_entry = PlainInput(left_content_frame, "Email:", "Enter your Email Address...")
        self.email_entry.grid(row=0, column=0, sticky='nw', padx=100, pady=(40, 0))
        self.email_entry.input.insert(0, self.data['user']['email'])

        self.username_entry = PlainInput(left_content_frame, "Username:", "Enter your username...")
        self.username_entry.grid(row=1, column=0, sticky='nw', padx=100, pady=20)
        self.username_entry.input.insert(0, self.data['user']['username'])

        self.name_entry = PlainInput(left_content_frame, "Name:", "Enter your name...")
        self.name_entry.grid(row=2, column=0, sticky='nw', padx=100)
        self.name_entry.input.insert(0, self.data['user']['fullName'])

        # frame to contain profile picture and its picker
        right_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        right_content_frame.grid(row=0, column=1, pady=(20, 0))
        right_content_frame.grid_columnconfigure(0, weight=1)

        # Load the image
        res = requests.get(self.data['user']['profilePic'])
        self.prof_image = Image.open(BytesIO(res.content))
        self.profile_pic_label = ctk.CTkLabel(right_content_frame, text="",
                                              image=ctk.CTkImage(dark_image=self.prof_image, size=(300, 300)))
        self.profile_pic_label.grid(row=0, column=0)

        pick_new_profile_button = ctk.CTkButton(right_content_frame, text="Select New Profile",
                                                command=self.select_prof_pic)
        pick_new_profile_button.grid(row=1, column=0, pady=(20, 0))
        self.selected_profile_pic = None

        # update user details submit button
        ctk.CTkButton(parent, text="Save", command=self.update_user).grid(row=1, column=0, columnspan=2, padx=100,
                                                                          pady=40)

        change_password_frame = ctk.CTkFrame(parent, fg_color='transparent')
        change_password_frame.grid(row=2, column=0, columnspan=2, sticky='ew')

        self.current_password_entry = PlainInput(change_password_frame, label_text="Current Password:",
                                                 input_placeholder="Enter Your Current Password...")
        self.current_password_entry.grid(row=0, column=0, sticky='w', padx=100)

        self.new_password_entry = PlainInput(change_password_frame, label_text="New Password:",
                                             input_placeholder="Enter Your New Password...")
        self.new_password_entry.grid(row=1, column=0, sticky='w', padx=100, pady=20)

        ctk.CTkButton(change_password_frame, text="Change Password", command=self.update_password).grid(row=3, column=0,
                                                                                                        padx=100,
                                                                                                        sticky='w',
                                                                                                        pady=(10, 60))

    def update_user(self):
        update_result = update_user(user_id=self.data['user']['_id'], email=self.email_entry.input.get(),
                                    username=self.username_entry.input.get(),
                                    fullName=self.name_entry.input.get(),
                                    profilePic=self.selected_profile_pic)

        if update_result['ok']:
            CTkMessagebox(title="Success", message=update_result['message'], icon='check')
            if self.second_parent:
                self.second_parent.welcome_label.configure(
                    text=f"Welcome Dear {update_result['updatedUser']['fullName']}")
            else:
                self.welcome_label.configure(text=f"Welcome Dear {update_result['updatedUser']['fullName']}")
        else:
            CTkMessagebox(title="Error", message=update_result['message'], icon='cancel')

    def update_password(self):
        update_result = update_user(user_id=self.data['user']['_id'],
                                    currentPassword=self.current_password_entry.input.get(),
                                    updatingPassword=self.new_password_entry.input.get())

        if update_result['ok']:
            msg = CTkMessagebox(title="Success", message=update_result['message'], icon='check')
            res = msg.get()
            from modules.loginForm import LoginForm
            if res.lower() == 'ok':
                log_out()
                if self.second_parent:
                    self.second_parent.destroy()
                self.destroy()
                LoginForm(self.master).grid(row=0, column=0)
        else:
            CTkMessagebox(title="Error", message=update_result['message'], icon='cancel')

    def load_my_comments_tab(self, parent, btn_container=None):
        from modules.comment import Comment
        from modules.sectionTitle import SectionTitle
        from api_services.comment import get_my_comments

        self.my_comments = get_my_comments()['userComments']

        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_comments_button.configure(state='disabled')
        btn_container.my_profile_button.configure(state='normal')
        btn_container.my_favorite_movies_button.configure(state='normal')
        btn_container.my_articles_button.configure(state='normal')
        if hasattr(btn_container, 'users_button'):
            btn_container.users_button.configure(state='normal')
        if hasattr(btn_container, 'movies_button'):
            btn_container.movies_button.configure(state='normal')
        if hasattr(btn_container, 'articles_button'):
            btn_container.articles_button.configure(state='normal')
        if hasattr(btn_container, 'comments_button'):
            btn_container.comments_button.configure(state='normal')
        if hasattr(btn_container, 'casts_button'):
            btn_container.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        SectionTitle(parent, 'My Comments').grid(row=0, column=0, sticky='w', padx=30, pady=10)

        # create each comments template from the backend
        for index, comment in enumerate(self.my_comments):
            Comment(parent, comment, fg_color='gray23', has_reply_btn=False, has_like_label=True,
                    has_delete_btn=True).grid(row=index + 1, column=0, columnspan=2,
                                              sticky='ew',
                                              padx=40, pady=20)

        if not len(self.my_comments):
            ctk.CTkLabel(parent, text='No Comments Yet...', font=('Arial', 16, 'italic'), text_color='gray').grid(row=1,
                                                                                                                  column=0,
                                                                                                                  columnspan=2)
        # did this to access update comments list function without passing parent from another page
        # that it's being called
        parent.update_comments_list_handler = lambda: self.update_comments_list(parent)

    def update_comments_list(self, parent):
        from api_services.comment import get_my_comments
        self.my_comments = get_my_comments()['userComments']
        if not len(self.my_comments):
            ctk.CTkLabel(parent, text='No Comments Yet...', font=('Arial', 16, 'italic'), text_color='gray').grid(row=1,
                                                                                                                  column=0,
                                                                                                                  columnspan=2)

    def load_my_favorite_movies_tab(self, parent, btn_container):
        from modules.itemBox import ItemBox
        from modules.moviePage import MoviePage
        from math import floor
        from modules.sectionTitle import SectionTitle
        from api_services.movies import get_favorite_movies

        favorite_movies = get_favorite_movies()['allFavoriteMovies']

        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_favorite_movies_button.configure(state='disabled')
        btn_container.my_profile_button.configure(state='normal')
        btn_container.my_comments_button.configure(state='normal')
        btn_container.my_articles_button.configure(state='normal')
        if hasattr(btn_container, 'users_button'):
            btn_container.users_button.configure(state='normal')
        if hasattr(btn_container, 'movies_button'):
            btn_container.movies_button.configure(state='normal')
        if hasattr(btn_container, 'articles_button'):
            btn_container.articles_button.configure(state='normal')
        if hasattr(btn_container, 'comments_button'):
            btn_container.comments_button.configure(state='normal')
        if hasattr(btn_container, 'casts_button'):
            btn_container.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        holder_frame = ctk.CTkFrame(parent, fg_color='transparent')
        holder_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        SectionTitle(holder_frame, text="Favorite Movies").grid(row=0, column=0, sticky='w', padx=20)

        for index, movie in enumerate(favorite_movies):
            ItemBox(holder_frame, target_fg_color=['gray86', 'gray17'], details_page=MoviePage, item=movie,
                    target_page_id=movie['movie']['_id'], base_frame_count=6).grid(
                row=floor(index / 4) + 2, column=(index % 4), padx=(40 if (index % 4) == 0 or (index % 4) == 3 else 10),
                pady=10)

        if not len(favorite_movies):
            ctk.CTkLabel(parent, text='No Favorite Movies Yet...', font=('Arial', 16, 'italic'),
                         text_color='gray').grid(row=1, column=0, columnspan=2)

    def select_article_cover(self):
        self.selected_article_cover = filedialog.askopenfilename()
        self.selected_cover_label.configure(text='Cover Selected Successfully!')

    def load_my_articles_tab(self, parent, btn_container):
        from modules.itemBox import ItemBox
        from modules.articlePage import ArticlePage
        from math import floor
        from modules.sectionTitle import SectionTitle
        from api_services.articles import get_favorite_articles, get_my_articles

        favorite_articles = get_favorite_articles()['allFavoriteArticles']
        self.my_articles = get_my_articles()['userArticles']

        # if the function was used from AdminDashboard then change the btn container and disable buttons there
        if btn_container is None:
            btn_container = self

        # disable target tab button and enable other tabs button
        btn_container.my_articles_button.configure(state='disabled')
        btn_container.my_profile_button.configure(state='normal')
        btn_container.my_comments_button.configure(state='normal')
        btn_container.my_favorite_movies_button.configure(state='normal')
        if hasattr(btn_container, 'users_button'):
            btn_container.users_button.configure(state='normal')
        if hasattr(btn_container, 'movies_button'):
            btn_container.movies_button.configure(state='normal')
        if hasattr(btn_container, 'articles_button'):
            btn_container.articles_button.configure(state='normal')
        if hasattr(btn_container, 'comments_button'):
            btn_container.comments_button.configure(state='normal')
        if hasattr(btn_container, 'casts_button'):
            btn_container.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        add_new_article_frame = ctk.CTkFrame(parent, fg_color='transparent')
        add_new_article_frame.grid_columnconfigure((0, 1, 2), weight=1)
        add_new_article_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)
        SectionTitle(add_new_article_frame, text='Add New Article').grid(row=0, column=0, sticky='w', padx=30,
                                                                         pady=(0, 20))
        self.article_title_entry = PlainInput(add_new_article_frame, label_text='Article Title:',
                                              input_placeholder="Enter Article Title...")
        self.article_title_entry.grid(row=1, column=0, sticky='w', padx=45)
        article_body_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
        article_body_frame.grid_columnconfigure(0, weight=1)
        article_body_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=45, pady=10)
        ctk.CTkLabel(article_body_frame, text='Article Body:', text_color='gray',
                     font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        self.article_body_entry = ctk.CTkTextbox(article_body_frame)
        self.article_body_entry.grid(row=1, column=0, sticky='ew')
        self.selected_article_cover = None
        article_cover_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
        article_cover_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(article_cover_frame, text='Article Cover:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(article_cover_frame, text='Add Cover', command=self.select_article_cover).grid(row=1,
                                                                                                     column=0,
                                                                                                     sticky='w')
        self.selected_cover_label = ctk.CTkLabel(article_cover_frame,
                                                 text='Please Select Article Cover')
        self.selected_cover_label.grid(row=0, column=1, padx=20)
        submit_form_buttons_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
        submit_form_buttons_frame.grid(row=4, column=0, columnspan=3, pady=40)
        ctk.CTkButton(submit_form_buttons_frame, text='Create',
                      command=lambda: self.create_article_handler(isPublished=True)).grid(row=0, column=0)
        ctk.CTkButton(submit_form_buttons_frame, text='Save As Draft', fg_color='#EF5350',
                      hover_color='#C62828', command=lambda: self.create_article_handler(isPublished=False)).grid(
            row=0, column=1, padx=30)

        self.my_articles_holder = ctk.CTkFrame(parent, fg_color='transparent')
        self.my_articles_holder.grid(row=1, column=0, sticky='nsew', padx=10, pady=10, columnspan=2)
        SectionTitle(self.my_articles_holder, text='My Articles').pack(anchor='w', padx=20)

        values = [
            ['ID', 'Title', 'Body', 'Rate', 'Status', 'Change Status', 'Edit', 'Delete'],
            *[
                [
                    '...' + article['_id'][-6:],
                    article['title'],
                    article['body'][:20] + '...',
                    article['rate'] or '0',
                    'Published' if article['isPublished'] else 'Not Published',
                    'UnPublish' if article['isPublished'] else 'Publish',
                    'Edit',
                    'Delete'
                ] for article in self.my_articles
            ]
        ]

        self.my_articles_not_found_label = None
        self.my_articles_table = None
        # make these None so if there wasn't table or the label at the beginning and wanted
        # to update the table there would be no need to destroy it
        if len(values) > 1:
            self.my_articles_table = CTkTable(master=self.my_articles_holder, column=8, values=values,
                                              hover=True, column_hover=[5, 6, 7],
                                              not_hover_rows=[0],
                                              command=self.handle_clicking_on_article_table,
                                              column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                              column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'])
            self.my_articles_table.pack(expand=True, fill='both', pady=(10, 0), padx=30)
        else:
            self.my_articles_not_found_label = ctk.CTkLabel(self.my_articles_holder, text='No Articles Yet...',
                                                            font=('Arial', 16, 'italic'),
                                                            text_color='gray')
            self.my_articles_not_found_label.pack()

        favorite_articles_holder = ctk.CTkFrame(parent, fg_color='transparent')
        favorite_articles_holder.grid(row=2, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)
        SectionTitle(favorite_articles_holder, text="Favorite Articles").grid(row=0, column=0, sticky='w', padx=20)

        for index, article in enumerate(favorite_articles):
            ItemBox(master=favorite_articles_holder, target_fg_color=['gray86', 'gray17'], details_page=ArticlePage,
                    item=article, target_page_id=article['article']['_id'], base_frame_count=6).grid(
                row=floor(index / 4) + 2, column=(index % 4),
                padx=(40 if (index % 4) == 0 or (index % 4) == 3 else 10), pady=10)

        if not len(favorite_articles):
            ctk.CTkLabel(parent, text='No Favorite Articles Yet...', font=('Arial', 16, 'italic'),
                         text_color='gray').grid(row=3, column=0, columnspan=2)

    def create_article_handler(self, isPublished):
        from api_services.articles import create_article, get_my_articles

        if not self.article_title_entry.input.get() or not self.article_body_entry.get("1.0",
                                                                                       tkinter.END) or not self.selected_article_cover:
            CTkMessagebox(title='Error', message="Article Fields Can Not Be Empty!", icon='cancel')
            return False

        create_result = create_article(title=self.article_title_entry.input.get(),
                                       body=self.article_body_entry.get("1.0", tkinter.END),
                                       cover=self.selected_article_cover,
                                       isPublished=isPublished)

        if create_result['ok']:
            CTkMessagebox(title='Success', message=f'Article {isPublished and 'Created' or 'Drafted'} Successfully!',
                          icon='check')
            self.update_my_articles_table()
        else:
            message = ""
            for error in create_result['message']:
                message += error['message'] + ', '
            message = message[:-2]
            CTkMessagebox(title='Error', message=message,
                          icon='cancel')

    def update_my_articles_table(self):
        from api_services.articles import get_my_articles

        self.my_articles = get_my_articles()['userArticles']

        values = [
            ['ID', 'Title', 'Body', 'Rate', 'Status', 'Change Status', 'Edit', 'Delete'],
            *[
                [
                    '...' + article['_id'][-6:],
                    article['title'],
                    article['body'][:20] + '...',
                    article['rate'] or '0',
                    'Published' if article['isPublished'] else 'Not Published',
                    'UnPublish' if article['isPublished'] else 'Publish',
                    'Edit',
                    'Delete'
                ] for article in self.my_articles
            ]
        ]

        if self.my_articles_table:
            self.my_articles_table.destroy()
        if self.my_articles_not_found_label:
            self.my_articles_not_found_label.destroy()

        if len(values) > 1:
            self.my_articles_table = CTkTable(master=self.my_articles_holder, column=8, values=values,
                                              hover=True, column_hover=[5, 6, 7],
                                              not_hover_rows=[0],
                                              command=self.handle_clicking_on_article_table,
                                              column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                              column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'])
            self.my_articles_table.pack(expand=True, fill='both', pady=(10, 0), padx=30)
        else:
            self.my_articles_not_found_label = ctk.CTkLabel(self.my_articles_holder, text='No Articles Yet...',
                                                            font=('Arial', 16, 'italic'),
                                                            text_color='gray')
            self.my_articles_not_found_label.pack()

    def handle_clicking_on_article_table(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 5:
                from api_services.articles import change_article_status

                res = change_article_status(article_id=self.my_articles[row - 1]['_id'])
                if res['ok']:
                    CTkMessagebox(title='Success', message="Article Status Updated Successfully!", icon='check')
                    self.update_my_articles_table()
                else:
                    CTkMessagebox(title='Error', message="Error In Changing Article Status!", icon='cancel')
            elif column == 6:
                from modules.editArticleModal import EditArticleModal
                EditArticleModal(self, article_id=self.my_articles[row - 1]['_id'])
            elif column == 7:
                from api_services.articles import delete_article

                res = delete_article(article_id=self.my_articles[row - 1]['_id'])
                if res['ok']:
                    CTkMessagebox(title='Success', message="Article Deleted Successfully!", icon='check')
                    self.update_my_articles_table()
                else:
                    CTkMessagebox(title='Error', message="Error In Deleting Article!", icon='cancel')
