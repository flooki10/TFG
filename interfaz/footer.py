import customtkinter as ctk
from utils import create_styled_frame, create_styled_label, create_styled_button, CustomTheme
from PIL import Image, ImageTk
import time

class Footer(ctk.CTkFrame):
    def __init__(self, parent, add_new_patient):
        super().__init__(parent)
        self.add_new_patient = add_new_patient
        self.create_footer_content()

    def create_footer_content(self):
        self.configure(height=80, fg_color=CustomTheme.COLORS["primary"], corner_radius=0)
        self.grid_columnconfigure(1, weight=1)

        # Crear y agregar el botón "Add Patient" a la izquierda
        add_icon = self.create_colored_icon("C:/Users/walid/OneDrive/Desktop/interfaz/img/database.png")
        add_button = self.create_icon_button(add_icon, self.add_new_patient)
        add_button.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Crear el reloj en tiempo real a la derecha
        self.clock_label = create_styled_label(
            self, 
            text="", 
            font=("Roboto", 14),
            text_color=CustomTheme.COLORS["text_primary"]
        )
        self.clock_label.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        # Iniciar la actualización del reloj
        self.update_clock()

    def create_colored_icon(self, path, size=(30,30)):
        original = Image.open(path).resize(size, Image.LANCZOS)
        colored = Image.new("RGBA", original.size, CustomTheme.COLORS["icon_color"])
        colored.putalpha(original.getchannel('A'))
        return ImageTk.PhotoImage(colored)

    def create_icon_button(self, icon, command):
        button = create_styled_button(self, text="", image=icon, command=command, width=60, height=60)
        button.configure(fg_color=CustomTheme.COLORS["icon_bg"], hover_color=CustomTheme.COLORS["secondary"])
        return button

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.configure(text=current_time)
        self.after(1000, self.update_clock)  # Actualizar cada segundo

