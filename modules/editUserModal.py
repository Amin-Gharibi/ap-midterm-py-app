import customtkinter as ctk
from modules.modalWindow import ModalWindow
from api_services.user import get_user_by_id
from modules.sectionTitle import SectionTitle
from modules.plainInput import PlainInput
from tkinter import filedialog


class EditUserModal(ModalWindow):
    def __init__(self, master, user_id):
        super().__init__(master, geometry='700x550', title='Edit User')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.user_id = user_id
        self.user = get_user_by_id(self.user_id)['user']

        edit_user_form_frame = ctk.CTkFrame(self, fg_color='transparent')
        edit_user_form_frame.grid_columnconfigure((0, 1), weight=1)
        edit_user_form_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        edit_user_form_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        SectionTitle(edit_user_form_frame, text='Edit User ').grid(row=0, column=0, sticky='w', padx=10, pady=(0, 10))

        self.email_entry = PlainInput(master=edit_user_form_frame, label_text='Email:',
                                      input_placeholder="Enter user's Email Address...", input_value=self.user['email'])
        self.email_entry.grid(row=1, column=0)

        self.username_entry = PlainInput(master=edit_user_form_frame, label_text='Username:',
                                         input_placeholder="Enter user's Username...",
                                         input_value=self.user['username'])
        self.username_entry.grid(row=1, column=1)

        self.password_entry = PlainInput(master=edit_user_form_frame,
                                         label_text="NEW Password:(don't fill out if don't want to change)",
                                         input_placeholder="Enter user's NEW Password...")
        self.password_entry.grid(row=2, column=0, pady=10)

        self.full_name_entry = PlainInput(master=edit_user_form_frame, label_text='Full Name:',
                                          input_placeholder="Enter user's Full Name...",
                                          input_value=self.user['fullName'])
        self.full_name_entry.grid(row=2, column=1, pady=10)

        role_frame = ctk.CTkFrame(edit_user_form_frame, fg_color='transparent')
        role_frame.grid(row=3, column=0)
        ctk.CTkLabel(role_frame, text="Role:", text_color='gray', font=("Arial", 12, 'italic')).grid(row=0, column=0,
                                                                                                     sticky='nw')
        self.role_entry = ctk.CTkOptionMenu(role_frame, width=300, height=40, values=["ADMIN", "USER", "CRITIC"],
                                            fg_color=['#F9F9FA', '#343638'])
        self.role_entry.set(self.user['role'])
        self.role_entry.grid(row=1, column=0, sticky='ew')

        self.selected_user_profile = None
        user_profile_frame = ctk.CTkFrame(edit_user_form_frame, fg_color='transparent')
        user_profile_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=20)
        ctk.CTkLabel(user_profile_frame, text='Profile Picture:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(user_profile_frame, text="Select New Profile Picture",
                      command=self.select_profile_pic_handler).grid(row=1,
                                                                    column=0,
                                                                    sticky='w')
        self.selected_profile_label = ctk.CTkLabel(user_profile_frame,
                                                   text="If You Don't Want To Change The Profile Picture, Leave This Field Empty")
        self.selected_profile_label.grid(row=0, column=1, padx=20)

        ctk.CTkButton(self, text='Save', height=30,
                      command=self.handle_updating_user).grid(row=1, column=0, columnspan=2, sticky='s', pady=20)

    def select_profile_pic_handler(self):
        self.selected_user_profile = filedialog.askopenfilename()
        self.selected_user_profile = self.selected_user_profile if self.selected_user_profile else None
        if self.selected_user_profile:
            self.selected_profile_label.configure(text='Profile Picture Selected Successfully!')

    def handle_updating_user(self):
        from api_services.user import update_user
        from CTkMessagebox import CTkMessagebox

        update_result = update_user(user_id=self.user_id,
                                    email=self.email_entry.input.get(),
                                    username=self.username_entry.input.get(),
                                    updatingPassword=self.password_entry.input.get() or None,
                                    fullName=self.full_name_entry.input.get(),
                                    profilePic=self.selected_user_profile,
                                    role=self.role_entry.get())

        if update_result['ok']:
            CTkMessagebox(title='Success', message='User Edited Successfully!', icon='check')
            super().on_close()
            self.master.update_all_users_table()
        else:
            CTkMessagebox(title='Error', message=update_result['message'], icon='cancel')
