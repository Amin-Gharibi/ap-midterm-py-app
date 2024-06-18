import customtkinter as ctk
from PIL import Image
from math import ceil
import requests
from io import BytesIO
from datetime import datetime
from urllib.parse import urlparse
from os import getenv
from api_services.auth import get_me


class Comment(ctk.CTkFrame):
    def __init__(self, master, comment, fg_color, is_reply=False, has_movie_name=False, has_reply_btn=True,
                 has_like_button=False, has_like_label=False, has_delete_btn=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=fg_color)

        self.comment = comment

        self.grid_columnconfigure(0, weight=1)

        # container to hold user profile picture and user's name
        user_prof_name_frame = ctk.CTkFrame(self, fg_color='transparent')
        user_prof_name_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        # user profile pic
        parsed_url = urlparse(getenv('BASE_URL'))
        res = requests.get(
            f"{parsed_url.scheme}://{parsed_url.netloc}/usersProfilePictures/{self.comment['user']['profilePic']}")
        image = ctk.CTkImage(dark_image=Image.open(BytesIO(res.content)), size=(30, 30))
        user_prof_pic = ctk.CTkLabel(user_prof_name_frame, image=image, text='')
        user_prof_pic.grid(row=0, column=0)

        user_name_role_frame = ctk.CTkFrame(user_prof_name_frame, fg_color='transparent')
        user_name_role_frame.grid(row=0, column=1, padx=(10, 0))

        # user's name
        user_name = ctk.CTkLabel(user_name_role_frame, text=self.comment['user'][
            'username'] if not has_movie_name else f'{self.comment["user"]["username"]} · {self.comment["page"]["fullName"] or self.comment['page']['title']}',
                                 font=('Arial', 14, 'bold'), height=10)
        user_name.grid(row=0, column=0)

        # user role
        user_role = ctk.CTkLabel(user_name_role_frame, text=self.comment['user']['role'], font=('Arial', 12),
                                 text_color='gray', height=10)
        user_role.grid(row=1, column=0, sticky='w')

        # release date of the comment
        dt = datetime.strptime(self.comment['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        create_date = ctk.CTkLabel(self, fg_color='transparent', text=dt.strftime("%d/%m/%Y"),
                                   font=('Arial', 12, 'italic'), text_color='gray')
        create_date.grid(row=0, column=0, sticky='e', padx=10, pady=10)

        # comment body container
        comment_body = ctk.CTkLabel(self, fg_color='transparent', text=self.comment['body'], font=('Arial', 14),
                                    anchor='w',
                                    justify='left')
        comment_body.grid(row=1, column=0, sticky='w', padx=10, pady=10)

        options_frame = ctk.CTkFrame(self, fg_color='transparent')
        options_frame.grid(row=2, column=0, sticky='e', padx=10, pady=(0, 10))
        options_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # if the comment wasn't a response type comment then add reply button
        if not is_reply:
            if has_reply_btn:
                reply_button = ctk.CTkButton(options_frame, text='Reply', width=50, command=self.handle_replying)
                reply_button.grid(row=0, column=2, sticky='e', padx=(0, 10), pady=(0, 10))

            # user rate label
            rate_label = ctk.CTkLabel(self,
                                      text=f'{'rate' in self.comment.keys() and self.comment['rate'] or '0'}/10 {'rate' in self.comment.keys() and ceil(self.comment['rate']) * '⭐' or ''}',
                                      text_color='yellow', font=('Arial', 12, 'italic'))
            rate_label.grid(row=2, column=0, sticky='w', padx=10, pady=(0, 10))

        if has_like_button:
            data = get_me()
            self.user = data['user'] if data else None

            self.like_button = ctk.CTkButton(options_frame, text=f'Likes {len(self.comment['likes'])}',
                                             command=lambda: self.handle_liking(operation='like'),
                                             width=50)
            self.like_button.grid(row=0, column=1, sticky='e', padx=10, pady=(0, 10))
            self.dislike_button = ctk.CTkButton(options_frame, text=f'DisLikes {len(self.comment['disLikes'])}',
                                                command=lambda: self.handle_liking(operation='dislike'),
                                                width=50)
            self.dislike_button.grid(row=0, column=0, sticky='e', pady=(0, 10))
            if self.user:
                for user_id in comment['likes']:
                    if self.user['_id'] == user_id['_id']:
                        self.like_button.configure(state='disabled')

                for user_id in comment['disLikes']:
                    if self.user['_id'] == user_id['_id']:
                        self.dislike_button.configure(state='disabled')
        elif has_like_label:
            ctk.CTkLabel(options_frame, text=f'Likes: {len(self.comment['likes'])}', text_color='gray').grid(row=0,
                                                                                                             column=2)
            ctk.CTkLabel(options_frame, text=f'DisLikes: {len(self.comment['disLikes'])}', text_color='gray').grid(
                row=0, column=1, padx=10)

        if has_delete_btn:
            ctk.CTkButton(options_frame, text='🗑', font=('Arial', 16), width=50, fg_color='#EF5350', hover_color='#C62828', command=self.handle_deleting).grid(row=0, column=0)

        # if the comment had replies then add a frame to store them and create a comment component for each of them
        if 'replies' in comment.keys() and len(comment['replies']):
            replies_frame = ctk.CTkFrame(self, fg_color='transparent')
            replies_frame.grid_columnconfigure(0, weight=1)
            replies_frame.grid(row=3, column=0, sticky='ew', padx=20)

            for index, cmnt in enumerate(comment['replies']):
                Comment(replies_frame, cmnt, self.master.cget('fg_color'), is_reply=True, has_like_button=True).grid(row=index, column=0, sticky='ew', pady=10)

    def handle_liking(self, operation):
        from api_services.comment import like_comment, dislike_comment, get_comment_by_id
        if not self.user:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title='Error', message='For Liking Or Disliking Comments You Have To Login First!')
            return None

        operation_result = None
        if operation == 'like':
            operation_result = like_comment(self.comment['_id'])
        elif operation == 'dislike':
            operation_result = dislike_comment(self.comment['_id'])

        self.comment = get_comment_by_id(self.comment['_id'])['targetComment']

        if not operation_result['ok']:
            from CTkMessagebox import CTkMessagebox
            CTkMessagebox(title='Error',
                          message=f'Failed To {operation.upper()} Comment! {operation_result['message']}',
                          icon='cancel')
        else:
            if operation == 'like':
                self.like_button.configure(text=f'Likes {len(self.comment['likes'])}', state='disabled')
                self.dislike_button.configure(text=f'Dislikes {len(self.comment['disLikes'])}', state='normal')
            if operation == 'dislike':
                self.like_button.configure(text=f'Likes {len(self.comment['likes'])}', state='normal')
                self.dislike_button.configure(text=f'Dislikes {len(self.comment['disLikes'])}', state='disabled')

    def handle_deleting(self):
        from api_services.comment import delete_comment
        from CTkMessagebox import CTkMessagebox
        delete_result = delete_comment(self.comment['_id'])
        if delete_result['ok']:
            CTkMessagebox(title='Success', message='Comment Deleted Successfully!', icon='check')
            self.destroy()
        else:
            CTkMessagebox(title='Error', message=f'Failed To Delete Comment! {delete_result['message']}', icon='cancel')

    def handle_replying(self):
        self.master.master.ready_replying(title=f' - Replying to {self.comment['user']['username']}', comment_id=self.comment['_id'])
