import customtkinter as ctk


class PlainInput(ctk.CTkFrame):
    def __init__(self, master, label_text, input_placeholder, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=master.cget("fg_color"))

        # input label placement
        input_label = ctk.CTkLabel(self, text=label_text, text_color='gray', font=("Arial", 12, 'italic'))
        input_label.grid(row=0, column=0, sticky='w')

        # input placement
        input_entry = ctk.CTkEntry(self, placeholder_text=input_placeholder, width=300, height=40)
        input_entry.grid(row=1, column=0, sticky='ew')
