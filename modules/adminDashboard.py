import customtkinter as ctk
from modules.userDashboard import UserDashboard
from modules.sectionTitle import SectionTitle
from modules.ctktable import *


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        user_dashboard = UserDashboard(master=None)

        # configure page grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        welcome_label = ctk.CTkLabel(self, text="Welcome Dear MohamadAmin Gharibi ", font=("Arial", 20, "italic"))
        welcome_label.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

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

        self.my_favorite_articles_button = ctk.CTkButton(navbar_frame, text="My Favorite Articles",
                                                         command=lambda: user_dashboard.load_my_favorite_articles_tab(
                                                             dynamic_content_frame, self))
        self.my_favorite_articles_button.grid(row=0, column=3, padx=20, pady=20)

        self.users_button = ctk.CTkButton(navbar_frame, text="Users",
                                          command=lambda: self.load_users_tab(dynamic_content_frame))
        self.users_button.grid(row=0, column=4, padx=20, pady=20)

        self.movies_button = ctk.CTkButton(navbar_frame, text="Movies",
                                           command=lambda: user_dashboard.load_my_favorite_articles_tab(
                                               dynamic_content_frame, self))
        self.movies_button.grid(row=0, column=5, padx=20, pady=20)

        self.articles_button = ctk.CTkButton(navbar_frame, text="Articles",
                                             command=lambda: user_dashboard.load_my_favorite_articles_tab(
                                                 dynamic_content_frame, self))
        self.articles_button.grid(row=0, column=6, padx=20, pady=20)

        self.comments_button = ctk.CTkButton(navbar_frame, text="Comments",
                                             command=lambda: user_dashboard.load_my_favorite_articles_tab(
                                                 dynamic_content_frame, self))
        self.comments_button.grid(row=0, column=7, padx=20, pady=20)

        # this frame would contain each tab's content
        dynamic_content_frame = ctk.CTkScrollableFrame(self)
        dynamic_content_frame.grid(row=3, column=0, sticky='nsew')
        # handle its grid system
        dynamic_content_frame.grid_columnconfigure((0, 1), weight=1)

        # user_dashboard.load_my_profile_tab(dynamic_content_frame)
        self.load_users_tab(dynamic_content_frame)

    def load_users_tab(self, parent):
        from modules.plainInput import PlainInput

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

        email_entry = PlainInput(master=add_new_user_frame, label_text='Email:',
                                 input_placeholder="Enter user's Email Address...")
        email_entry.grid(row=1, column=0)

        username_entry = PlainInput(master=add_new_user_frame, label_text='Username:',
                                    input_placeholder="Enter user's Username...")
        username_entry.grid(row=1, column=1)

        password_entry = PlainInput(master=add_new_user_frame, label_text='Password:',
                                    input_placeholder="Enter user's Password...")
        password_entry.grid(row=1, column=2)

        full_name_entry = PlainInput(master=add_new_user_frame, label_text='Full Name:',
                                     input_placeholder="Enter user's Full Name...")
        full_name_entry.grid(row=2, column=0, pady=10)

        role_frame = ctk.CTkFrame(add_new_user_frame, fg_color='transparent')
        role_frame.grid(row=2, column=1, pady=10)
        ctk.CTkLabel(role_frame, text="Role:", text_color='gray', font=("Arial", 12, 'italic')).grid(row=0, column=0,
                                                                                                     sticky='nw')
        role_entry = ctk.CTkOptionMenu(role_frame, width=300, height=40, values=["test2", "test3"],
                                       fg_color=['#F9F9FA', '#343638'])
        role_entry.set("Choose user's Role...")
        role_entry.grid(row=1, column=0, sticky='ew')

        add_new_user_submit_btn = ctk.CTkButton(add_new_user_frame, text='Submit', height=30)
        add_new_user_submit_btn.grid(row=3, column=1, pady=(10, 0))

        # list of users waiting to be approved
        users_waiting_list_frame = ctk.CTkFrame(parent, fg_color='transparent')
        users_waiting_list_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=20, pady=(50, 0))

        SectionTitle(users_waiting_list_frame, text="Users Wait-List").pack(anchor='w')

        values = [['ID', 'Username', 'Full Name', 'Role', 'Approve', 'Reject'],
                  ['0', 'amingharibi', 'Mohamad Amin Gharibi', 'Admin', 'Approve', 'Reject'],
                  ['1', 'amin', 'Amin Gharibi', 'User', 'Approve', 'Reject'],
                  ['2', 'gharibi', 'Mohamad Gharibi', 'Montaghed', 'Approve', 'Reject'],
                  ['3', 'am_gh', 'MohamadAmin Gharibi', 'Admin', 'Approve', 'Reject']]

        wait_list_table = CTkTable(master=users_waiting_list_frame, row=5, column=6, values=values,
                                   command=self.handle_approving, hover=True, column_hover=[4, 5], not_hover_row=0,
                                   hover_color='#1B5E20')
        wait_list_table.pack(expand=True, fill='both', pady=(10, 0))

        all_users_list_frame = ctk.CTkFrame(parent, fg_color='transparent')
        all_users_list_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=20, pady=(50, 0))

        SectionTitle(all_users_list_frame, text='All Users').pack(anchor='w')

        all_users_table = CTkTable(master=all_users_list_frame, row=5, column=6, values=values,
                                   command=self.handle_approving, hover=True, column_hover=[4, 5], not_hover_row=0,
                                   hover_color='#1B5E20')
        all_users_table.pack(expand=True, fill='both', pady=(10, 0))

    def handle_approving(self, *kwargs):
        if kwargs[0]['row'] > 0 and kwargs[0]['column'] == 4:
            print('approved')
