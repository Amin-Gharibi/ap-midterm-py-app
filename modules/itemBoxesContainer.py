import customtkinter as ctk
from modules.itemBox import ItemBox
from modules.sectionTitle import SectionTitle
from math import floor


class ItemBoxesContainer(ctk.CTkFrame):
    def __init__(self, master, target_fg_color, title, items: list, details_page, container_bg_color=None, **kwargs):
        super().__init__(master, **kwargs)

        if container_bg_color is None:
            container_bg_color = master.cget('bg_color')

        # set containers fg color to be like the bg color of the scrollable frame, so user wouldn't feel any change
        # in the bg color
        self.configure(fg_color=container_bg_color)

        # set the title of the section
        self.section_title = SectionTitle(master=self, text=title)
        self.section_title.grid(row=0, column=0, padx=(30, 0), pady=(50, 0), sticky='w')

        # create boxes from the details passed to the class
        for item in enumerate(items):
            (ItemBox(master=self,
                     target_fg_color=target_fg_color,
                     details_page=details_page,
                     item=item[1])
             .grid(row=floor(item[0] / 4) + 1, column=(item[0] % 4), padx=(50, 0), pady=(50, 0)))

        if not len(items):
            self.grid_columnconfigure((0, 1), weight=1)
            ctk.CTkLabel(self, text='Nothing Found...', font=('Arial', 16, 'italic'), text_color='gray').grid(row=1, column=0, columnspan=2)
