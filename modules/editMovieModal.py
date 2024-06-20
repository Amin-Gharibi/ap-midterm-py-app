import customtkinter as ctk
from modules.modalWindow import ModalWindow
from api_services.movies import get_movie_by_id
from modules.plainInput import PlainInput
from modules.sectionTitle import SectionTitle
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog


class EditMovieModal(ModalWindow):
    def __init__(self, master, movie_id):
        super().__init__(master, geometry='1100x600', title='Edit Movie')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.movie_id = movie_id
        self.movie = get_movie_by_id(self.movie_id)['targetMovie']

        container = ctk.CTkScrollableFrame(self)
        container.grid(row=0, column=0, sticky='nsew')

        add_new_movie_frame = ctk.CTkFrame(container, fg_color='transparent')
        add_new_movie_frame.grid_columnconfigure((0, 1, 2), weight=1)
        add_new_movie_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=20)

        SectionTitle(add_new_movie_frame, text='Edit Movie').grid(row=0, column=0, sticky='w', padx=30, pady=(0, 20))

        self.movie_name_entry = PlainInput(add_new_movie_frame, label_text='Movie Full Name:',
                                           input_placeholder="Enter Movie Name...", input_value=self.movie['fullName'])
        self.movie_name_entry.grid(row=1, column=0, padx=(45, 0))

        self.movie_genre_entry = PlainInput(add_new_movie_frame, label_text='Movie Genres(separated by space):',
                                            input_placeholder="Enter Movie Genres...",
                                            input_value=' '.join(self.movie['genre']))
        self.movie_genre_entry.grid(row=1, column=1, padx=20)

        self.movie_release_date_entry = PlainInput(add_new_movie_frame, label_text='Release Date:',
                                                   input_placeholder="Enter Movie Release Date...",
                                                   input_value=self.movie['releaseDate'])
        self.movie_release_date_entry.grid(row=1, column=2, padx=(0, 45))

        self.movie_language_entry = PlainInput(add_new_movie_frame, label_text='Movie Language:',
                                               input_placeholder="Enter Movie Languages...",
                                               input_value=self.movie['movieLanguage'])
        self.movie_language_entry.grid(row=2, column=0, pady=20, padx=(45, 0))

        self.movie_countries_entry = PlainInput(add_new_movie_frame, label_text='Movie Country:',
                                                input_placeholder='Enter Movie Countries...',
                                                input_value=self.movie['countries'])
        self.movie_countries_entry.grid(row=2, column=1, padx=20)

        self.movie_budget_entry = PlainInput(add_new_movie_frame, label_text='Movie Budget:',
                                             input_placeholder='Enter Movie Budget...',
                                             input_value=self.movie['budget'])
        self.movie_budget_entry.grid(row=2, column=2, padx=(0, 45))

        movie_summary_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_summary_frame.grid_columnconfigure(0, weight=1)
        movie_summary_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=45)
        ctk.CTkLabel(movie_summary_frame, text='Movie Summary:', text_color='gray', font=("Arial", 12, 'italic')).grid(
            row=0, column=0, sticky='w')
        self.movie_summary_entry = ctk.CTkTextbox(movie_summary_frame)
        self.movie_summary_entry.delete("1.0", ctk.END)
        self.movie_summary_entry.insert("1.0", self.movie['summary'])
        self.movie_summary_entry.grid(row=1, column=0, sticky='ew')

        self.movie_cover = None
        movie_cover_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_cover_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(movie_cover_frame, text='Movie Cover:', text_color='gray',
                     font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(movie_cover_frame, text='Add New Cover', command=self.select_movie_cover_handler).grid(row=1,
                                                                                                             column=0,
                                                                                                             sticky='w')
        self.movie_selected_cover_label = ctk.CTkLabel(movie_cover_frame,
                                                       text="Select New Movie Cover (Don't Select If Don't Want To Change)")
        self.movie_selected_cover_label.grid(row=0, column=1, padx=20)

        self.movie_medias = []
        movie_medias_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_medias_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=45, pady=20)
        ctk.CTkLabel(movie_medias_frame, text='Movie Medias:', text_color='gray', font=("Arial", 12, "italic")).grid(
            row=0, column=0, sticky='w')
        ctk.CTkButton(movie_medias_frame, text='Add New Media', command=self.select_movie_medias_handler).grid(row=1,
                                                                                                               column=0,
                                                                                                               sticky='w')
        self.selected_movie_medias_count_label = ctk.CTkLabel(movie_medias_frame,
                                                              text=f"Select Movie Medias (Don't Select If Don't Want To Change)")
        self.selected_movie_medias_count_label.grid(row=0, column=1, padx=20)

        self.movie_casts = []
        self.movie_casts_table = None
        self.movie_casts_not_found_label = None
        movie_cast_frame = ctk.CTkFrame(add_new_movie_frame, fg_color='transparent')
        movie_cast_frame.grid_columnconfigure((0, 1, 2), weight=1)
        movie_cast_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=45)
        ctk.CTkLabel(movie_cast_frame, text='Movie Cast:', text_color='gray', font=('Arial', 14, 'italic')).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky='w')
        self.search_cast_name_entry = PlainInput(movie_cast_frame, label_text='Name - In-Movie-Name - In-Movie-Role:',
                                                 input_placeholder='Enter Cast Name...')
        self.search_cast_name_entry.grid(row=1, column=0, sticky='nw')
        ctk.CTkButton(movie_cast_frame, text='Search', command=self.search_cast_handler).grid(row=1, column=0,
                                                                                              sticky='w')

        self.cast_results_var = []
        self.cast_results_check_buttons = []
        ctk.CTkLabel(movie_cast_frame, text='Search Results:', text_color='gray', font=('Arial', 10, 'italic')).grid(
            row=0, column=1)
        self.cast_result_box = ctk.CTkScrollableFrame(movie_cast_frame, width=200, height=200,
                                                      fg_color=['#F9F9FA', 'gray23'])
        self.cast_result_box.grid(row=1, column=1, sticky='nsew', padx=50)
        self.cast_result_box.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(movie_cast_frame, text='Selected Cast:', text_color='gray', font=('Arial', 10, 'italic')).grid(
            row=0, column=2)
        self.cast_selected_box = ctk.CTkScrollableFrame(movie_cast_frame, width=200, height=200,
                                                        fg_color=['#F9F9FA', 'gray23'])
        self.cast_selected_box.grid_columnconfigure(0, weight=1)
        self.cast_selected_box.grid(row=1, column=2, sticky='nsew')

        ctk.CTkButton(container, text='Save', command=self.handle_editing_movie).grid(row=1, column=0, columnspan=3,
                                                                                      pady=20)
        self.cast_results_check_buttons = []
        self.cast_selected_check_buttons = []

        self.updating_cast = []
        self.duplicate_updating_cast = []
        for cast in self.movie['cast']:
            self.updating_cast.append({"castId": cast['cast']['_id'],
                                       "inMovieRole": cast['inMovieRole'],
                                       "inMovieName": cast['inMovieName']})
            self.duplicate_updating_cast.append({"fullName": cast['cast']['fullName'],
                                                 "inMovieRole": cast['inMovieRole']})

        self.update_movie_selected_cast_box()

    def select_movie_cover_handler(self):
        self.movie_cover = filedialog.askopenfilename()
        self.movie_cover = self.movie_cover if self.movie_cover else None
        if self.movie_cover is not None:
            self.movie_selected_cover_label.configure(text="Movie Cover Selected!")

    def select_movie_medias_handler(self):
        self.movie_medias = filedialog.askopenfilenames()
        self.movie_medias = self.movie_medias if self.movie_medias else None
        if self.movie_medias is not None:
            self.selected_movie_medias_count_label.configure(text="Movie Medias Selected!")

    def search_cast_handler(self):
        from api_services.cast import search_cast
        cast_search_result = search_cast(self.search_cast_name_entry.input.get().split(' - ')[0])
        if cast_search_result['ok']:
            self.update_searched_casts_table(cast_search_result['result'])
        else:
            CTkMessagebox(title='Error', message=cast_search_result['message'], icon='cancel')

    def handle_editing_movie(self):
        from api_services.movies import update_movie

        update_result = update_movie(movie_id=self.movie_id,
                                     fullName=self.movie_name_entry.input.get(),
                                     summary=self.movie_summary_entry.get("1.0", ctk.END),
                                     genre=self.movie_genre_entry.input.get(),
                                     releaseDate=self.movie_release_date_entry.input.get(),
                                     countries=self.movie_countries_entry.input.get(),
                                     language=self.movie_language_entry.input.get(),
                                     budget=self.movie_budget_entry.input.get(),
                                     cover=self.movie_cover,
                                     medias=self.movie_medias,
                                     cast=self.updating_cast)

        if update_result['ok']:
            CTkMessagebox(title='Success', message='Movie Edited Successfully!', icon='check')
            super().on_close()
            self.master.update_all_movies_table()
        else:
            CTkMessagebox(title='Error', message=update_result['message'], icon='cancel')

    def update_searched_casts_table(self, data):
        for check_button in self.cast_results_check_buttons:
            check_button.grid_forget()
        self.cast_results_var = []
        self.cast_results_check_buttons = []

        for index, item in enumerate(data):
            var = ctk.BooleanVar()
            check_button = ctk.CTkCheckBox(self.cast_result_box, text=f"{item['fullName']}", variable=var, width=160,
                                           command=lambda idx=index: self.handle_adding_cast(adding_index=idx, data=data))
            check_button.grid(row=index, column=0, sticky='w', padx=20, pady=10)
            self.cast_results_check_buttons.append(check_button)

        if not len(data):
            label = ctk.CTkLabel(self.cast_result_box, text="No results found")
            label.grid(row=0, column=0, sticky='ew')
            self.cast_results_check_buttons.append(label)

    def handle_adding_cast(self, adding_index, data):
        self.updating_cast.append({
            "castId": data[adding_index]['_id'],
            "inMovieName": self.search_cast_name_entry.input.get().split(" - ")[1],
            "inMovieRole": self.search_cast_name_entry.input.get().split(" - ")[2]
        })
        self.duplicate_updating_cast.append({
            "fullName": data[adding_index]['fullName'],
            "inMovieRole": self.search_cast_name_entry.input.get().split(" - ")[2]
        })
        self.update_movie_selected_cast_box()

    def update_movie_selected_cast_box(self):
        for widget in self.cast_selected_check_buttons:
            widget.grid_forget()
        self.cast_selected_check_buttons = []

        for index, item in enumerate(self.duplicate_updating_cast):
            var = ctk.BooleanVar()
            var.set(True)
            check_button = ctk.CTkCheckBox(self.cast_selected_box,
                                           text=f"{item['fullName']} - {item['inMovieRole']}", variable=var,
                                           width=160,
                                           command=lambda idx=index: self.handle_deleting_cast(deleting_index=idx))
            check_button.grid(row=index, column=0, sticky='w', padx=20, pady=10)
            self.cast_selected_check_buttons.append(check_button)
        if not len(self.duplicate_updating_cast):
            label = ctk.CTkLabel(self.cast_result_box, text="No cast found")
            label.grid(row=0, column=0, sticky='ew')
            self.cast_selected_check_buttons.append(label)

    def handle_deleting_cast(self, deleting_index):
        del self.updating_cast[deleting_index]
        del self.duplicate_updating_cast[deleting_index]
        self.update_movie_selected_cast_box()
