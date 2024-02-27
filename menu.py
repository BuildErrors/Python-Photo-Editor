import customtkinter as ctk
from panels import *

class Menu(ctk.CTkTabview):
    def __init__(self, parent, pos_vars, color_vars, effect_vars):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew', pady = 10, padx = 10)

        # Tabs
        self.add('Position')
        self.add('Color')
        self.add('Effects')
        self.add('Export')

        # Widgets
        PositionFrame(self.tab('Position'), pos_vars)
        ColorFrame(self.tab('Color'), color_vars)
        EffectsFrame(self.tab('Effects'), effect_vars)
        ExportFrame(self.tab('Export'))

class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, pos_vars):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        SliderPanel(self, 'Rotation', pos_vars['rotate'], 0, 360)
        SliderPanel(self, 'Zoom', pos_vars['zoom'], 0, 200)
        SegmentedPanel(self, 'Invert', pos_vars['flip'], FLIP_OPTIONS)
        RevertButton(self,
                     (pos_vars['rotate'], ROTATE_DEFAULT),
                     (pos_vars['zoom'], ZOOM_DEFAULT),
                     (pos_vars['flip'], FLIP_OPTIONS[0]),
                     )

class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_vars):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        SwitchPanel(self, (color_vars['Grayscale'], 'B/W'), (color_vars['Invert'], 'Invert'))
        SliderPanel(self, 'Brightness', color_vars['Brightness'], 0, 5)
        SliderPanel(self, 'Vibrance', color_vars['Vibrance'], 0, 5)
        RevertButton(self,
                     (color_vars['Brightness'], BRIGHTNESS_DEFAULT),
                     (color_vars['Grayscale'], GRAYSCALE_DEFAULT),
                     (color_vars['Invert'], INVERT_DEFAULT),
                     (color_vars['Vibrance'], VIBRANCE_DEFAULT)
                     )
class EffectsFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_vars):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

        DropDownPanel(self, effect_vars['Effect'], EFFECT_OPTIONS)
        SliderPanel(self, 'Blur', effect_vars['Blur'], 0, 3)
        SliderPanel(self, 'Contrast', effect_vars['Contrast'], 0, 10)
        RevertButton(self,
                     (effect_vars['Blur'], BLUR_DEFAULT),
                     (effect_vars['Contrast'], CONTRAST_DEFAULT),
                     (effect_vars['Effect'], EFFECT_OPTIONS[0])
                     )
class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = 'transparent')
        self.pack(expand = True, fill = 'both')

