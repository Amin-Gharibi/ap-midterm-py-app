import customtkinter as ctk
from modules.sectionTitle import SectionTitle
from modules.comment import Comment


class CommentsSection(ctk.CTkFrame):
    def __init__(self, master, comments, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color='transparent')

        self.grid_columnconfigure(0, weight=1)

        # section title
        section_title = SectionTitle(self, 'Comments')
        section_title.grid(row=0, column=0, sticky='w', padx=(30, 0), pady=(50, 0))

        # new comment entry box
        comment_text_box = ctk.CTkTextbox(self)
        comment_text_box.grid(row=1, column=0, sticky='ew', padx=40, pady=(20, 0))

        # rate entry
        rate_entry = ctk.CTkEntry(self, placeholder_text='Enter Your Rate out of 10', width=200)
        rate_entry.grid(row=2, column=0, sticky='w', padx=40, pady=(10, 0))

        # submit comment to be added button
        submit_btn = ctk.CTkButton(self, text='Submit')
        submit_btn.grid(row=2, column=0, sticky='e', padx=40, pady=(10, 0))

        # comments container frame
        comments_container = ctk.CTkFrame(self)
        comments_container.grid_columnconfigure(0, weight=1)
        comments_container.grid(row=3, column=0, sticky='ew', padx=40, pady=(20, 10))

        # create each comments template from the backend
        for index, comment in enumerate(comments):
            Comment(comments_container, comment, fg_color='gray23').grid(row=index, column=0, sticky='ew', padx=20, pady=20)
