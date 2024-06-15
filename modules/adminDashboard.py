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

        self.articles_button = ctk.CTkButton(navbar_frame, text="Articles",
                                             command=lambda: self.load_articles_tab(dynamic_content_frame))
        self.articles_button.grid(row=0, column=6, padx=20, pady=20)

        self.comments_button = ctk.CTkButton(navbar_frame, text="Comments",
                                             command=lambda: self.load_comments_tab(dynamic_content_frame))
        self.comments_button.grid(row=0, column=7, padx=20, pady=20)

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

        add_new_user_submit_btn = ctk.CTkButton(add_new_user_frame, text='Submit', height=30, command=self.handle_creating_user)
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
        ctk.CTkButton(search_box_frame, text='Go!', width=60, command=self.handle_searching_in_users).grid(row=0, column=1)
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

        # disable target tab button and enable other tabs button
        self.movies_button.configure(state='disabled')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.users_button.configure(state='normal')
        self.articles_button.configure(state='normal')
        self.comments_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        add_new_movie_frame = ctk.CTkFrame(parent, fg_color='transparent')
        add_new_movie_frame.grid_columnconfigure((0, 1, 2), weight=1)
        add_new_movie_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)

        SectionTitle(add_new_movie_frame, text='Add New Movie').grid(row=0, column=0, sticky='w', padx=30, pady=(0, 20))

        full_name_input = PlainInput(add_new_movie_frame, label_text='Movie Full Name:',
                                     input_placeholder="Enter Movie Name...")
        full_name_input.grid(row=1, column=0)

        genre_input = PlainInput(add_new_movie_frame, label_text='Movie Genre:',
                                 input_placeholder="Enter Movie Genres...")
        genre_input.grid(row=1, column=1)

        release_date_input = PlainInput(add_new_movie_frame, label_text='Release Date:',
                                        input_placeholder="Enter Movie Release Date...")
        release_date_input.grid(row=1, column=2)

        language_input = PlainInput(add_new_movie_frame, label_text='Movie Language:',
                                    input_placeholder="Enter Movie Languages...")
        language_input.grid(row=2, column=0, pady=20)

        countries_input = PlainInput(add_new_movie_frame, label_text='Movie Country:',
                                     input_placeholder='Enter Movie Countries...')
        countries_input.grid(row=2, column=1)

        budget_input = PlainInput(add_new_movie_frame, label_text='Movie Budget:',
                                  input_placeholder='Enter Movie Budget...')
        budget_input.grid(row=2, column=2)

        movie_summary_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_summary_frame.grid_columnconfigure(0, weight=1)
        movie_summary_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45)
        ctk.CTkLabel(movie_summary_frame, text='Movie Summary:', text_color='gray', font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        movie_summary_input = ctk.CTkTextbox(movie_summary_frame)
        movie_summary_input.grid(row=1, column=0, sticky='ew')

        movie_medias = []
        movie_medias_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_medias_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(movie_medias_frame, text='Movie Medias:', text_color='gray', font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(movie_medias_frame, text='Add Media', command=self.select_file).grid(row=1, column=0, sticky='w')
        selected_medias_count_label = ctk.CTkLabel(movie_medias_frame,
                                                   text=f'{len(movie_medias)} Medias Have Been Selected!')
        selected_medias_count_label.grid(row=0, column=1, padx=20)

        movie_cast_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_cast_frame.grid_columnconfigure((0, 1, 2), weight=1)
        movie_cast_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=45)
        ctk.CTkLabel(movie_cast_frame, text='Movie Cast:', text_color='gray', font=('Arial', 14, 'italic')).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky='w')
        cast_name_input = PlainInput(movie_cast_frame, label_text='Name:', input_placeholder='Enter Cast Name...')
        cast_name_input.grid(row=1, column=0, sticky='nw')
        ctk.CTkButton(movie_cast_frame, text='Search').grid(row=1, column=0, sticky='w')
        ctk.CTkLabel(movie_cast_frame, text='Search Results:', text_color='gray', font=('Arial', 10, 'italic')).grid(
            row=0, column=1)
        cast_result_box = ctk.CTkFrame(movie_cast_frame, width=200)
        cast_result_box.grid_columnconfigure(0, weight=1)
        cast_result_box.grid(row=1, column=1, sticky='ew')
        ctk.CTkLabel(movie_cast_frame, text='Selected Cast:', text_color='gray', font=('Arial', 10, 'italic')).grid(
            row=0, column=2)
        cast_selected_box = ctk.CTkFrame(movie_cast_frame, width=200)
        cast_selected_box.grid_columnconfigure(0, weight=1)
        cast_selected_box.grid(row=1, column=2, sticky='ew', padx=100)

        submit_form_buttons_frame = ctk.CTkFrame(movie_cast_frame, fg_color='transparent')
        submit_form_buttons_frame.grid(row=2, column=0, columnspan=3, pady=40)
        ctk.CTkButton(submit_form_buttons_frame, text='Create').grid(row=0, column=0)
        ctk.CTkButton(submit_form_buttons_frame, text='Save As Draft', fg_color='#EF5350', hover_color='#C62828').grid(
            row=0, column=1, padx=30)

        all_movies_list = [
            ['Name', 'Rate', 'Status', 'Details', 'Edit', 'Delete'],
            ['After Jendegi', '4.3', 'Published', 'Details', 'Edit', 'Delete'],
            ['After Life', '4.1', 'Published', 'Details', 'Edit', 'Delete'],
            ['After Zendegi', '0.0', 'Draft', 'Details', 'Edit', 'Delete']
        ]

        all_movies_frame = ctk.CTkFrame(parent, fg_color='transparent')
        all_movies_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        temp_frame = ctk.CTkFrame(all_movies_frame, fg_color='transparent')
        temp_frame.pack(expand=True, fill='x')
        SectionTitle(temp_frame, text='All Movies').pack(padx=30, side=tkinter.LEFT)
        search_box_frame = ctk.CTkFrame(temp_frame, fg_color='transparent')
        search_box_frame.pack(padx=30, side=tkinter.RIGHT)
        search_box_entry = ctk.CTkEntry(search_box_frame, placeholder_text='Search here...', width=200)
        search_box_entry.grid(row=0, column=0, padx=10)
        ctk.CTkButton(search_box_frame, text='Go!', width=60).grid(row=0, column=1)
        all_movies_table = CTkTable(all_movies_frame, values=all_movies_list, hover=True, column_hover=[3, 4, 5],
                                    column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                    column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'], not_hover_rows=[0])
        all_movies_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)

    def select_file(self):
        file_name = filedialog.askopenfilename()
        print(file_name)
        return file_name

    def load_articles_tab(self, parent):
        from modules.plainInput import PlainInput

        # disable target tab button and enable other tabs button
        self.articles_button.configure(state='disabled')
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
        ctk.CTkLabel(article_body_frame, text='Article Body:', text_color='gray', font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        article_body_input = ctk.CTkTextbox(article_body_frame)
        article_body_input.grid(row=1, column=0, sticky='ew')

        article_cover = None
        article_cover_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
        article_cover_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(article_cover_frame, text='Article Cover:', text_color='gray', font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(article_cover_frame, text='Add Cover', command=self.select_file).grid(row=1, column=0, sticky='w')
        selected_cover_count_label = ctk.CTkLabel(article_cover_frame,
                                                  text=article_cover and 'Article Cover Has Been Selected!' or 'Please Select Article Cover')
        selected_cover_count_label.grid(row=0, column=1, padx=20)

        submit_form_buttons_frame = ctk.CTkFrame(add_new_article_frame, fg_color='transparent')
        submit_form_buttons_frame.grid(row=4, column=0, columnspan=3, pady=40)
        ctk.CTkButton(submit_form_buttons_frame, text='Create').grid(row=0, column=0)
        ctk.CTkButton(submit_form_buttons_frame, text='Save As Draft', fg_color='#EF5350', hover_color='#C62828').grid(
            row=0, column=1, padx=30)

        all_articles_list = [
            ['Title', 'Rate', 'Status', 'Details', 'Edit', 'Delete'],
            ['After Jendegi', '4.3', 'Published', 'Details', 'Edit', 'Delete'],
            ['After Life', '4.1', 'Published', 'Details', 'Edit', 'Delete'],
            ['After Zendegi', '0.0', 'Draft', 'Details', 'Edit', 'Delete']
        ]

        all_articles_frame = ctk.CTkFrame(parent, fg_color='transparent')
        all_articles_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        temp_frame = ctk.CTkFrame(all_articles_frame, fg_color='transparent')
        temp_frame.pack(expand=True, fill='x')
        SectionTitle(temp_frame, text='All Articles').pack(padx=30, side=tkinter.LEFT)
        search_box_frame = ctk.CTkFrame(temp_frame, fg_color='transparent')
        search_box_frame.pack(padx=30, side=tkinter.RIGHT)
        search_box_entry = ctk.CTkEntry(search_box_frame, placeholder_text='Search here...', width=200)
        search_box_entry.grid(row=0, column=0, padx=10)
        ctk.CTkButton(search_box_frame, text='Go!', width=60).grid(row=0, column=1)
        all_articles_table = CTkTable(all_articles_frame, values=all_articles_list, hover=True, column_hover=[3, 4, 5],
                                      column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                      column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'], not_hover_rows=[0])
        all_articles_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)

    def load_comments_tab(self, parent):
        # disable target tab button and enable other tabs button
        self.comments_button.configure(state='disabled')
        self.my_profile_button.configure(state='normal')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')
        self.users_button.configure(state='normal')
        self.articles_button.configure(state='normal')
        self.movies_button.configure(state='normal')

        # empty widgets in the parent
        for widget in parent.winfo_children():
            widget.destroy()

        all_waiting_comments = [
            ['User', 'Page', 'Rate', 'Status', 'Body', 'Approve', 'Reject'],
            ['MohamadAmin Gharibi', 'After Life', '4.5', 'Approved', 'See', 'Approve', 'Reject'],
            ['Amin Gharibi', 'After Jendegi', '1.2', 'Rejected', 'See', 'Approve', 'Reject'],
            ['Amir Testi', 'After Zendegi', '3.4', '--', 'See', 'Approve', 'Reject']
        ]

        all_waiting_comments_frame = ctk.CTkFrame(parent, fg_color='transparent')
        all_waiting_comments_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=20)
        SectionTitle(all_waiting_comments_frame, text='Comments Waiting List').pack(padx=30, anchor='w')
        all_articles_table = CTkTable(all_waiting_comments_frame, values=all_waiting_comments, hover=True,
                                      column_hover=[4, 5, 6],
                                      column_hover_text_color=['#F57C00', '#F57C00', '#F57C00'],
                                      column_hover_bg_color=['#1B5E20', '#1B5E20', '#B71C1C'], not_hover_rows=[0])
        all_articles_table.pack(expand=True, fill='both', pady=(10, 0), padx=20)
