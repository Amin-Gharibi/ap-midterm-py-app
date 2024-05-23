import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance


class ImageSlider(ctk.CTkFrame):
    def __init__(self, master, images_addresses: list, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.configure(fg_color=master.cget('fg_color'))

        self.images = [self.load_and_resize_image(image, (1000, 500)) for image in images_addresses]
        self.small_images = [self.load_and_resize_image(image, (100, 50), opacity=0.5) for image in images_addresses]
        self.image_index = 0

        # Convert images to a format suitable for Tkinter
        self.tk_images = [ImageTk.PhotoImage(image) for image in self.images]
        self.tk_small_images = [ImageTk.PhotoImage(image) for image in self.small_images]

        self.shown_image_label = ctk.CTkLabel(self, image=self.tk_images[self.image_index], text='')
        self.shown_image_label.grid(row=0, column=1, columnspan=3, sticky='ew')

        # Previous button
        self.prev_button = ctk.CTkButton(self, text="<", command=self.show_previous_image, width=50)
        self.prev_button.grid(row=0, column=0, padx=(0, 20))

        # Next button
        self.next_button = ctk.CTkButton(self, text=">", command=self.show_next_image, width=50)
        self.next_button.grid(row=0, column=5, padx=(20, 0))

        # Thumbnail images
        self.thumbnail_frame = ctk.CTkFrame(self)
        self.thumbnail_frame.grid(row=1, column=1, columnspan=3, sticky='ew', pady=(10, 0))
        self.thumbnail_labels = []

        for idx, img in enumerate(self.tk_small_images):
            lbl = ctk.CTkLabel(self.thumbnail_frame, image=img, text='')
            lbl.grid(row=0, column=idx, padx=5, pady=5)
            self.thumbnail_labels.append(lbl)

    def load_and_resize_image(self, image_path, size, opacity=1.0):
        image = Image.open(image_path).resize(size)
        if opacity < 1.0:
            image = self.adjust_opacity(image, opacity)
        return image

    def adjust_opacity(self, image, opacity):
        alpha = image.split()[3] if image.mode == 'RGBA' else Image.new('L', image.size, 255)
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image

    def show_previous_image(self):
        self.image_index = (self.image_index - 1) % len(self.tk_images)
        self.shown_image_label.configure(image=self.tk_images[self.image_index])

    def show_next_image(self):
        self.image_index = (self.image_index + 1) % len(self.tk_images)
        self.shown_image_label.configure(image=self.tk_images[self.image_index])
