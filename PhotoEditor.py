import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
    
        # setup
        super()._init_()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo Editor')
        
        # run
        self.mainloop()

App()
