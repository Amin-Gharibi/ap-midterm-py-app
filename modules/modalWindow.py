import customtkinter as ctk


class ModalWindow(ctk.CTkToplevel):
    def __init__(self, master, geometry, title):
        super().__init__(master)

        self.master = master

        self.geometry(geometry)
        self.title(title)
        self.resizable(False, False)

        self.grab_set()

        # close current modal window and enable master window
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.grab_release()
        self.destroy()
