import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from menu import Menu
class App(ctk.CTk):
    def __init__(self):
        # Setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo Editor')
        self.minsize(800,500)
        self.init_parameters()

        # Layout
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 2, uniform = 'a')
        self.columnconfigure(1, weight = 6, uniform = 'a')

        # Canvas Data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # Widgets
        self.image_import = ImageImport(self, self.import_image)

        # ImportButton (Frame with a button)
        ImageImport(self, self.import_image)

        # Run
        self.mainloop()
    def init_parameters(self):
        self.pos_vars = {
                'rotate': ctk.DoubleVar(value = ROTATE_DEFAULT),
                'zoom' : ctk.DoubleVar(value = ZOOM_DEFAULT),
                'flip': ctk.StringVar(value = FLIP_OPTIONS[0])
        }

        self.color_vars = {
            'Brightness': ctk.DoubleVar(value = BRIGHTNESS_DEFAULT),
            'Grayscale': ctk.DoubleVar(value = GRAYSCALE_DEFAULT),
            'Invert': ctk.BooleanVar(value = INVERT_DEFAULT),
            'Vibrance': ctk.DoubleVar(value = VIBRANCE_DEFAULT)
        }

        self.effect_vars = {
            'Blur': ctk.DoubleVar(value = BLUR_DEFAULT),
            'Contrast': ctk.IntVar(value = CONTRAST_DEFAULT),
            'Effect': ctk.StringVar(value = EFFECT_OPTIONS[0])
        }

        # Tracing
        combined_vars = list(self.pos_vars.values()) + list(self.color_vars.values()) + list(self.effect_vars.values())
        for var in combined_vars:
            var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original

        # Rotate Logic
        if self.pos_vars['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_vars['rotate'].get())

        # Zoom Logic
        if self.pos_vars['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(image = self.image, border = self.pos_vars['zoom'].get())

        # Flip Logic
        if self.pos_vars['flip'].get() != FLIP_OPTIONS[0]:
            if self.pos_vars['flip'].get() == 'X':
                self.image = ImageOps.mirror(self.image)
            if self.pos_vars['flip'].get() == 'Y':
                self.image = ImageOps.flip(self.image)
            if self.pos_vars['flip'].get() == 'Both':
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        # Brightness & Vibrance Logic
        if self.color_vars['Brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enchancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enchancer.enhance(self.color_vars['Brightness'].get())
        if self.color_vars['Vibrance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_vars['Vibrance'].get())

        # Grayscale and Invert of the Colors Logic
        if self.color_vars['Grayscale'].get():
            self.image = ImageOps.grayscale(self.image)
        if self.color_vars['Invert'].get():
            self.image = ImageOps.invert(self.image)

        # Blur and Contrast Logic
        if self.effect_vars['Blur'].get() != BLUR_DEFAULT:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['Blur'].get()))
        if self.effect_vars['Contrast'].get() != CONTRAST_DEFAULT:
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['Contrast'].get()))

        effect = self.effect_vars['Effect'].get()
#        match self.effect_vars['Effect'].get():
        if effect == 'Emboss':
            self.image = self.image.filter(ImageFilter.EMBOSS)
        elif effect == 'Find Edges':
            self.image = self.image.filter(ImageFilter.FIND_EDGES)
        elif effect == 'Contour':
            self.image = self.image.filter(ImageFilter.CONTOUR)
        elif effect == 'Edge Enhance':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)

        self.place_image()
    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget() # Closing the import button
        self.image_output = ImageOutput(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit)
        self.menu = Menu(self, self.pos_vars, self.color_vars, self.effect_vars)
    def close_edit(self):
        # Hide the image and the close button
        self.image_output.grid_forget()
        self.image_output.place_forget()
        self.menu.grid_forget()
        # Recreate the import button
        self.image_import = ImageImport(self, self.import_image)
    def resize_image(self, event):
        # Current Canvas Ratio
        canvas_ratio = event.width / event.height

        # Update Canvas Attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # Resize Image
        if canvas_ratio > self.image_ratio: # Canvas is wider than the image
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else: # Canvas is taller than the image
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()
    def place_image(self):
        self.image_output.delete('all') # Fixes the image duplication when resizing the window
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image = self.image_tk)

App()
