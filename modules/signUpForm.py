import customtkinter as ctk
from modules.plainInput import PlainInput
from CTkMessagebox import CTkMessagebox


class SignUpForm(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=master.cget("bg"))

        # page title
        self.middle_page_title = ctk.CTkLabel(self, text="SIGN UP ", font=("Arial", 36, 'italic'))
        self.middle_page_title.grid(row=0, column=0)

        # full name field entry input
        self.full_name_entry = PlainInput(master=self, label_text="Full Name:",
                                          input_placeholder="Enter your first name and last name", )
        self.full_name_entry.grid(row=1, column=0, pady=(40, 0))

        # email field entry input
        self.email_entry = PlainInput(master=self, label_text="Email:",
                                      input_placeholder="Enter your Email", )
        self.email_entry.grid(row=2, column=0, pady=(10, 0))

        # username field entry input
        self.username_entry = PlainInput(master=self, label_text="Username:",
                                         input_placeholder="Enter your Username", )
        self.username_entry.grid(row=3, column=0, pady=(10, 0))

        # password field entry input
        self.password_entry = PlainInput(master=self, label_text="Password:",
                                         input_placeholder="Enter your Password", )
        self.password_entry.grid(row=4, column=0, pady=(10, 0))

        # role field entry input
        role_input_label = ctk.CTkLabel(self, text='Role:', text_color='gray', font=("Arial", 12, 'italic'))
        role_input_label.grid(row=5, column=0, pady=(10, 0), sticky='w')
        self.role_entry = ctk.CTkOptionMenu(self, values=["Choose The Role You Are Interested In...", "User", "Critic"])
        self.role_entry.grid(row=6, column=0, sticky='ew')

        # submit button
        self.submit_button = ctk.CTkButton(self, text="Sign Up", width=150, height=30, command=self.sign_up_handler)
        self.submit_button.grid(row=7, column=0, pady=(20, 0))

        # go to login page button
        self.switch_to_login = ctk.CTkButton(self, text="Already have an account? Login here!",
                                             fg_color='transparent', hover_color=self.cget('fg_color'),
                                             cursor='hand2', text_color='#78909C',
                                             command=self.switch_to_login_handler)
        self.switch_to_login.grid(row=8, column=0, pady=(30, 0))

    def switch_to_login_handler(self):
        from modules.loginForm import LoginForm

        # destroy current page content
        self.destroy()

        # load login page contents
        login_form = LoginForm(master=self.master)
        login_form.grid(column=0, row=0)

    def sign_up_handler(self):
        from api_services.auth import register
        from modules.otpForm import OTPForm
        sign_up_result = register(fullName=self.full_name_entry.input.get(),
                                  email=self.email_entry.input.get(),
                                  username=self.username_entry.input.get(),
                                  password=self.password_entry.input.get(),
                                  role=self.role_entry.get().upper()
                                  )

        if sign_up_result and sign_up_result['ok']:
            fullName = self.full_name_entry.input.get()
            email = self.email_entry.input.get()
            username = self.username_entry.input.get()
            password = self.password_entry.input.get()
            role = self.role_entry.get().upper()
            self.destroy()
            OTPForm(master=self.master, fullName=fullName, email=email, username=username, password=password,
                    role=role, operation='signup').grid(column=0, row=0)
        else:
            CTkMessagebox(title='Error', message=sign_up_result['message'], icon='cancel')
