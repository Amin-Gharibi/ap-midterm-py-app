from tkinter import filedialog
import customtkinter as ctk
from modules.plainInput import PlainInput
from PIL import Image


class UserDashboard(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # configure page grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        welcome_label = ctk.CTkLabel(self, text="Welcome Dear MohamadAmin Gharibi ", font=("Arial", 20, "italic"))
        welcome_label.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

        # frame to hold the header navbar
        navbar_frame = ctk.CTkFrame(self)
        navbar_frame.grid(row=1, column=0, sticky='n', pady=5)

        self.my_profile_button = ctk.CTkButton(navbar_frame, text="My Profile", command=lambda: self.load_my_profile_section(dynamic_content_frame))
        self.my_profile_button.grid(row=0, column=0, padx=20, pady=20)

        self.my_comments_button = ctk.CTkButton(navbar_frame, text="My Comments")
        self.my_comments_button.grid(row=0, column=1, padx=20, pady=20)

        self.my_favorite_movies_button = ctk.CTkButton(navbar_frame, text="My Favorite Movies")
        self.my_favorite_movies_button.grid(row=0, column=2, padx=20, pady=20)

        self.my_favorite_articles_button = ctk.CTkButton(navbar_frame, text="My Favorite Articles")
        self.my_favorite_articles_button.grid(row=0, column=3, padx=20, pady=20)

        # this frame would contain each tab's content
        dynamic_content_frame = ctk.CTkScrollableFrame(self)
        dynamic_content_frame.grid(row=3, column=0, sticky='nsew')

        # handle its grid system
        dynamic_content_frame.grid_columnconfigure(0, weight=1)
        dynamic_content_frame.grid_columnconfigure(1, weight=1)

    def select_file(self):
        file_name = filedialog.askopenfilename()
        print(file_name)
        return file_name

    def load_my_profile_section(self, parent):
        # disable target tab button and enable other tabs button
        self.my_profile_button.configure(state='disabled')
        self.my_comments_button.configure(state='normal')
        self.my_favorite_movies_button.configure(state='normal')
        self.my_favorite_articles_button.configure(state='normal')

        # frame to contain left inputs
        left_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        left_content_frame.grid(row=0, column=0, sticky='nw')

        username_entry = PlainInput(left_content_frame, "Username:", "Enter your username...")
        username_entry.grid(row=0, column=0, sticky='nw', padx=20, pady=20)

        name_entry = PlainInput(left_content_frame, "Name:", "Enter your name...")
        name_entry.grid(row=1, column=0, sticky='nw', padx=20)

        phone_number_entry = PlainInput(left_content_frame, "Phone Number:", "Enter your phone number...")
        phone_number_entry.grid(row=2, column=0, sticky='nw', padx=20, pady=20)

        # frame to contain profile picture and its picker
        right_content_frame = ctk.CTkFrame(parent, fg_color='transparent')
        right_content_frame.grid(row=0, column=1, pady=(20, 0))
        right_content_frame.grid_columnconfigure(0, weight=1)

        # Load the image
        image = Image.open('images/imdb_logo.png')
        profile_pic_label = ctk.CTkLabel(right_content_frame, text="",
                                         image=ctk.CTkImage(dark_image=image, size=(300, 300)))
        profile_pic_label.grid(row=0, column=0)

        pick_new_profile_button = ctk.CTkButton(right_content_frame, text="Select New Profile",
                                                command=self.select_file)
        pick_new_profile_button.grid(row=1, column=0, pady=(20, 0))
