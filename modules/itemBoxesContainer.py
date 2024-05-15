import customtkinter as ctk
from modules.itemBox import ItemBox
from modules.sectionTitle import SectionTitle
from math import floor


class ItemBoxesContainer(ctk.CTkFrame):
    def __init__(self, master, target_fg_color, title, items: list, **kwargs):
        super().__init__(master, **kwargs)

        # set containers fg color to be like the bg color of the scrollable frame, so user wouldn't feel any change
        # in the bg color
        self.configure(fg_color=master.cget('bg_color'))

        # set the title of the section
        latest_movies_title = SectionTitle(master=self, text=title)
        latest_movies_title.grid(row=0, column=0, padx=(30, 0), pady=(50, 0), sticky='w')

        # create boxes from the details passed to the class
        for item in enumerate(items):
            items_box = ItemBox(master=self, cover=item[1]['cover'], title=item[1]['title'], description=item[1]['description'],
                                rate=item[1]['rate'], target_fg_color=target_fg_color)
            items_box.grid(row=floor(item[0] / 4) + 1, column=(item[0] % 4), padx=(50, 0), pady=(50, 0))
