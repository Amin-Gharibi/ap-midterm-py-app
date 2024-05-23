import tkinter
import customtkinter as ctk


class SearchBox(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # config foreground color
        self.configure(fg_color='transparent')

        # config grid template
        self.grid_columnconfigure(0, weight=1)

        # frame title
        frame_label = ctk.CTkLabel(self, text="Find Your Favorite Movie Or Actor Instantly!", text_color='yellow',
                                   font=('Arial', 36, 'bold'))
        frame_label.grid(row=0, column=0)

        search_entry_frame = ctk.CTkFrame(self, fg_color='transparent')
        search_entry_frame.grid_columnconfigure(0, weight=1)
        search_entry_frame.grid_columnconfigure(1, weight=1)

        # frame search entry
        self.search_entry = ctk.CTkEntry(search_entry_frame, placeholder_text='Search here...', font=('Arial', 16),
                                         width=400, height=35, justify=tkinter.CENTER)
        self.search_entry.grid(row=1, column=0)

        # search button
        self.search_button = ctk.CTkButton(search_entry_frame, text='Find...', width=100, height=36,
                                           command=self.search_handler)
        self.search_button.grid(row=1, column=1, padx=(5, 0))

        # place the frame
        search_entry_frame.grid(row=1, column=0, pady=(20, 0))

    def search_handler(self):
        from modules.searchResultsPage import SearchResultsPage

        # saved the value of the entry in another var because I am destroying all the widgets and after that
        # I can not access the value
        value = self.search_entry.get()

        for widget in self.master.master.winfo_children():
            widget.destroy()

        SearchResultsPage(self.master.master, value).grid(row=0, column=0, sticky='nsew')
