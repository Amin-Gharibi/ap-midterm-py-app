import customtkinter as ctk
import tkinter as tk
from PIL import Image


class ItemBox(tk.Frame):
    def __init__(self, id, cover, title, description, rate, target_fg_color, details_page, **kwargs):
        super().__init__(**kwargs)

        self.details_page = details_page
        self.id = id

        # configure bg color, so it would change and user feel the box is separate from the background,
        # like the header navbar
        self.configure(bg=target_fg_color[1], border=10)

        # cover image
        image = ctk.CTkImage(dark_image=Image.open(cover), size=(200, 150))
        image_label = ctk.CTkLabel(self, image=image, text="")
        image_label.grid(row=1, column=0, pady=(0, 15))

        # title label
        title_label = ctk.CTkLabel(self, text=title, fg_color=target_fg_color[1], font=("Arial", 14))
        title_label.grid(row=2, column=0, padx=10, sticky="w")

        # artists item box doesn't have a description, so its height must be 0
        if len(description):
            description_label_height = 80
        else:
            description_label_height = 0

        # description label
        description_label = ctk.CTkLabel(self, text=description, fg_color=target_fg_color[1], font=("Arial", 12), text_color='gray', height=description_label_height)
        description_label.grid(row=3, column=0, padx=15, sticky='w')

        # rate label
        rate_label = ctk.CTkLabel(self, text=f"{rate} {'⭐' * int(rate)}", fg_color=target_fg_color[1], font=("Arial", 12, 'italic'), text_color='yellow')
        rate_label.grid(row=4, column=0, padx=10, sticky="w")

        # more details button
        details_button = ctk.CTkButton(self, text="Details", font=("Arial", 12, 'bold'), command=self.on_details_click_handler)
        details_button.grid(row=5, column=0, padx=0, pady=(10, 0), sticky="ew")

    def on_details_click_handler(self):
        for widget in self.master.master.master.winfo_children():
            widget.destroy()

        dt_page = self.details_page(master=self.master.master.master, movie={
                "id": 0,
                "title": "After Life",
                "description": "This movie is so amazing and i would definitely suggest you to watch this super amazing movie. seriously i mean it hatman nagash konid",
                "cover": "images/imdb_logo.png",
                "rate": 5
            })

        dt_page.grid(row=0, column=0, sticky='nsew')
