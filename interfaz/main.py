import customtkinter as ctk
from image_processing_page import ImageProcessingPage
from header import Header
from footer import Footer
from utils import set_appearance_mode, CustomTheme

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clostr - Advanced Medical Image Processing")
        self.geometry("1200x800")

        set_appearance_mode("light")
        CustomTheme.apply(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((0, 2), weight=0) # Update 1

        self.create_header()
        self.create_main_page()
        self.create_footer()

    def create_header(self):
        self.header = Header(self)
        self.header.grid(row=0, column=0, sticky="ew")

    def create_main_page(self):
        self.main_page = ImageProcessingPage(self)
        self.main_page.grid(row=1, column=0, sticky="nsew", columnspan=2) # Update 2

    def create_footer(self):
        self.footer = Footer(self, self.add_new_image)
        self.footer.grid(row=2, column=0, sticky="ew", columnspan=2) # Update 3

    def add_new_image(self):
        self.main_page.load_image()

if __name__ == "__main__":
    app = App()
    app.mainloop()

