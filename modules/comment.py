import customtkinter as ctk
from PIL import Image
from math import ceil


class Comment(ctk.CTkFrame):
    def __init__(self, master, comment, fg_color, is_respond=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=fg_color)

        self.grid_columnconfigure(0, weight=1)

        # container to hold user profile picture and user's name
        user_prof_name_frame = ctk.CTkFrame(self, fg_color='transparent')
        user_prof_name_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # user profile pic
        image = ctk.CTkImage(dark_image=Image.open(comment['user']['profile_pic']), size=(30, 30))
        user_prof_pic = ctk.CTkLabel(user_prof_name_frame, image=image, text='')
        user_prof_pic.grid(row=0, column=0)

        user_name_role_frame = ctk.CTkFrame(user_prof_name_frame, fg_color='transparent')
        user_name_role_frame.grid(row=0, column=1, padx=(10, 0))

        # user's name
        user_name = ctk.CTkLabel(user_name_role_frame, text=comment['user']['name'], font=('Arial', 14, 'bold'), height=10)
        user_name.grid(row=0, column=0)

        # user role
        user_role = ctk.CTkLabel(user_name_role_frame, text=comment['user']['role'], font=('Arial', 12), text_color='gray', height=10)
        user_role.grid(row=1, column=0, sticky='w')

        # release date of the comment
        approve_date = ctk.CTkLabel(self, fg_color='transparent', text='14/07/2005', font=('Arial', 12, 'italic'), text_color='gray')
        approve_date.grid(row=0, column=0, sticky='e', padx=10, pady=10)

        # comment body container
        comment_body = ctk.CTkLabel(self, fg_color='transparent', text=comment['body'], font=('Arial', 14))
        comment_body.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        # if the comment wasn't a response type comment then add reply button
        if not is_respond:
            reply_button = ctk.CTkButton(self, text='Reply', width=50)
            reply_button.grid(row=2, column=0, sticky='e', padx=10, pady=(0, 10))

            # user rate label
            rate_label = ctk.CTkLabel(self, text=f'{comment['rate']}/10 {ceil(comment['rate']) * '⭐'}', text_color='yellow', font=('Arial', 12, 'italic'))
            rate_label.grid(row=2, column=0, sticky='w', padx=10, pady=(0, 10))

        # if the comment had responds then add a frame to store them and create a comment component for each of them
        if 'responds' in comment.keys() and len(comment['responds']):
            responds_frame = ctk.CTkFrame(self, fg_color='transparent')
            responds_frame.grid_columnconfigure(0, weight=1)
            responds_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=10)

            for index, cmnt in enumerate(comment['responds']):
                Comment(responds_frame, cmnt, self.master.cget('fg_color'), True).grid(row=index, column=0, sticky='ew')