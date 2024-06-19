import customtkinter as ctk
from modules.modalWindow import ModalWindow
from modules.sectionTitle import SectionTitle
from modules.plainInput import PlainInput
from api_services.articles import get_article_by_id
from tkinter import filedialog


class EditArticleModal(ModalWindow):
    def __init__(self, master, article_id):
        super().__init__(master, geometry='700x550', title='Edit Article')

        self.article_id = article_id
        self.article = get_article_by_id(self.article_id)['targetArticle']

        self.grid_columnconfigure(0, weight=1)

        edit_article_form_frame = ctk.CTkFrame(self, fg_color='transparent')
        edit_article_form_frame.grid_columnconfigure((0, 1, 2), weight=1)
        edit_article_form_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=20)
        SectionTitle(edit_article_form_frame, text='Edit Article').grid(row=0, column=0, sticky='w', padx=30,
                                                                         pady=(0, 20))
        self.article_title_entry = PlainInput(edit_article_form_frame, label_text='Article Title:',
                                              input_placeholder="Enter Article Title...", input_value=self.article['title'])
        self.article_title_entry.grid(row=1, column=0, sticky='w', padx=45)

        article_body_frame = ctk.CTkFrame(edit_article_form_frame, fg_color='transparent')
        article_body_frame.grid_columnconfigure(0, weight=1)
        article_body_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=45, pady=10)
        ctk.CTkLabel(article_body_frame, text='Article Body:', text_color='gray',
                     font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        self.article_body_entry = ctk.CTkTextbox(article_body_frame)
        self.article_body_entry.grid(row=1, column=0, sticky='ew')
        self.article_body_entry.delete("1.0", ctk.END)
        self.article_body_entry.insert("1.0", self.article['body'])

        self.selected_article_cover = None
        article_cover_frame = ctk.CTkFrame(edit_article_form_frame, fg_color='transparent')
        article_cover_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(article_cover_frame, text='Article Cover:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(article_cover_frame, text="Select New Cover", command=self.select_article_cover).grid(row=1,
                                                                                                     column=0,
                                                                                                     sticky='w')
        self.selected_cover_label = ctk.CTkLabel(article_cover_frame,
                                                 text="If You Don't Want To Change The Cover, Leave This Field Empty")
        self.selected_cover_label.grid(row=0, column=1, padx=20)

        ctk.CTkButton(self, text='Save',
                      command=self.update_article_handler).grid(row=1, column=0)

    def select_article_cover(self):
        self.selected_article_cover = filedialog.askopenfilename()
        self.selected_cover_label.configure(text='Cover Selected Successfully!')

    def update_article_handler(self):
        from api_services.articles import update_article
        from CTkMessagebox import CTkMessagebox

        update_result = update_article(article_id=self.article_id,
                                       title=self.article_title_entry.input.get(),
                                       body=self.article_body_entry.get("1.0", ctk.END),
                                       cover=self.selected_article_cover)

        if update_result['ok']:
            CTkMessagebox(title='Success', message='Article Edited Successfully!', icon='check')
            super().on_close()
            self.master.update_my_articles_table()
        else:
            CTkMessagebox(title='Error', message=update_result['message'], icon='cancel')
