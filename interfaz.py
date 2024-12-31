import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pymongo

# Configuración de MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["PatientDatabase"]
collection = db["PatientRecords"]

# Configuración de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MultiPageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Plataforma de Análisis de Imágenes")
        self.geometry("1200x800")  # Tamaño inicial más grande

        # Contenedor principal para las páginas
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)  # Permite expansión vertical
        self.container.grid_columnconfigure(0, weight=1)  # Permite expansión horizontal

        self.frames = {}
        for Page in (PatientDataPage, ImageAnalysisPage, DatabasePage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PatientDataPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class PatientDataPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configurar la cuadrícula del marco
        self.grid_rowconfigure((0, 13), weight=1)  # Peso para margen superior e inferior
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=0)  # Campos
        self.grid_columnconfigure((0, 2), weight=1)  # Márgenes izquierdo y derecho
        self.grid_columnconfigure(1, weight=3)  # Columna central (campos de entrada)

        # Título
        ctk.CTkLabel(self, text="Datos del Paciente", font=("Arial", 24)).grid(
            row=0, column=0, columnspan=3, pady=20
        )

        # Campos de entrada
        self.create_input("Número de Historia Clínica:", 1)
        self.create_input("Nombre:", 2)
        self.create_input("Apellidos:", 3)
        self.create_input("Fecha de Nacimiento (YYYY-MM-DD):", 4)
        self.create_option_menu("Sexo:", ["Masculino", "Femenino", "Otro"], 5)
        self.create_input("Diagnóstico Clínico Inicial:", 6)
        self.create_input("Fecha del Diagnóstico (YYYY-MM-DD):", 7)
        self.create_input("Código de la Muestra:", 8)
        self.create_input("Fecha de Toma de Muestra (YYYY-MM-DD):", 9)
        self.create_input("Centro Médico:", 10)
        self.create_input("Médico Responsable:", 11)
        self.create_input("Observaciones Clínicas:", 12)

        # Botón
        ctk.CTkButton(self, text="Guardar y Continuar", command=self.save_data).grid(
            row=13, column=1, pady=20
        )

    def create_input(self, placeholder, row):
        """Crea un campo de entrada con un label."""
        label = ctk.CTkLabel(self, text=placeholder)
        label.grid(row=row, column=0, sticky="e", padx=10, pady=5)
        entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        return entry

    def create_option_menu(self, placeholder, options, row):
        """Crea un menú desplegable con un label."""
        label = ctk.CTkLabel(self, text=placeholder)
        label.grid(row=row, column=0, sticky="e", padx=10, pady=5)
        menu = ctk.CTkOptionMenu(self, values=options)
        menu.grid(row=row, column=1, sticky="ew", padx=10, pady=5)
        return menu

    def save_data(self):
        # Recopilar los datos ingresados
        patient_data = {
            "patient_id": self.id_entry.get(),
            "name": self.name_entry.get(),
            "last_name": self.last_name_entry.get(),
            "dob": self.dob_entry.get(),
            "sex": self.sex_entry.get(),
            "diagnosis": self.diagnosis_entry.get(),
            "diagnosis_date": self.diagnosis_date_entry.get(),
            "sample_code": self.sample_code_entry.get(),
            "sample_date": self.sample_date_entry.get(),
            "center": self.center_entry.get(),
            "doctor": self.doctor_entry.get(),
            "notes": self.notes_entry.get()
        }

        # Validar campos obligatorios
        required_fields = ["patient_id", "name", "last_name", "dob", "sex", "diagnosis", "diagnosis_date", "sample_code", "sample_date", "center", "doctor"]
        for field in required_fields:
            if not patient_data[field]:
                messagebox.showerror("Error", f"Por favor, completa el campo: {field.replace('_', ' ').capitalize()}.")
                return

        # Guardar en MongoDB
        try:
            collection.insert_one(patient_data)
            messagebox.showinfo("Éxito", "Datos del paciente guardados correctamente.")

            # Ir a la página de análisis de imágenes
            self.controller.show_frame("ImageAnalysisPage")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {str(e)}")


class ImageAnalysisPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Título
        ctk.CTkLabel(self, text="Análisis de la Imagen", font=("Arial", 24)).pack(pady=20)

        # Botón para cargar imagen
        self.image_label = ctk.CTkLabel(self, text="No se ha cargado ninguna imagen.")
        self.image_label.pack(pady=10)

        ctk.CTkButton(self, text="Cargar Imagen", command=self.load_image).pack(pady=10)

        # Botón para procesar imagen
        ctk.CTkButton(self, text="Procesar Imagen", command=self.process_image).pack(pady=10)

        # Campo para observaciones
        self.observations_entry = ctk.CTkTextbox(self, height=100)
        self.observations_entry.pack(pady=10, fill="x", padx=20)
        
        # Botón para guardar y continuar
        ctk.CTkButton(self, text="Guardar y Continuar", command=self.save_and_continue).pack(pady=20)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.tiff")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.image_label.configure(image=self.image_tk, text="")

    def process_image(self):
        if hasattr(self, 'image'):
            # Aquí va la lógica de segmentación con tu modelo.
            messagebox.showinfo("Procesamiento", "La imagen ha sido segmentada.")
        else:
            messagebox.showerror("Error", "Por favor, carga una imagen primero.")

    def save_and_continue(self):
        observations = self.observations_entry.get("1.0", "end").strip()
        if not hasattr(self, 'image'):
            messagebox.showerror("Error", "Por favor, carga y procesa una imagen antes de continuar.")
            return

        # Guardar imagen y observaciones en MongoDB
        collection.update_one({}, {"$set": {"observations": observations}}, upsert=True)
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")

        # Ir a la página de base de datos
        self.controller.show_frame("DatabasePage")

class DatabasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Título
        ctk.CTkLabel(self, text="Base de Datos", font=("Arial", 24)).pack(pady=20)

        # Botón para volver al inicio
        ctk.CTkButton(self, text="Volver al Inicio", command=lambda: controller.show_frame("PatientDataPage")).pack(pady=10)

if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()
