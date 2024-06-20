import customtkinter as ctk
from modules.headerNavBar import HeaderNavBar
from modules.sectionTitle import SectionTitle
from modules.itemBox import ItemBox
from math import floor


class AllOneTypePage(ctk.CTkScrollableFrame):
    def __init__(self, master, get_all_items_func, get_all_items_param, search_func, page_title, items_details_page):
        super().__init__(master)

        self.search_func = search_func
        self.items_details_page = items_details_page
        self.all_items = get_all_items_func()[get_all_items_param]

        self.configure(fg_color=self.cget('bg_color'))
        self.grid_columnconfigure((0, 1), weight=1)

        # header navbar
        self.header = HeaderNavBar(self, parent_count=4)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        SectionTitle(self, text=page_title).grid(row=1, column=0, sticky="w", padx=10, pady=(30, 20))

        search_options_frame = ctk.CTkFrame(self, fg_color='transparent')
        search_options_frame.grid(row=1, column=1, sticky="e", padx=15, pady=(30, 20))

        self.search_filter = ctk.CTkComboBox(search_options_frame, values=['Latest Added', 'Top Rated', 'Low Rated'])
        self.search_filter.set('Latest Added')
        self.search_filter.grid(row=0, column=0)

        self.search_query = ctk.CTkEntry(search_options_frame, placeholder_text='Search...', width=150)
        self.search_query.grid(row=0, column=1, padx=10)

        ctk.CTkButton(search_options_frame, text='Go...', width=60, command=self.handle_searching).grid(row=0, column=2)

        self.items_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.items_frame.grid(row=2, column=0, columnspan=2, sticky='ew')

        self.load_items_to_frame()

    def load_items_to_frame(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        for index, item in enumerate(self.all_items):
            ItemBox(self.items_frame, target_fg_color=self.header.get_fg_color(), details_page=self.items_details_page,
                    item=item, base_frame_count=5).grid(row=floor(index / 4) + 1, column=(index % 4), padx=(50, 0),
                                                        pady=(50, 0), sticky='nsew')

        if not len(self.all_items):
            ctk.CTkLabel(self.items_frame, text='No Results Found...', font=('Arial', 16, 'italic'),
                         text_color='gray').pack(pady=50)

    def handle_searching(self):
        filter = None
        match self.search_filter.get():
            case 'Latest Added':
                filter = 'LATEST'
            case 'Top Rated':
                filter = 'TOPRATED'
            case 'Low Rated':
                filter = 'LOWRATED'

        self.all_items = self.search_func(q=self.search_query.get(), filter=filter)['result']
        self.load_items_to_frame()
