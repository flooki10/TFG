#home_icon = CTkImage(Image.open("C:/Users/walid/OneDrive/Desktop/interfaz/img/home.png"), size=(20, 20))
#database_icon = CTkImage(Image.open("C:/Users/walid/OneDrive/Desktop/interfaz/img/database.png"), size=(20, 20))


import customtkinter as ctk
from utils import create_styled_frame, create_styled_button, create_styled_label, CustomTheme
from PIL import Image, ImageTk

class Header(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.create_header_content()

    def create_header_content(self):
        self.configure(height=80, fg_color=CustomTheme.COLORS["primary"])
        self.grid_columnconfigure(1, weight=1)

        # Load icon
        home_icon = self.create_colored_icon("C:/Users/walid/OneDrive/Desktop/interfaz/img/home.png")

        # Create home button with icon
        home_button = self.create_icon_button(home_icon, lambda: None)  # No action needed as we only have one page
        home_button.grid(row=0, column=0, padx=20, pady=10)

        # Add a title to the header
        title_label = create_styled_label(self, text="Clostr", font=("Arial", 24, "bold"), text_color=CustomTheme.COLORS["text_primary"])
        title_label.grid(row=0, column=1, padx=20, pady=10, sticky="e")

    def create_colored_icon(self, path, size=(30, 30)):
        original = Image.open(path).resize(size, Image.LANCZOS)
        colored = Image.new("RGBA", original.size, CustomTheme.COLORS["icon_color"])
        colored.putalpha(original.getchannel('A'))
        return ImageTk.PhotoImage(colored)

    def create_icon_button(self, icon, command):
        button = create_styled_button(self, text="", image=icon, command=command, width=60, height=60)
        button.configure(fg_color=CustomTheme.COLORS["icon_bg"], hover_color=CustomTheme.COLORS["secondary"])
        return button

