import customtkinter as ctk
from modules.modalWindow import ModalWindow
from api_services.cast import get_one_cast
from modules.sectionTitle import SectionTitle
from modules.plainInput import PlainInput
from tkinter import filedialog


class EditCastModal(ModalWindow):
    def __init__(self, master, cast_id):
        super().__init__(master, geometry='700x700', title='Edit Cast')

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.cast_id = cast_id
        self.cast = get_one_cast(self.cast_id)['targetCast']

        edit_cast_form_frame = ctk.CTkFrame(self, fg_color='transparent')
        edit_cast_form_frame.grid_columnconfigure((0, 1), weight=1)
        edit_cast_form_frame.grid(row=0, column=0, sticky='nsew', pady=20)

        SectionTitle(edit_cast_form_frame, text='Edit Cast').grid(row=0, column=0, sticky='w', padx=20,
                                                                  pady=(0, 20))

        self.cast_name_entry = PlainInput(edit_cast_form_frame, label_text='Name:',
                                          input_placeholder="Enter Cast Name...", input_value=self.cast['fullName'])
        self.cast_name_entry.grid(row=1, column=0, columnspan=2, sticky='w', padx=20)

        cast_bio_frame = ctk.CTkFrame(edit_cast_form_frame, fg_color='transparent')
        cast_bio_frame.grid_columnconfigure(0, weight=1)
        cast_bio_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(cast_bio_frame, text='Biography:', text_color='gray', font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        self.cast_bio_input = ctk.CTkTextbox(cast_bio_frame, height=150)
        self.cast_bio_input.delete("1.0", ctk.END)
        self.cast_bio_input.insert("1.0", self.cast['biography'])
        self.cast_bio_input.grid(row=1, column=0, sticky='ew')

        self.cast_birth_date_entry = PlainInput(edit_cast_form_frame, label_text='Birth Date:',
                                                input_placeholder="Enter Cast Birth Date...",
                                                input_value=self.cast['birthDate'])
        self.cast_birth_date_entry.grid(row=3, column=0, padx=20)

        self.cast_birth_place_entry = PlainInput(edit_cast_form_frame, label_text='Birth Place:',
                                                 input_placeholder="Enter Birth Place...",
                                                 input_value=self.cast['birthPlace'])
        self.cast_birth_place_entry.grid(row=3, column=1, padx=20)

        self.cast_height_entry = PlainInput(edit_cast_form_frame, label_text='Height:',
                                            input_placeholder="Enter Cast Height...", input_value=self.cast['height'])
        self.cast_height_entry.grid(row=4, column=0, padx=20, pady=10)

        self.cast_profile_pic = None
        self.cast_page_photos = None

        cast_profile_pic_frame = ctk.CTkFrame(edit_cast_form_frame, fg_color='transparent')
        cast_profile_pic_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        ctk.CTkLabel(cast_profile_pic_frame, text="Cast Profile:", text_color='gray',
                     font=("Arial", 12, "italic")).grid(row=0, column=0, sticky='w')
        ctk.CTkButton(cast_profile_pic_frame, text='Add New Profile', command=self.select_cast_profile_pic).grid(row=1,
                                                                                                                 column=0,
                                                                                                                 sticky='w')
        self.selected_profile_pic_label = ctk.CTkLabel(cast_profile_pic_frame,
                                                  text="Select Cast New Profile (Don't Select If Don't Want To Change)")
        self.selected_profile_pic_label.grid(row=0, column=1, padx=20)

        cast_page_photos_frame = ctk.CTkFrame(edit_cast_form_frame, fg_color='transparent')
        cast_page_photos_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=20)
        ctk.CTkLabel(cast_page_photos_frame, text='Cast Page Photos:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(cast_page_photos_frame, text='Add New Photos', command=self.select_cast_page_pics).grid(row=1,
                                                                                                              column=0,
                                                                                                              sticky='w')
        self.selected_page_pics_label = ctk.CTkLabel(cast_page_photos_frame,
                                                text="Select Cast Page Photos (Don't Select If Don't Want To Change)")
        self.selected_page_pics_label.grid(row=0, column=1, padx=20)

        ctk.CTkButton(self, text='Save', command=self.handle_editing_cast).grid(row=1, column=0, pady=(0, 20))

    def select_cast_profile_pic(self):
        self.cast_profile_pic = filedialog.askopenfilename()
        self.cast_profile_pic = self.cast_profile_pic if self.cast_profile_pic else None
        if self.cast_profile_pic:
            self.selected_profile_pic_label.configure(text='New Profile Picture Selected!')

    def select_cast_page_pics(self):
        self.cast_page_photos = filedialog.askopenfilenames()
        self.cast_page_photos = self.cast_page_photos if self.cast_page_photos else None
        if self.cast_page_photos:
            self.selected_page_pics_label.configure(text='New Page Pictures Selected!')

    def handle_editing_cast(self):
        from api_services.cast import edit_cast
        from CTkMessagebox import CTkMessagebox

        update_result = edit_cast(cast_id=self.cast_id,
                                  fullName=self.cast_name_entry.input.get(),
                                  biography=self.cast_bio_input.get("1.0", ctk.END),
                                  birthDate=self.cast_birth_date_entry.input.get(),
                                  birthPlace=self.cast_birth_place_entry.input.get(),
                                  profilePic=self.cast_profile_pic,
                                  photos=self.cast_page_photos,
                                  height=self.cast_height_entry.input.get())

        if update_result['ok']:
            CTkMessagebox(title='Success', message='Cast Edited Successfully!', icon='check')
            super().on_close()
            self.master.update_all_casts_table()
        else:
            CTkMessagebox(title='Error', message=update_result['message'], icon='cancel')
