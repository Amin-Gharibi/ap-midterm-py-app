import customtkinter as ctk
import tkinter as tk
from PIL import Image
import requests
from io import BytesIO
from os import getenv
from urllib.parse import urlparse


class ItemBox(tk.Frame):
    def __init__(self, master, target_fg_color, details_page, item, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.details_page = details_page
        self.item = item

        # Configure background color to separate the box from the background
        self.configure(bg=target_fg_color[1], border=10)

        # Display the cover image
        self.display_cover_image()

        # Title label
        title_text = self.get_title_text()
        title_label = ctk.CTkLabel(self, text=title_text, fg_color=target_fg_color[1], font=("Arial", 14))
        title_label.grid(row=2, column=0, padx=10, sticky="w")

        # Summary label
        summary_text, summary_label_height = self.get_summary_text()
        summary_label = ctk.CTkLabel(self, text=summary_text, fg_color=target_fg_color[1], font=("Arial", 12),
                                     text_color='gray', height=summary_label_height, anchor='w', justify='left')
        summary_label.grid(row=3, column=0, padx=15, sticky='w')

        # Rate label
        rate_label = ctk.CTkLabel(self, text=f"{self.item.get('movie', self.item.get('article', 'cast')).get('rate', 0)} {'⭐' * int(self.item.get('movie', self.item.get('article', 'cast')).get('rate', 0))}",
                                  fg_color=target_fg_color[1], font=("Arial", 12, 'italic'), text_color='yellow')
        rate_label.grid(row=4, column=0, padx=10, sticky="w")

        # More details button
        details_button = ctk.CTkButton(self, text="Details", font=("Arial", 12, 'bold'),
                                       command=self.on_details_click_handler)
        details_button.grid(row=5, column=0, padx=0, pady=(10, 0), sticky="ew")

    def display_cover_image(self):
        """Fetch and display the cover image based on the item type."""
        parsed_url = urlparse(getenv('BASE_URL'))
        item_type, cover_key = self.get_item_type_and_cover_key()

        if item_type and cover_key:
            image_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{item_type}/{cover_key}"
            res = requests.get(image_url)
            if res.status_code == 200:
                image = ctk.CTkImage(dark_image=Image.open(BytesIO(res.content)), size=(300, 150))
                image_label = ctk.CTkLabel(self, image=image, text="")
                image_label.grid(row=1, column=0, pady=(0, 15))

    def get_item_type_and_cover_key(self):
        """Determine the item type and corresponding cover key."""
        if 'movie' in self.item:
            return 'moviesPictures', self.item['movie']['cover']
        elif 'article' in self.item:
            return 'articlesCovers', self.item['article']['cover']
        elif 'cast' in self.item:
            return 'usersProfilePictures', self.item['cast']['profilePic']
        return None, None

    def get_title_text(self):
        """Extract the title text based on the item type."""
        if 'movie' in self.item:
            return self.item['movie']['fullName']
        elif 'article' in self.item:
            return self.item['article']['title']
        elif 'cast' in self.item:
            return self.item['cast']['fullName']
        return ''

    def get_summary_text(self):
        """Extract the summary or body text and its height."""
        if 'movie' in self.item and self.item['movie']['summary']:
            return self.item['movie']['summary'], 80
        elif 'article' in self.item and self.item['article']['body']:
            return self.item['article']['body'], 80
        elif 'biography' in self.item and self.item['cast']['biography']:
            return self.item['cast']['biography'], 80
        return '', 0

    def on_details_click_handler(self):
        """Handle the details button click by navigating to the details page."""
        for widget in self.master.master.master.winfo_children():
            widget.destroy()

        dt_page = self.details_page(self.master.master.master, self.item)
        dt_page.grid(row=0, column=0, sticky='nsew')
