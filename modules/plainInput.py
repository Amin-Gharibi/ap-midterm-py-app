import customtkinter as ctk


class PlainInput(ctk.CTkFrame):
    def __init__(self, master, label_text, input_placeholder, input_value='', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=master.cget("fg_color"))

        # input label placement
        input_label = ctk.CTkLabel(self, text=label_text, text_color='gray', font=("Arial", 12, 'italic'))
        input_label.grid(row=0, column=0, sticky='w')

        # input placement
        self.input = ctk.CTkEntry(self, placeholder_text=input_placeholder, width=300, height=40)
        self.input.grid(row=1, column=0, sticky='ew')

        if input_value:
            self.set_value(input_value)

    def set_value(self, value):
        self.input.delete(0, ctk.END)
        self.input.insert(0, value)
