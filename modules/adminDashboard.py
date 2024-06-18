import tkinter
from tkinter import filedialog
import customtkinter as ctk
from modules.userDashboard import UserDashboard
from modules.sectionTitle import SectionTitle
from modules.ctktable import *
from api_services.auth import get_me
from CTkMessagebox import CTkMessagebox


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        user_dashboard = UserDashboard(master=None, second_parent=self)

        # configure page grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.data = get_me()
        if not self.data:
            from modules.loginForm import LoginForm
            self.destroy()
            LoginForm(self.master).grid(row=0, column=0)


        self.welcome_label = ctk.CTkButton(self, text=f"Welcome Dear {self.data['user']['fullName']} ",
                                           fg_color='transparent', hover_color=self.cget('fg_color'),
                                           font=("Arial", 20, "italic"), command=user_dashboard.load_main_page)
        self.welcome_label.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

        ctk.CTkButton(self, text='Log Out', command=user_dashboard.log_out_handler).grid(row=0, column=0, sticky='e',
                                                                                         padx=50)

        # frame to hold the header navbar
        navbar_frame = ctk.CTkScrollableFrame(self, orientation='horizontal', height=60, width=800)
        navbar_frame.grid(row=1, column=0, sticky='n', pady=5)

        self.my_profile_button = ctk.CTkButton(navbar_frame, text="My Profile",
                                               command=lambda: user_dashboard.load_my_profile_tab(dynamic_content_frame,
                                                                                                  self),
                                               state='disabled')
        self.my_profile_button.grid(row=0, column=0, padx=20, pady=20)

        self.my_comments_button = ctk.CTkButton(navbar_frame, text="My Comments",
                                                command=lambda: user_dashboard.load_my_comments_tab(
                                                    dynamic_content_frame, self))
        self.my_comments_button.grid(row=0, column=1, padx=20, pady=20)

        self.my_favorite_movies_button = ctk.CTkButton(navbar_frame, text="My Favorite Movies",
                                                       command=lambda: user_dashboard.load_my_favorite_movies_tab(
                                                           dynamic_content_frame, self))
        self.my_favorite_movies_button.grid(row=0, column=2, padx=20, pady=20)

        self.my_favorite_articles_button = ctk.CTkButton(navbar_frame, text="My Articles",
                                                         command=lambda: user_dashboard.load_my_favorite_articles_tab(
                                                             dynamic_content_frame, self))
        self.my_favorite_articles_button.grid(row=0, column=3, padx=20, pady=20)

        self.users_button = ctk.CTkButton(navbar_frame, text="Users",
                                          command=lambda: self.load_users_tab(dynamic_content_frame))
        self.users_button.grid(row=0, column=4, padx=20, pady=20)

        self.movies_button = ctk.CTkButton(navbar_frame, text="Movies",
                                           command=lambda: self.load_movies_tab(dynamic_content_frame))
        self.movies_button.grid(row=0, column=5, padx=20, pady=20)

        self.casts_button = ctk.CTkButton(navbar_frame, text="Casts",
                                          command=lambda: self.load_casts_tab(dynamic_content_frame))
        self.casts_button.grid(row=0, column=6, padx=20, pady=20)

        self.articles_button = ctk.CTkButton(navbar_frame, text="Articles",
                                             command=lambda: self.load_articles_tab(dynamic_content_frame))
        self.articles_button.grid(row=0, column=7, padx=20, pady=20)

        self.comments_button = ctk.CTkButton(navbar_frame, text="Comments",
                                             command=lambda: self.load_comments_tab(dynamic_content_frame))
        self.comments_button.grid(row=0, column=8, padx=20, pady=20)

        # this frame would contain each tab's content
        dynamic_content_frame = ctk.CTkScrollableFrame(self)
        dynamic_content_frame.grid(row=3, column=0, sticky='nsew')
        # handle its grid system
        dynamic_content_frame.grid_columnconfigure((0, 1), weight=1)

        user_dashboard.load_my_profile_tab(dynamic_content_frame)

    def load_users_tab(self, parent):
        from modules.plainInput import PlainInput
        from api_services.user import get_all_users, get_users_wait_list

        self.all_users = get_all_users()
        self.wait_list_users = get_users_wait_list()
        if self.all_users['ok']:
            self.all_users = self.all_users['users']
        if self.wait_list_users['ok']:
            self.wait_list_users = self.wait_list_users['waitListUsers']

        # disable target tab button and enable other tabs button
        self.users_button.configure(state='disabled')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.movies_button.configure(state='normal')
        self.articles_button.configure(state='normal')
        self.comments_button.configure(state='normal')
        self.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        # add new user form frame
        add_new_user_frame = ctk.CTkFrame(parent, fg_color='transparent')
        add_new_user_frame.grid_columnconfigure((0, 1, 2), weight=1)
        add_new_user_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        add_new_user_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=20, pady=20)

        SectionTitle(add_new_user_frame, text='Add New User ').grid(row=0, column=0, sticky='w', padx=10, pady=(0, 10))

        self.email_entry = PlainInput(master=add_new_user_frame, label_text='Email:',
                                      input_placeholder="Enter user's Email Address...")
        self.email_entry.grid(row=1, column=0)

        self.username_entry = PlainInput(master=add_new_user_frame, label_text='Username:',
                                         input_placeholder="Enter user's Username...")
        self.username_entry.grid(row=1, column=1)

        self.password_entry = PlainInput(master=add_new_user_frame, label_text='Password:',
                                         input_placeholder="Enter user's Password...")
        self.password_entry.grid(row=1, column=2)

        self.full_name_entry = PlainInput(master=add_new_user_frame, label_text='Full Name:',
                                          input_placeholder="Enter user's Full Name...")
        self.full_name_entry.grid(row=2, column=0, pady=10)

        role_frame = ctk.CTkFrame(add_new_user_frame, fg_color='transparent')
        role_frame.grid(row=2, column=1, pady=10)
        ctk.CTkLabel(role_frame, text="Role:", text_color='gray', font=("Arial", 12, 'italic')).grid(row=0, column=0,
                                                                                                     sticky='nw')
        self.role_entry = ctk.CTkOptionMenu(role_frame, width=300, height=40, values=["ADMIN", "USER", "CRITIC"],
                                            fg_color=['#F9F9FA', '#343638'])
        self.role_entry.set("Choose user's Role...")
        self.role_entry.grid(row=1, column=0, sticky='ew')

        add_new_user_submit_btn = ctk.CTkButton(add_new_user_frame, text='Submit', height=30,
                                                command=self.handle_creating_user)
        add_new_user_submit_btn.grid(row=3, column=1, pady=(10, 0))

        wait_list_values = [
            ['ID', 'Email', 'Username', 'Full Name', 'Role', 'Approve', 'Reject'],
            *[
                [
                    '...' + user['_id'][-6:],
                    user['email'],
                    user['username'],
                    user['fullName'],
                    user['role'],
                    'Approve',
                    'Reject'
                ] for user in self.wait_list_users
            ]
        ]

        all_users_values = [
            ['ID', 'Email', 'Username', 'Full Name', 'Role', 'Edit', 'Delete', 'Ban'],
            *[
                [
                    '...' + user['_id'][-6:],
                    user['email'],
                    user['username'],
                    user['fullName'],
                    user['role'],
                    'Edit',
                    'Delete',
                    'Ban' if not user['isBanned'] else 'UnBan'
                ] for user in self.all_users
            ]
        ]

        # list of users waiting to be approved
        self.users_waiting_list_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.users_waiting_list_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=20, pady=(50, 0))
        SectionTitle(self.users_waiting_list_frame, text="Users Wait-List").pack(anchor='w')
        self.users_wait_list_table = None
        self.users_wait_list_not_found_label = None
        if len(wait_list_values) > 1:
            self.users_wait_list_table = CTkTable(master=self.users_waiting_list_frame, column=7,
                                                  values=wait_list_values,
                                                  command=self.handle_approving_user, hover=True, column_hover=[5, 6],
                                                  not_hover_rows=[0],
                                                  column_hover_text_color=['#F57C00', '#F57C00'],
                                                  column_hover_bg_color=['#1B5E20', '#B71C1C'])
            self.users_wait_list_table.pack(expand=True, fill='both', pady=(10, 0))
        else:
            self.users_wait_list_not_found_label = ctk.CTkLabel(self.users_waiting_list_frame,
                                                                text='No Users In Wait List...',
                                                                font=('Arial', 16, 'italic'),
                                                                text_color='gray')
            self.users_wait_list_not_found_label.pack()

        # list of all users
        self.all_users_table_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.all_users_table_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=20, pady=(50, 0))
        temp_frame = ctk.CTkFrame(self.all_users_table_frame, fg_color='transparent')
        temp_frame.pack(expand=True, fill='x')
        SectionTitle(temp_frame, text='All Users').pack(side=tkinter.LEFT)
        search_box_frame = ctk.CTkFrame(temp_frame, fg_color='transparent')
        search_box_frame.pack(side=tkinter.RIGHT)
        self.all_users_search_box_entry = ctk.CTkEntry(search_box_frame, placeholder_text='Search here...', width=200)
        self.all_users_search_box_entry.grid(row=0, column=0, padx=10)
        ctk.CTkButton(search_box_frame, text='Go!', width=60, command=self.handle_searching_in_users).grid(row=0,
                                                                                                           column=1)
        self.all_users_table = None
        self.all_users_not_found_label = None
        if len(all_users_values) > 1:
            self.all_users_table = CTkTable(master=self.all_users_table_frame,
                                            values=all_users_values,
                                            command=self.handle_all_users_funcs, hover=True, column_hover=[5, 6, 7],
                                            not_hover_rows=[0],
                                            column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                            column_hover_bg_color=['#1B5E20', '#B71C1C', '#B71C1C'])
            self.all_users_table.pack(expand=True, fill='both', pady=(10, 0))
        else:
            self.all_users_not_found_label = ctk.CTkLabel(self.all_users_table_frame,
                                                          text='No Users Yet...',
                                                          font=('Arial', 16, 'italic'),
                                                          text_color='gray')
            self.all_users_not_found_label.pack()

    def handle_creating_user(self):
        from api_services.auth import admin_register_user
        create_result = admin_register_user(
            fullName=self.full_name_entry.input.get(),
            username=self.username_entry.input.get(),
            email=self.email_entry.input.get(),
            password=self.password_entry.input.get(),
            role=self.role_entry.get()
        )
        if create_result['ok']:
            CTkMessagebox(title='Success', message='User Created Successfully!', icon='check')
            self.update_users_wait_list_table()
        else:
            CTkMessagebox(title='Error', message=create_result['message'], icon='cancel')

    def handle_searching_in_users(self):
        from api_services.user import search_user
        search_result = search_user(self.all_users_search_box_entry.get())
        if search_result['ok']:
            self.update_all_users_table(search_result=search_result['result'])
        else:
            CTkMessagebox(title='Error', message='Failed To Search In Users', icon='cancel')

    def update_users_wait_list_table(self):
        from api_services.user import get_users_wait_list

        self.wait_list_users = get_users_wait_list()

        if self.wait_list_users['ok']:
            self.wait_list_users = self.wait_list_users['waitListUsers']

        values = [
            ['ID', 'Email', 'Username', 'Full Name', 'Role', 'Approve', 'Reject'],
            *[
                [
                    '...' + user['_id'][-6:],
                    user['email'],
                    user['username'],
                    user['fullName'],
                    user['role'],
                    'Approve',
                    'Reject'
                ] for user in self.wait_list_users
            ]
        ]

        if self.users_wait_list_table:
            self.users_wait_list_table.destroy()
        if self.users_wait_list_not_found_label:
            self.users_wait_list_not_found_label.destroy()

        if len(values) > 1:
            self.users_wait_list_table = CTkTable(master=self.users_waiting_list_frame, column=7,
                                                  values=values,
                                                  command=self.handle_approving_user, hover=True, column_hover=[5, 6],
                                                  not_hover_rows=[0],
                                                  column_hover_text_color=['#F57C00', '#F57C00'],
                                                  column_hover_bg_color=['#1B5E20', '#B71C1C'])
            self.users_wait_list_table.pack(expand=True, fill='both', pady=(10, 0))
        else:
            self.users_wait_list_not_found_label = ctk.CTkLabel(self.users_waiting_list_frame,
                                                                text='No User In Wait List...',
                                                                font=('Arial', 16, 'italic'),
                                                                text_color='gray')
            self.users_wait_list_not_found_label.pack()

    def update_all_users_table(self, search_result=None):
        from api_services.user import get_all_users

        self.all_users = search_result if search_result else get_all_users()

        if not search_result and self.all_users['ok']:
            self.all_users = self.all_users['users']

        values = [
            ['ID', 'Email', 'Username', 'Full Name', 'Role', 'Edit', 'Delete', 'Ban'],
            *[
                [
                    '...' + user['_id'][-6:],
                    user['email'],
                    user['username'],
                    user['fullName'],
                    user['role'],
                    'Edit',
                    'Delete',
                    'Ban' if not user['isBanned'] else 'UnBan'
                ] for user in self.all_users
            ]
        ]

        if self.all_users_table:
            self.all_users_table.destroy()
        if self.all_users_not_found_label:
            self.all_users_not_found_label.destroy()

        if len(values) > 1:
            self.all_users_table = CTkTable(master=self.all_users_table_frame,
                                            values=values,
                                            command=self.handle_all_users_funcs, hover=True, column_hover=[5, 6, 7],
                                            not_hover_rows=[0],
                                            column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                            column_hover_bg_color=['#1B5E20', '#B71C1C', '#B71C1C'])
            self.all_users_table.pack(expand=True, fill='both', pady=(10, 0))
        else:
            self.all_users_not_found_label = ctk.CTkLabel(self.all_users_table_frame,
                                                          text='No Users Yet...',
                                                          font=('Arial', 16, 'italic'),
                                                          text_color='gray')
            self.all_users_not_found_label.pack()

    def handle_approving_user(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 5:
                from api_services.user import approve_user
                approve_result = approve_user(self.wait_list_users[row - 1]['_id'])
                if approve_result['ok']:
                    CTkMessagebox(title='Success', message='User Was Approved Successfully!', icon='check')
                    self.update_users_wait_list_table()
                    self.update_all_users_table()
                else:
                    CTkMessagebox(title='Error', message='Failed To Approve User!', icon='cancel')
            if column == 6:
                from api_services.user import reject_user
                reject_result = reject_user(self.wait_list_users[row - 1]['_id'])
                if reject_result['ok']:
                    CTkMessagebox(title='Success', message='User Was Rejected Successfully!', icon='check')
                    self.update_users_wait_list_table()
                else:
                    CTkMessagebox(title='Error', message='Failed To Reject User!', icon='cancel')

    def handle_all_users_funcs(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 5:
                # handle editing user
                pass
            if column == 6:
                from api_services.user import delete_user
                delete_result = delete_user(self.all_users[row - 1]['_id'])
                if delete_result['ok']:
                    CTkMessagebox(title='Success', message='User Was Deleted Successfully!', icon='check')
                    self.update_all_users_table()
                else:
                    CTkMessagebox(title='Error', message='Failed To Delete User!', icon='cancel')
            if column == 7:
                if self.all_users[row - 1]['isBanned']:
                    from api_services.user import unban_user
                    unban_result = unban_user(self.all_users[row - 1]['_id'])
                    if unban_result['ok']:
                        CTkMessagebox(title='Success', message='User Was Unbanned Successfully!', icon='check')
                        self.update_all_users_table()
                    else:
                        CTkMessagebox(title='Error', message='Failed To Unban User!', icon='cancel')
                else:
                    from api_services.user import ban_user
                    ban_result = ban_user(self.all_users[row - 1]['_id'])
                    if ban_result['ok']:
                        CTkMessagebox(title='Success', message='User Was Banned Successfully!', icon='check')
                        self.update_all_users_table()
                    else:
                        CTkMessagebox(title='Error', message='Failed To Ban User!', icon='cancel')

    def load_movies_tab(self, parent):
        from modules.plainInput import PlainInput
        from api_services.movies import get_all_movies

        self.all_movies = get_all_movies()
        if self.all_movies['ok']:
            self.all_movies = self.all_movies['allMovies']

        # disable target tab button and enable other tabs button
        self.movies_button.configure(state='disabled')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.users_button.configure(state='normal')
        self.articles_button.configure(state='normal')
        self.comments_button.configure(state='normal')
        self.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        add_new_movie_frame = ctk.CTkFrame(parent, fg_color='transparent')
        add_new_movie_frame.grid_columnconfigure((0, 1, 2), weight=1)
        add_new_movie_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)

        SectionTitle(add_new_movie_frame, text='Add New Movie').grid(row=0, column=0, sticky='w', padx=30, pady=(0, 20))

        self.movie_name_entry = PlainInput(add_new_movie_frame, label_text='Movie Full Name:',
                                           input_placeholder="Enter Movie Name...")
        self.movie_name_entry.grid(row=1, column=0)

        self.movie_genre_entry = PlainInput(add_new_movie_frame, label_text='Movie Genres(separated by space):',
                                            input_placeholder="Enter Movie Genres...")
        self.movie_genre_entry.grid(row=1, column=1)

        self.movie_release_date_entry = PlainInput(add_new_movie_frame, label_text='Release Date:',
                                                   input_placeholder="Enter Movie Release Date...")
        self.movie_release_date_entry.grid(row=1, column=2)

        self.movie_language_entry = PlainInput(add_new_movie_frame, label_text='Movie Language:',
                                               input_placeholder="Enter Movie Languages...")
        self.movie_language_entry.grid(row=2, column=0, pady=20)

        self.movie_countries_entry = PlainInput(add_new_movie_frame, label_text='Movie Country:',
                                                input_placeholder='Enter Movie Countries...')
        self.movie_countries_entry.grid(row=2, column=1)

        self.movie_budget_entry = PlainInput(add_new_movie_frame, label_text='Movie Budget:',
                                             input_placeholder='Enter Movie Budget...')
        self.movie_budget_entry.grid(row=2, column=2)

        movie_summary_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_summary_frame.grid_columnconfigure(0, weight=1)
        movie_summary_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45)
        ctk.CTkLabel(movie_summary_frame, text='Movie Summary:', text_color='gray', font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        self.movie_summary_entry = ctk.CTkTextbox(movie_summary_frame)
        self.movie_summary_entry.grid(row=1, column=0, sticky='ew')

        self.movie_cover = None
        movie_cover_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_cover_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(movie_cover_frame, text='Movie Cover:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(movie_cover_frame, text='Add Cover', command=self.select_file).grid(row=1, column=0,
                                                                                          sticky='w')
        self.movie_selected_cover_label = ctk.CTkLabel(movie_cover_frame,
                                                       text=self.movie_cover and 'Movie Cover Has Been Selected!' or 'Please Select Movie Cover')
        self.movie_selected_cover_label.grid(row=0, column=1, padx=20)

        self.movie_medias = []
        movie_medias_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_medias_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(movie_medias_frame, text='Movie Medias:', text_color='gray', font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(movie_medias_frame, text='Add Media', command=self.select_file).grid(row=1, column=0, sticky='w')
        self.selected_movie_medias_count_label = ctk.CTkLabel(movie_medias_frame,
                                                              text=f'{len(self.movie_medias)} Medias Have Been Selected!')
        self.selected_movie_medias_count_label.grid(row=0, column=1, padx=20)

        self.movie_casts = []
        self.movie_casts_temp = []
        self.movie_casts_table = None
        self.movie_casts_not_found_label = None
        movie_cast_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_cast_frame.grid_columnconfigure((0, 1, 2), weight=1)
        movie_cast_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=45)
        ctk.CTkLabel(movie_cast_frame, text='Movie Cast:', text_color='gray', font=('Arial', 14, 'italic')).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky='w')
        self.search_cast_name_entry = PlainInput(movie_cast_frame, label_text='Name - In-Movie-Name - In-Movie-Role:',
                                                 input_placeholder='Enter Cast Name...')
        self.search_cast_name_entry.grid(row=1, column=0, sticky='nw')
        ctk.CTkButton(movie_cast_frame, text='Search', command=self.search_cast_handler).grid(row=1, column=0,
                                                                                              sticky='w')

        ctk.CTkLabel(movie_cast_frame, text='Search Results:', text_color='gray', font=('Arial', 10, 'italic')).grid(
            row=0, column=1)
        cast_result_frame = ctk.CTkFrame(movie_cast_frame, width=200, height=200)
        cast_result_frame.grid(row=1, column=1, sticky='nsew')
        cast_result_frame.grid_columnconfigure(0, weight=1)
        self.cast_result_box = ctk.CTkFrame(cast_result_frame, fg_color='transparent',
                                            width=cast_result_frame.cget('width'),
                                            height=cast_result_frame.cget('height'))
        self.cast_result_box.grid_columnconfigure(0, weight=1)
        self.cast_result_box.grid_rowconfigure(0, weight=1)
        self.cast_result_box.grid(row=0, column=0, sticky='nsew')
        ctk.CTkLabel(movie_cast_frame, text='Selected Cast:', text_color='gray', font=('Arial', 10, 'italic')).grid(
            row=0, column=2)
        self.cast_selected_box = ctk.CTkFrame(movie_cast_frame, width=200, height=200)
        self.cast_selected_box.grid_columnconfigure(0, weight=1)
        self.cast_selected_box.grid(row=1, column=2, sticky='nsew', padx=100)

        submit_form_buttons_frame = ctk.CTkFrame(movie_cast_frame, fg_color='transparent')
        submit_form_buttons_frame.grid(row=2, column=0, columnspan=3, pady=40)
        ctk.CTkButton(submit_form_buttons_frame, text='Create',
                      command=lambda: self.handle_creating_movie(isPublished=True)).grid(row=0, column=0)
        ctk.CTkButton(submit_form_buttons_frame, text='Save As Draft', fg_color='#EF5350', hover_color='#C62828',
                      command=lambda: self.handle_creating_movie(isPublished=False)).grid(
            row=0, column=1, padx=30)

        all_movies_values = [
            ['ID', 'Name', 'Rate', 'Details', 'Status', 'Edit', 'Delete'],
            *[
                [
                    '...' + movie['_id'][-6:],
                    movie['fullName'],
                    movie['rate'],
                    'Details',
                    'Published' if movie['isPublished'] else 'Not Published',
                    'Edit',
                    'Delete'
                ] for movie in self.all_movies
            ]
        ]

        self.all_movies_table_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.all_movies_table_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        temp_frame = ctk.CTkFrame(self.all_movies_table_frame, fg_color='transparent')
        temp_frame.pack(expand=True, fill='x')
        SectionTitle(temp_frame, text='All Movies').pack(padx=30, side=tkinter.LEFT)
        search_box_frame = ctk.CTkFrame(temp_frame, fg_color='transparent')
        search_box_frame.pack(padx=30, side=tkinter.RIGHT)
        search_box_entry = ctk.CTkEntry(search_box_frame, placeholder_text='Search here...', width=200)
        search_box_entry.grid(row=0, column=0, padx=10)
        ctk.CTkButton(search_box_frame, text='Go!', width=60).grid(row=0, column=1)
        self.all_movies_table = None
        self.movies_not_found_label = None
        if len(all_movies_values) > 1:
            self.all_movies_table = CTkTable(self.all_movies_table_frame, values=all_movies_values, hover=True,
                                             column_hover=[3, 4, 5, 6],
                                             command=self.handle_movies_funcs,
                                             column_hover_text_color=['#F57C00', '#F57C00', '#F57C00', '#F57C00'],
                                             column_hover_bg_color=['#1B5E20', '#1B5E20', '#1B5E20', '#B71C1C'],
                                             not_hover_rows=[0])
            self.all_movies_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.movies_not_found_label = ctk.CTkLabel(self.all_movies_table_frame,
                                                       text='No Movies Yet...',
                                                       font=('Arial', 16, 'italic'),
                                                       text_color='gray')
            self.movies_not_found_label.pack()

    def search_cast_handler(self):
        from api_services.cast import search_cast
        self.cast_search_result = search_cast(self.search_cast_name_entry.input.get().split(' - ')[0])
        if self.cast_search_result['ok']:
            self.update_searched_casts_table(self.cast_search_result['result'])
        else:
            CTkMessagebox(title='Error', message=self.cast_search_result['message'], icon='cancel')

    def update_searched_casts_table(self, search_result):
        values = [
            ["Name", "Select"],
            *[
                [
                    cast['fullName'],
                    'Select'
                ] for cast in search_result
            ]
        ]

        if self.movie_casts_table:
            self.movie_casts_table.destroy()
        if self.movie_casts_not_found_label:
            self.movie_casts_not_found_label.destroy()

        if len(values) > 1:
            self.movie_casts_table = CTkTable(self.cast_result_box, values=values, hover=True,
                                              column_hover=[1],
                                              command=self.handle_adding_cast,
                                              column_hover_text_color=['#F57C00'],
                                              column_hover_bg_color=['#1B5E20'],
                                              not_hover_rows=[0])
            self.movie_casts_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.movie_casts_not_found_label = ctk.CTkLabel(self.cast_result_box,
                                                            text='No Cast Found...',
                                                            font=('Arial', 16, 'italic'),
                                                            text_color='gray',
                                                            width=self.cast_result_box.cget('width'),
                                                            height=self.cast_result_box.cget('height'))
            self.movie_casts_not_found_label.grid(row=0, column=0)

    def handle_adding_cast(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 1:
                self.movie_casts.append({"castId": self.cast_search_result['result'][row - 1]['_id'],
                                         "inMovieName": self.search_cast_name_entry.input.get().split(' - ')[1],
                                         "inMovieRole": self.search_cast_name_entry.input.get().split(' - ')[2]})
                self.movie_casts_temp.append([self.cast_search_result['result'][row - 1]['fullName'],
                                              self.search_cast_name_entry.input.get().split(' - ')[1]])
                self.update_movie_selected_cast_box()

    def update_movie_selected_cast_box(self):
        for widget in self.cast_selected_box.winfo_children():
            widget.destroy()

        for index, cast in enumerate(self.movie_casts_temp):
            ctk.CTkLabel(self.cast_selected_box, text=f"{cast[0]} - {cast[1]}").grid(row=index, column=0)

    def handle_creating_movie(self, isPublished):
        from api_services.movies import create_movie
        create_result = create_movie(
            fullName=self.movie_name_entry.input.get(),
            summary=self.movie_summary_entry.get("1.0"),
            genre=self.movie_genre_entry.input.get(),
            releaseDate=self.movie_release_date_entry.input.get(),
            countries=self.movie_countries_entry.input.get(),
            language=self.movie_language_entry.input.get(),
            budget=self.movie_budget_entry.input.get(),
            cover=self.movie_cover,
            medias=self.movie_medias,
            cast=self.movie_casts,
            isPublished=isPublished
        )

        if create_result['ok']:
            CTkMessagebox(title='Success', message='Movie Created Successfully!', icon='check')
            self.update_all_movies_table()
        else:
            CTkMessagebox(title='Error', message=create_result['message'], icon='cancel')

    def update_all_movies_table(self, search_result=None):
        from api_services.movies import get_all_movies

        self.all_movies = search_result if search_result else get_all_movies()

        if not search_result and self.all_movies['ok']:
            self.all_movies = self.all_movies['allMovies']

        values = [
            ['ID', 'Name', 'Rate', 'Details', 'Status', 'Edit', 'Delete'],
            *[
                [
                    '...' + movie['_id'][-6:],
                    movie['fullName'],
                    movie['rate'],
                    'Details',
                    'Published' if movie['isPublished'] else 'Not Published',
                    'Edit',
                    'Delete'
                ] for movie in self.all_movies
            ]
        ]

        if self.all_movies_table:
            self.all_movies_table.destroy()
        if self.movies_not_found_label:
            self.movies_not_found_label.destroy()

        if len(values) > 1:
            self.all_movies_table = CTkTable(master=self.all_movies_table_frame,
                                             values=values,
                                             command=self.handle_movies_funcs, hover=True,
                                             column_hover=[3, 4, 5, 6],
                                             not_hover_rows=[0],
                                             column_hover_text_color=['#F57C00', '#F57C00', '#F57C00', '#F57C00'],
                                             column_hover_bg_color=['#1B5E20', '#1B5E20', '#B1B5E20', '#B71C1C'])
            self.all_movies_table.pack(expand=True, fill='both', pady=(10, 0))
        else:
            self.movies_not_found_label = ctk.CTkLabel(self.all_movies_table_frame,
                                                       text='No Movies Yet...',
                                                       font=('Arial', 16, 'italic'),
                                                       text_color='gray')
            self.movies_not_found_label.pack()

    def handle_movies_funcs(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 3:
                # handle showing details
                pass
            elif column == 4:
                from api_services.movies import change_movie_status_by_id
                change_result = change_movie_status_by_id(self.all_movies[row - 1]['_id'])
                if change_result['ok']:
                    CTkMessagebox(title='Success', message='Movie Status Changed Successfully!', icon='check')
                    self.update_all_movies_table()
                else:
                    CTkMessagebox(title='Error', message='Failed To Change Movie Status!', icon='cancel')
            elif column == 5:
                # handle edit movie
                pass
            elif column == 6:
                from api_services.movies import delete_movie_by_id
                delete_result = delete_movie_by_id(self.all_movies[row - 1]['_id'])
                if delete_result['ok']:
                    CTkMessagebox(title='Success', message='Movie Deleted Successfully!', icon='check')
                    self.update_all_movies_table()
                else:
                    CTkMessagebox(title='Error', message='Failed To Delete Movie!', icon='cancel')

    def load_casts_tab(self, parent):
        from modules.plainInput import PlainInput
        from api_services.cast import get_all_casts

        self.all_casts = get_all_casts()
        if self.all_casts['ok']:
            self.all_casts = self.all_casts['allCast']

        # disable target tab button and enable other tabs button
        self.casts_button.configure(state='disabled')
        self.articles_button.configure(state='normal')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.users_button.configure(state='normal')
        self.movies_button.configure(state='normal')
        self.comments_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        add_new_cast_frame = ctk.CTkFrame(parent, fg_color='transparent')
        add_new_cast_frame.grid_columnconfigure((0, 1, 2), weight=1)
        add_new_cast_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)

        SectionTitle(add_new_cast_frame, text='Add New Cast').grid(row=0, column=0, sticky='w', padx=30,
                                                                   pady=(0, 20))

        self.cast_name_entry = PlainInput(add_new_cast_frame, label_text='Name:',
                                          input_placeholder="Enter Cast Name...")
        self.cast_name_entry.grid(row=1, column=0, sticky='w', padx=45)

        cast_bio_frame = ctk.CTkFrame(add_new_cast_frame, fg_color='transparent')
        cast_bio_frame.grid_columnconfigure(0, weight=1)
        cast_bio_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=45, pady=10)
        ctk.CTkLabel(cast_bio_frame, text='Biography:', text_color='gray', font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        self.cast_bio_input = ctk.CTkTextbox(cast_bio_frame)
        self.cast_bio_input.grid(row=1, column=0, sticky='ew')

        self.cast_birth_date_entry = PlainInput(add_new_cast_frame, label_text='Birth Date:',
                                                input_placeholder="Enter Cast Birth Date...")
        self.cast_birth_date_entry.grid(row=3, column=0, sticky='w', padx=45)

        self.cast_birth_place_entry = PlainInput(add_new_cast_frame, label_text='Birth Place:',
                                                 input_placeholder="Enter Birth Place...")
        self.cast_birth_place_entry.grid(row=4, column=0, sticky='w', padx=45)

        self.cast_height_entry = PlainInput(add_new_cast_frame, label_text='Name:',
                                            input_placeholder="Enter Cast Height...")
        self.cast_height_entry.grid(row=5, column=0, sticky='w', padx=45)

        self.cast_profile_pic = None
        self.cast_page_photos = None

        cast_profile_pic_frame = ctk.CTkFrame(add_new_cast_frame, fg_color='transparent')
        cast_profile_pic_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(cast_profile_pic_frame, text='Cast Profile:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(cast_profile_pic_frame, text='Add Profile', command=self.select_file).grid(row=1, column=0,
                                                                                                 sticky='w')
        selected_profile_pic_label = ctk.CTkLabel(cast_profile_pic_frame,
                                                  text=self.cast_profile_pic and 'Cast Profile Has Been Selected!' or 'Please Select Cast Profile')
        selected_profile_pic_label.grid(row=0, column=1, padx=20)

        cast_page_photos_frame = ctk.CTkFrame(add_new_cast_frame, fg_color='transparent')
        cast_page_photos_frame.grid(row=7, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(cast_page_photos_frame, text='Cast Page Photos:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(cast_page_photos_frame, text='Add Photos', command=self.select_cast_page_pics).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky='w')
        selected_page_pics_label = ctk.CTkLabel(cast_page_photos_frame,
                                                text=self.cast_profile_pic and 'Cast Page Photos Have Been Selected!' or 'Please Select Cast Page Photos')
        selected_page_pics_label.grid(row=0, column=1, padx=20)

        ctk.CTkButton(add_new_cast_frame, text='Create', command=self.handle_creating_cast).grid(row=8, column=0,
                                                                                                 columnspan=3)

        all_casts_list = [
            ['ID', 'FullName', 'Bio', 'BirthDate', 'BirthPlace', 'Details', 'Edit', 'Delete'],
            *[
                [
                    '...' + cast['_id'][-6:],
                    cast['fullName'],
                    cast['biography'][:15] + '...',
                    cast['birthDate'],
                    cast['birthPlace'],
                    'Details',
                    'Edit',
                    'Delete'
                ] for cast in self.all_casts
            ]
        ]

        self.all_casts_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.all_casts_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        temp_frame = ctk.CTkFrame(self.all_casts_frame, fg_color='transparent')
        temp_frame.pack(expand=True, fill='x')
        SectionTitle(temp_frame, text='All Casts').pack(padx=30, side=tkinter.LEFT)
        self.all_casts_table = None
        self.cast_not_found_label = None
        if len(all_casts_list) > 1:
            self.all_casts_table = CTkTable(self.all_casts_frame, values=all_casts_list, hover=True,
                                            column_hover=[5, 6, 7],
                                            command=self.handle_casts_funcs,
                                            column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                            column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'],
                                            not_hover_rows=[0])
            self.all_casts_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.cast_not_found_label = ctk.CTkLabel(self.all_casts_frame,
                                                     text='No Cast Yet...',
                                                     font=('Arial', 16, 'italic'),
                                                     text_color='gray')
            self.cast_not_found_label.pack()

    def update_all_casts_table(self):
        from api_services.cast import get_all_casts

        self.all_casts = get_all_casts()
        if self.all_casts['ok']:
            self.all_casts = self.all_casts['allCast']

        all_casts_list = [
            ['ID', 'FullName', 'Bio', 'BirthDate', 'BirthPlace', 'Details', 'Edit', 'Delete'],
            *[
                [
                    '...' + cast[-6:],
                    cast['fullName'],
                    cast['biography'],
                    cast['birthDate'],
                    cast['birthPlace'],
                    'Details',
                    'Edit',
                    'Delete'
                ] for cast in self.all_casts
            ]
        ]

        if self.all_casts_table:
            self.all_casts_table.destroy()
        if self.cast_not_found_label:
            self.cast_not_found_label.destroy()

        if len(all_casts_list) > 1:
            self.all_casts_table = CTkTable(self.all_casts_frame, values=all_casts_list, hover=True,
                                            column_hover=[5, 6, 7],
                                            column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                            column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'],
                                            not_hover_rows=[0])
            self.all_casts_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.cast_not_found_label = ctk.CTkLabel(self.all_casts_frame,
                                                     text='No Cast Yet...',
                                                     font=('Arial', 16, 'italic'),
                                                     text_color='gray')
            self.cast_not_found_label.pack()

    def handle_casts_funcs(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 5:
                # go to details page
                pass
            elif column == 6:
                # handle edit cast
                pass
            elif column == 7:
                from api_services.cast import delete_cast
                delete_result = delete_cast(self.all_casts[row - 1]['_id'])
                if delete_result['ok']:
                    CTkMessagebox(title='Success', message='Cast Deleted Successfully!', icon='check')
                    self.update_all_casts_table()
                else:
                    CTkMessagebox(title='Error', message='Failed To Delete Cast!', icon='cancel')

    def select_cast_page_pics(self):
        self.cast_page_photos = filedialog.askopenfilenames()

    def select_cast_profile_pic(self):
        self.cast_profile_pic = filedialog.askopenfilename()

    def handle_creating_cast(self):
        from api_services.cast import create_cast
        create_result = create_cast(
            fullName=self.cast_name_entry.input.get(),
            biography=self.cast_bio_input.get("1.0"),
            birthDate=self.cast_birth_date_entry.input.get(),
            birthPlace=self.cast_birth_place_entry.input.get(),
            height=self.cast_height_entry.input.get(),
            profilePic=self.cast_profile_pic,
            photos=self.cast_page_photos
        )
        if create_result['ok']:
            CTkMessagebox(title='Success', message='Cast Created Successfully!', icon='check')
            self.update_users_wait_list_table()
        else:
            CTkMessagebox(title='Error', message=create_result['message'], icon='cancel')

    def select_file(self):
        file_name = filedialog.askopenfilename()
        print(file_name)
        return file_name

    def load_articles_tab(self, parent):
        from modules.plainInput import PlainInput
        from api_services.articles import get_all_articles

        self.all_articles = get_all_articles()
        if self.all_articles['ok']:
            self.all_articles = self.all_articles['allArticles']

        # disable target tab button and enable other tabs button
        self.articles_button.configure(state='disabled')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.users_button.configure(state='normal')
        self.movies_button.configure(state='normal')
        self.comments_button.configure(state='normal')
        self.casts_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        all_articles_list = [
            ['ID', 'Title', 'Rate', 'Status', 'Details', 'Delete'],
            *[
                [
                    '...' + article['_id'][-6:],
                    article['title'],
                    article['rate'],
                    'Published' if article['isPublished'] else 'Not Published',
                    'Details',
                    'Delete'
                ] for article in self.all_articles
            ]
        ]

        self.all_articles_table = None
        self.article_not_found_label = None
        self.all_articles_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.all_articles_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)
        temp_frame = ctk.CTkFrame(self.all_articles_frame, fg_color='transparent')
        temp_frame.pack(expand=True, fill='x')
        SectionTitle(temp_frame, text='All Articles').pack(padx=30, side=tkinter.LEFT)
        search_box_frame = ctk.CTkFrame(temp_frame, fg_color='transparent')
        search_box_frame.pack(padx=30, side=tkinter.RIGHT)
        self.search_in_articles_entry = ctk.CTkEntry(search_box_frame, placeholder_text='Search here...', width=200)
        self.search_in_articles_entry.grid(row=0, column=0, padx=10)
        ctk.CTkButton(search_box_frame, text='Go!', width=60, command=self.handle_searching_in_articles).grid(row=0,
                                                                                                              column=1)
        if len(all_articles_list) > 1:
            self.all_articles_table = CTkTable(self.all_articles_frame, values=all_articles_list, hover=True,
                                               column_hover=[4, 5],
                                               command=self.handle_articles_funcs,
                                               column_hover_text_color=['#F57C00', '#F57C00'],
                                               column_hover_bg_color=['#1B5E20', '#B71C1C'],
                                               not_hover_rows=[0])
            self.all_articles_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.article_not_found_label = ctk.CTkLabel(self.all_articles_frame,
                                                        text='No Articles Yet...',
                                                        font=('Arial', 16, 'italic'),
                                                        text_color='gray')
            self.article_not_found_label.pack()

    def handle_searching_in_articles(self):
        from api_services.articles import search_in_articles
        search_result = search_in_articles(q=self.search_in_articles_entry.get())
        self.update_all_articles_table(search_result=search_result['result'])

    def handle_articles_funcs(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 4:
                # handle showing details
                pass
            if column == 5:
                from api_services.articles import delete_article
                delete_result = delete_article(self.all_articles[row - 1]['_id'])
                if delete_result['ok']:
                    CTkMessagebox(title='Success', message='Article Deleted Successfully!', icon='check')
                    self.update_all_articles_table()
                else:
                    CTkMessagebox(title='Error', message=delete_result['message'], icon='cancel')

    def update_all_articles_table(self, search_result=None):
        from api_services.articles import get_all_articles

        self.all_articles = search_result if search_result else get_all_articles()
        if not search_result and self.all_articles['ok']:
            self.all_articles = self.all_articles['allArticles']

        all_articles_list = [
            ['ID', 'Title', 'Rate', 'Status', 'Details', 'Delete'],
            *[
                [
                    '...' + article['_id'][-6:],
                    article['title'],
                    article['rate'],
                    'Published' if article['isPublished'] else 'Not Published',
                    'Details',
                    'Delete'
                ] for article in self.all_articles
            ]
        ]

        if self.all_articles_table:
            self.all_articles_table.destroy()
        if self.article_not_found_label:
            self.article_not_found_label.destroy()

        if len(all_articles_list) > 1:
            self.all_articles_table = CTkTable(self.all_articles_frame, values=all_articles_list, hover=True,
                                               column_hover=[4, 5],
                                               command=self.handle_articles_funcs,
                                               column_hover_text_color=['#F57C00', '#F57C00'],
                                               column_hover_bg_color=['#1B5E20', '#B71C1C'],
                                               not_hover_rows=[0])
            self.all_articles_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.article_not_found_label = ctk.CTkLabel(self.all_casts_frame,
                                                        text='No Articles Yet...',
                                                        font=('Arial', 16, 'italic'),
                                                        text_color='gray')
            self.article_not_found_label.pack()

    def load_comments_tab(self, parent):
        from api_services.comment import get_wait_list_comments
        # disable target tab button and enable other tabs button
        self.comments_button.configure(state='disabled')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.users_button.configure(state='normal')
        self.articles_button.configure(state='normal')
        self.movies_button.configure(state='normal')
        self.casts_button.configure(state='normal')

        self.all_comments = get_wait_list_comments()
        if self.all_comments['ok']:
            self.all_comments = self.all_comments['waitListComments']

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        all_waiting_comments = [
            ['ID', 'User', 'Page', 'Rate', 'Body', 'Approve', 'Delete'],
            *[
                [
                    '...' + comment['_id'][-6:],
                    comment['user']['username'],
                    comment['page'].get('title', comment['page'].get('fullName')),
                    comment['rate'],
                    'See',
                    'Approve',
                    'Delete'
                ] for comment in self.all_comments
            ]
        ]

        self.all_waiting_comments_frame = ctk.CTkFrame(parent, fg_color='transparent')
        self.all_waiting_comments_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        SectionTitle(self.all_waiting_comments_frame, text='Comments Waiting List').pack(padx=30, anchor='w')
        self.all_comments_table = None
        self.comment_not_found_label = None
        if len(all_waiting_comments) > 1:
            self.all_comments_table = CTkTable(self.all_waiting_comments_frame, values=all_waiting_comments, hover=True,
                                               column_hover=[4, 5, 6],
                                               command=self.handle_comments_funcs,
                                               column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                               column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'],
                                               not_hover_rows=[0])
            self.all_comments_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.comment_not_found_label = ctk.CTkLabel(self.all_waiting_comments_frame,
                                                        text='No Comments In Waiting List...',
                                                        font=('Arial', 16, 'italic'),
                                                        text_color='gray')
            self.comment_not_found_label.pack()

    def handle_comments_funcs(self, *args):
        row = args[0]['row']
        column = args[0]['column']
        if row > 0:
            if column == 4:
                # show comment body
                pass
            if column == 5:
                from api_services.comment import approve_comment
                approve_result = approve_comment(self.all_comments[row - 1]['_id'])
                if approve_result['ok']:
                    CTkMessagebox(title='Success', message='Comment Approved Successfully!', icon='check')
                    self.update_wait_list_comments_table()
                else:
                    CTkMessagebox(title='Error', message=approve_result['message'], icon='cancel')
            if column == 6:
                from api_services.comment import delete_comment
                reject_result = delete_comment(self.all_comments[row-1]['_id'])
                if reject_result['ok']:
                    CTkMessagebox(title='Success', message='Comment Rejected And Deleted Successfully!', icon='check')
                    self.update_wait_list_comments_table()
                else:
                    CTkMessagebox(title='Error', message=reject_result['message'], icon='cancel')

    def update_wait_list_comments_table(self):
        from api_services.comment import get_wait_list_comments

        self.all_comments = get_wait_list_comments()
        if self.all_comments['ok']:
            self.all_comments = self.all_comments['waitListComments']

        all_waiting_comments = [
            ['ID', 'User', 'Page', 'Rate', 'Body', 'Approve', 'Delete'],
            *[
                [
                    '...' + comment['_id'][-6:],
                    comment['user']['username'],
                    comment['page'].get('fullName', 'title'),
                    comment['rate'],
                    'See',
                    'Approve',
                    'Delete'
                ] for comment in self.all_comments
            ]
        ]

        if self.all_comments_table:
            self.all_comments_table.destroy()
        if self.comment_not_found_label:
            self.comment_not_found_label.destroy()

        if len(all_waiting_comments) > 1:
            self.all_comments_table = CTkTable(self.all_waiting_comments_frame, values=all_waiting_comments, hover=True,
                                               column_hover=[4, 5, 6],
                                               column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                               column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'],
                                               not_hover_rows=[0])
            self.all_comments_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
        else:
            self.comment_not_found_label = ctk.CTkLabel(self.all_waiting_comments_frame,
                                                        text='No Comments In Waiting List...',
                                                        font=('Arial', 16, 'italic'),
                                                        text_color='gray')
            self.comment_not_found_label.pack()