import customtkinter as ctk
from PIL import Image
from math import ceil
import requests
from io import BytesIO
from datetime import datetime
from urllib.parse import urlparse
from os import getenv


class Comment(ctk.CTkFrame):
    def __init__(self, master, comment, fg_color, is_reply=False, has_movie_name=False, has_reply_btn=True, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=fg_color)

        self.grid_columnconfigure(0, weight=1)

        # container to hold user profile picture and user's name
        user_prof_name_frame = ctk.CTkFrame(self, fg_color='transparent')
        user_prof_name_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # user profile pic
        parsed_url = urlparse(getenv('BASE_URL'))
        res = requests.get(f"{parsed_url.scheme}://{parsed_url.netloc}/usersProfilePictures/{comment['user']['profilePic']}")
        image = ctk.CTkImage(dark_image=Image.open(BytesIO(res.content)), size=(30, 30))
        user_prof_pic = ctk.CTkLabel(user_prof_name_frame, image=image, text='')
        user_prof_pic.grid(row=0, column=0)

        user_name_role_frame = ctk.CTkFrame(user_prof_name_frame, fg_color='transparent')
        user_name_role_frame.grid(row=0, column=1, padx=(10, 0))

        # user's name
        user_name = ctk.CTkLabel(user_name_role_frame, text=comment['user']['username'] if not has_movie_name else f'{comment["user"]["username"]} · {comment["page"]["fullName"] or comment['page']['title']}', font=('Arial', 14, 'bold'), height=10)
        user_name.grid(row=0, column=0)

        # user role
        user_role = ctk.CTkLabel(user_name_role_frame, text=comment['user']['role'], font=('Arial', 12), text_color='gray', height=10)
        user_role.grid(row=1, column=0, sticky='w')

        # release date of the comment
        dt = datetime.strptime(comment['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        approve_date = ctk.CTkLabel(self, fg_color='transparent', text=dt.strftime("%d/%m/%Y"), font=('Arial', 12, 'italic'), text_color='gray')
        approve_date.grid(row=0, column=0, sticky='e', padx=10, pady=10)

        # comment body container
        comment_body = ctk.CTkLabel(self, fg_color='transparent', text=comment['body'], font=('Arial', 14), anchor='w', justify='left')
        comment_body.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        # if the comment wasn't a response type comment then add reply button
        if not is_reply:
            if has_reply_btn:
                reply_button = ctk.CTkButton(self, text='Reply', width=50)
                reply_button.grid(row=2, column=0, sticky='e', padx=10, pady=(0, 10))

            # user rate label
            rate_label = ctk.CTkLabel(self, text=f'{'rate' in comment.keys() and comment['rate'] or '0'}/10 {'rate' in comment.keys() and ceil(comment['rate']) * '⭐' or ''}', text_color='yellow', font=('Arial', 12, 'italic'))
            rate_label.grid(row=2, column=0, sticky='w', padx=10, pady=(0, 10))

        # if the comment had responds then add a frame to store them and create a comment component for each of them
        if 'replies' in comment.keys() and len(comment['replies']):
            replies_frame = ctk.CTkFrame(self, fg_color='transparent')
            replies_frame.grid_columnconfigure(0, weight=1)
            replies_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=10)

            for index, cmnt in enumerate(comment['responds']):
                Comment(replies_frame, cmnt, self.master.cget('fg_color'), True).grid(row=index, column=0, sticky='ew')