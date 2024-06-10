import customtkinter as ctk
from modules.plainInput import PlainInput
from CTkMessagebox import CTkMessagebox


class LoginForm(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master

        self.configure(fg_color=master.cget("bg"))

        # page title
        self.middle_page_title = ctk.CTkLabel(self, text="LOG IN ", font=("Arial", 36, 'italic'))
        self.middle_page_title.grid(row=0, column=0)

        # identifier field entry input
        self.identifier_entry = PlainInput(master=self, label_text="Email or Username:",
                                           input_placeholder="Enter your Email or Username", )
        self.identifier_entry.grid(row=1, column=0, pady=(40, 0))

        # password field entry input
        self.password_entry = PlainInput(master=self, label_text="Password:",
                                         input_placeholder="Enter your Password", )
        self.password_entry.grid(row=2, column=0, pady=(10, 0))

        # submit button
        self.submit_button = ctk.CTkButton(self, text="Login", width=150, height=30, command=self.login_handler)
        self.submit_button.grid(row=3, column=0, pady=(15, 0))

        # go to signup page button
        self.switch_to_sign_up = ctk.CTkButton(self, text="you don't have an account? Sign Up here!",
                                               fg_color='transparent', hover_color=self.cget('fg_color'),
                                               cursor='hand2', text_color='#78909C',
                                               command=self.switch_to_sign_up)
        self.switch_to_sign_up.grid(row=4, column=0, pady=(30, 0))

    def switch_to_sign_up(self):
        from modules.signUpForm import SignUpForm

        # destroy current page content
        self.destroy()

        # load sign up page contents
        SignUpForm(master=self.master).grid(column=0, row=0)

    def switch_to_otp_page(self):
        # destroy current page content
        self.destroy()

    def login_handler(self):
        from api_services.auth import login
        from modules.otpForm import OTPForm
        login_result = login(identifier=self.identifier_entry.input.get(), password=self.password_entry.input.get())

        if login_result and login_result['ok']:
            identifier = self.identifier_entry.input.get()
            password = self.password_entry.input.get()
            self.destroy()
            OTPForm(master=self.master, identifier=identifier, password=password).grid(column=0, row=0)
        else:
            CTkMessagebox(title='Error', message=login_result['message'], icon='cancel')
