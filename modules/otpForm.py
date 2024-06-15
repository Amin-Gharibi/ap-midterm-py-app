import customtkinter as ctk
from modules.plainInput import PlainInput
import tkinter as tk
from CTkMessagebox import CTkMessagebox


class OTPForm(ctk.CTkFrame):
    def __init__(self, master, identifier=None, username=None, email=None, password=None, fullName=None, role=None,
                 operation=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.identifier = identifier
        self.username = username
        self.email = email
        self.password = password
        self.fullName = fullName
        self.role = role
        self.operation = operation

        self.configure(fg_color=master.cget("bg"))

        # page title
        self.middle_page_title = ctk.CTkLabel(self, text="OTP Verification ", font=("Arial", 36, 'italic'))
        self.middle_page_title.grid(row=0, column=0)

        ctk.CTkLabel(self, text="OTP code was sent to your Email Address...", font=("Arial", 12, 'italic'),
                     text_color='gray').grid(row=1, column=0)

        # otp code field entry input
        self.otp_code_entry = PlainInput(master=self, label_text="OTP:",
                                         input_placeholder="Enter OTP code sent to your Email...", )
        self.otp_code_entry.grid(row=2, column=0, pady=(20, 0))

        self.minute = tk.StringVar()
        self.second = tk.StringVar()
        self.interval = 180

        self.minute.set("03")
        self.second.set("00")

        self.interval_label = ctk.CTkLabel(self, text=f"Resend OTP in {self.minute.get()}:{self.second.get()}",
                                           font=('Arial', 12, 'bold'), text_color='gray')
        self.interval_label.grid(row=3, column=0, sticky='e', pady=(10, 0))

        # submit button
        self.submit_button = ctk.CTkButton(self, text="Confirm", width=150, height=30, command=self.operation_handler)
        self.submit_button.grid(row=4, column=0, pady=(15, 0))

        # go to log in first step page button
        self.switch_to_login_first_step = ctk.CTkButton(self, text="You entered wrong info? Click To Go Back!",
                                                        fg_color='transparent', hover_color=self.cget('fg_color'),
                                                        cursor='hand2', text_color='#78909C',
                                                        command=self.switch_to_login_first_step_handler)
        self.switch_to_login_first_step.grid(row=5, column=0, pady=(30, 0))

        self.update_timer()

    def update_timer(self):
        mins, secs = divmod(self.interval, 60)
        self.minute.set(f"{mins:02d}")
        self.second.set(f"{secs:02d}")

        self.interval_label.configure(text=f"Resend OTP in {self.minute.get()}:{self.second.get()}")

        if self.interval > 0:
            self.interval -= 1
            self.after(1000, self.update_timer)
        else:
            self.interval_label.destroy()
            self.interval_label = ctk.CTkButton(self, text="Resend Otp", fg_color='transparent', text_color='gray',
                                                anchor='e', cursor='hand2',
                                                hover_color=self.cget('fg_color'), width=50,
                                                font=('Arial', 12, 'bold'), command=self.resend_otp_handler)
            self.interval_label.grid(row=3, column=0, sticky='e', pady=(10, 0))

    def switch_to_login_first_step_handler(self):
        if self.operation == 'login':
            from modules.loginForm import LoginForm

            self.destroy()

            LoginForm(self.master).grid(row=0, column=0)
        elif self.operation == 'signup':
            from modules.signUpForm import SignUpForm

            self.destroy()

            SignUpForm(self.master).grid(row=0, column=0)

    def operation_handler(self):
        login_result = None
        signup_result = None

        if self.operation == 'login':
            from api_services.auth import validate_login_otp

            login_result = validate_login_otp(identifier=self.identifier, password=self.password,
                                              code=self.otp_code_entry.input.get())

        elif self.operation == 'signup':
            from api_services.auth import validate_register_otp

            signup_result = validate_register_otp(fullName=self.fullName, email=self.email, username=self.username,
                                                  password=self.password, role=self.role,
                                                  code=self.otp_code_entry.input.get())

        if login_result and login_result['ok']:
            from api_services.auth import get_me
            user = get_me()['user']
            self.destroy()
            if user and user['role'] == 'ADMIN':
                from modules.adminDashboard import AdminDashboard
                AdminDashboard(master=self.master).grid(row=0, column=0, sticky='nsew')
            else:
                from modules.userDashboard import UserDashboard
                UserDashboard(master=self.master).grid(row=0, column=0, sticky='nsew')
        elif signup_result and signup_result['ok']:
            msg = CTkMessagebox(
                title='Success',
                message="Congratulations! You have successfully signed up, now you have to wait until admin approves your account. You are gonna be norified using email whenever you get approved!",
                icon='check')

            if msg.get().lower() == 'ok':
                from mainScrollableFrame import MainScrollableFrame
                MainScrollableFrame(master=self.master).grid(row=0, column=0, sticky='nsew')

        else:
            CTkMessagebox(title='Error', message=(login_result and login_result['message']) or (signup_result and signup_result['message']) or 'Something Went Wrong!', icon='cancel')

    def resend_otp_handler(self):
        if self.operation == 'login':
            from api_services.auth import login

            login_result = login(identifier=self.identifier, password=self.password)
            if login_result and login_result['ok']:
                self.minute.set("03")
                self.second.set("00")
                self.interval = 180
                self.after(1000, self.update_timer)
            else:
                CTkMessagebox(title='Error', message="Error Occurred While Sending OTP Code! Please Try Again...",
                              icon='cancel')

        elif self.operation == 'signup':
            from api_services.auth import register

            signup_result = register(fullName=self.fullName, email=self.email, username=self.username,
                                     password=self.password, role=self.role)
            if signup_result and signup_result['ok']:
                self.minute.set("03")
                self.second.set("00")
                self.interval = 180
                self.after(1000, self.update_timer)
            else:
                CTkMessagebox(title='Error', message="Error Occurred While Sending OTP Code! Please Try Again...",
                              icon='cancel')
