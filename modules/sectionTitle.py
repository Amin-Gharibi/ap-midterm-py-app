import customtkinter as ctk


class SectionTitle(ctk.CTkLabel):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, **kwargs)

        # create custom label for each section title
        self.title = ctk.CTkLabel(self, text=f"· {text}", font=("Arial", 20, "italic"))
        self.title.grid(row=0, column=0)
