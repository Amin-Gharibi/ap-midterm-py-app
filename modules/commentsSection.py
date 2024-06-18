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
        self.cancel_replying_button = None
        self.section_title = None

        # section title
        self.set_section_title('Comments')

        # new comment entry box
        self.comment_text_box = ctk.CTkTextbox(self)
        self.comment_text_box.grid(row=1, column=0, sticky='ew', padx=40, pady=(20, 0))

        # rate entry
        self.rate_entry = ctk.CTkEntry(self, placeholder_text='Enter Your Rate out of 10', width=200)
        self.rate_entry.grid(row=2, column=0, sticky='w', padx=40, pady=(10, 0))

        self.options_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.options_frame.grid(row=2, column=0, sticky='e', padx=40, pady=(10, 0))
        self.options_frame.grid_columnconfigure((0, 1), weight=1)
        # submit comment to be added button
        submit_btn = ctk.CTkButton(self.options_frame, text='Submit', command=self.submit_comment)
        submit_btn.grid(row=0, column=1, sticky='e')

        # comments container frame
        comments_container = ctk.CTkFrame(self)
        comments_container.grid_columnconfigure(0, weight=1)
        comments_container.grid(row=3, column=0, sticky='ew', padx=40, pady=(20, 10))

        # create each comments template from the backend
        for index, comment in enumerate(comments):
            Comment(comments_container, comment, fg_color='gray23', has_like_button=True).grid(row=index, column=0, sticky='ew', padx=20, pady=20)

        if not len(comments):
            ctk.CTkLabel(comments_container, text='No Comments Yet...! Be The First One To Tell Your Opinion :)', height=150).grid(row=0, column=0, sticky='ew')

    def set_section_title(self, title):
        if self.section_title:
            self.section_title.destroy()
        self.section_title = SectionTitle(self, title)
        self.section_title.grid(row=0, column=0, sticky='w', padx=(30, 0), pady=(50, 0))

    def ready_replying(self, title, comment_id):
        self.rate_entry.grid_forget()
        self.set_section_title(f'Comments{title}')
        self.replying_comment_id = comment_id
        self.cancel_replying_button = ctk.CTkButton(self.options_frame, text='Cancel Replying', command=self.abort_replying)
        self.cancel_replying_button.grid(row=0, column=0, sticky='e', padx=20)
        self.comment_text_box.delete("1.0", ctk.END)

    def abort_replying(self):
        self.rate_entry.grid(row=2, column=0, sticky='w', padx=40, pady=(10, 0))
        self.set_section_title('Comments')
        if self.cancel_replying_button:
            self.cancel_replying_button.grid_forget()
        self.replying_comment_id = None
        self.comment_text_box.delete("1.0", ctk.END)

    def submit_comment(self):
        from api_services.comment import create_comment
        from CTkMessagebox import CTkMessagebox
        create_result = create_comment(body=self.comment_text_box.get("1.0", ctk.END), page=self.page_id, pageModel=self.page_type, rate=self.rate_entry.get() or None, parentComment=self.replying_comment_id)
        if create_result['ok']:
            CTkMessagebox(title='Success', message='Your comment submitted successfully!', icon='check')
            self.abort_replying()
        else:
            CTkMessagebox(title='Success', message=create_result['message'], icon='check')
