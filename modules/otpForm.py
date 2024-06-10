import customtkinter as ctk
from modules.plainInput import PlainInput
import tkinter as tk
from CTkMessagebox import CTkMessagebox


class OTPForm(ctk.CTkFrame):
    def __init__(self, master, identifier, password, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.identifier = identifier
        self.password = password

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
        self.submit_button = ctk.CTkButton(self, text="Login", width=150, height=30, command=self.login_handler)
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
        from modules.loginForm import LoginForm

        self.destroy()

        LoginForm(self.master).grid(row=0, column=0)

    def login_handler(self):
        from api_services.auth import validate_login_otp

        login_result = validate_login_otp(identifier=self.identifier, password=self.password,
                                          code=self.otp_code_entry.input.get())

        if login_result and login_result['ok']:
            from api_services.auth import get_me

            user = get_me()
            user = user and user['user']

            self.destroy()

            if user['role'] == 'ADMIN':
                from modules.adminDashboard import AdminDashboard

                AdminDashboard(master=self.master).grid(row=0, column=0, sticky='nsew')
            else:
                from modules.userDashboard import UserDashboard

                UserDashboard(master=self.master).grid(row=0, column=0, sticky='nsew')
        else:
            CTkMessagebox(title='Error', message=login_result['message'], icon='cancel')

    def resend_otp_handler(self):
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
