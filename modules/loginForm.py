import customtkinter as ctk
from modules.plainInput import PlainInput


class LoginForm(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=master.cget("bg"))

        # page title
        self.middle_page_title = ctk.CTkLabel(self, text="LOGIN ", font=("Arial", 36, 'italic'))
        self.middle_page_title.grid(row=0, column=0)

        # identifier field entry input
        self.identifier_entry = PlainInput(master=self, label_text="Email or Username:",
                                           input_placeholder="Enter your Email or Username",)
        self.identifier_entry.grid(row=1, column=0, pady=(40, 0))

        # password field entry input
        self.identifier_entry = PlainInput(master=self, label_text="Password:",
                                           input_placeholder="Enter your Password", )
        self.identifier_entry.grid(row=2, column=0, pady=(10, 0))

        # submit button
        self.submit_button = ctk.CTkButton(self, text="Login", width=150, height=30)
        self.submit_button.grid(row=3, column=0, pady=(15, 0))

        # go to signup page button
        self.switch_to_sign_up = ctk.CTkButton(self, text="you don't have an account? Sign Up here!",
                                               fg_color='transparent', hover_color=self.cget('fg_color'),
                                               cursor='hand2', text_color='#78909C')
        self.switch_to_sign_up.grid(row=4, column=0, pady=(30, 0))
