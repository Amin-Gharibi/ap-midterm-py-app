import tkinter

import customtkinter as ctk
from modules.sectionTitle import SectionTitle
from modules.comment import Comment


class CommentsSection(ctk.CTkFrame):
    def __init__(self, master, comments, page_id, page_type, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color='transparent')

        self.grid_columnconfigure(0, weight=1)

        self.replying_comment_id = None
        self.page_id = page_id
        self.page_type = page_type

        # section title
        section_title = SectionTitle(self, 'Comments')
        section_title.grid(row=0, column=0, sticky='w', padx=(30, 0), pady=(50, 0))

        # new comment entry box
        self.comment_text_box = ctk.CTkTextbox(self)
        self.comment_text_box.grid(row=1, column=0, sticky='ew', padx=40, pady=(20, 0))

        # rate entry
        self.rate_entry = ctk.CTkEntry(self, placeholder_text='Enter Your Rate out of 10', width=200)
        self.rate_entry.grid(row=2, column=0, sticky='w', padx=40, pady=(10, 0))

        # submit comment to be added button
        submit_btn = ctk.CTkButton(self, text='Submit', command=self.submit_comment)
        submit_btn.grid(row=2, column=0, sticky='e', padx=40, pady=(10, 0))

        # comments container frame
        comments_container = ctk.CTkFrame(self)
        comments_container.grid_columnconfigure(0, weight=1)
        comments_container.grid(row=3, column=0, sticky='ew', padx=40, pady=(20, 10))

        # create each comments template from the backend
        for index, comment in enumerate(comments):
            Comment(comments_container, comment, fg_color='gray23', has_like_button=True).grid(row=index, column=0, sticky='ew', padx=20, pady=20)

        if not len(comments):
            ctk.CTkLabel(comments_container, text='No Comments Yet...! Be The First One To Tell Your Opinion :)', height=150).grid(row=0, column=0, sticky='ew')

    def submit_comment(self):
        from api_services.comment import create_comment
        from CTkMessagebox import CTkMessagebox
        create_result = create_comment(body=self.comment_text_box.get("1.0", tkinter.END), page=self.page_id, pageModel=self.page_type, rate=self.rate_entry.get(), parentComment=self.replying_comment_id)
        if create_result['ok']:
            CTkMessagebox(title='Success', message='Your comment submitted successfully!', icon='check')
        else:
            CTkMessagebox(title='Success', message=create_result['message'], icon='check')

    def destroy_rate_entry(self):
        self.rate_entry.destroy()

    def create_rate_entry(self):
        self.rate_entry = ctk.CTkEntry(self, placeholder_text='Enter Your Rate out of 10', width=200)
        self.rate_entry.grid(row=2, column=0, sticky='w', padx=40, pady=(10, 0))