import customtkinter as ctk
from PIL import Image,ImageDraw
from tkinter import filedialog, messagebox
import requests,cv2
from io import BytesIO
from skimage import measure, filters,color
import numpy as np
from utils import create_styled_frame, create_styled_button, create_styled_label, create_styled_optionemenu, CustomTheme



class ImageProcessingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        CustomTheme.apply(self)
        self.configure(fg_color=CustomTheme.COLORS["bg_primary"])
        self.grid_columnconfigure(1, weight=1)  # Columna principal con peso 1
        self.grid_rowconfigure(0, weight=1)  # Fila principal con peso 1

        self.original_image = None
        self.processed_image = None
        self.segmented_image = None
        self.show_values = False

        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        sidebar = create_styled_frame(self)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0, rowspan=2)
        sidebar.grid_rowconfigure((8, 9), weight=1)
        sidebar.configure(fg_color=CustomTheme.COLORS["barra"], corner_radius=0)

        title = create_styled_label(
            sidebar,
            text="Image Analysis",
            font=CustomTheme.FONTS["title"],
            text_color=CustomTheme.COLORS["success"]
        )
        title.grid(row=0, column=0, pady=(20, 30), padx=20, sticky="ew")

        # Model selection
        model_label = create_styled_label(sidebar, text="Segmentation Model", font=CustomTheme.FONTS["subtitle"], text_color=CustomTheme.COLORS["text_light"])
        model_label.grid(row=1, column=0, pady=(0, 5), padx=20, sticky="w")
        
        self.model_var = ctk.StringVar(value="Modelos")
        model_menu = create_styled_optionemenu(sidebar, variable=self.model_var, values=["TFGWalid_EG1"])
        model_menu.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="ew")

        # Threshold slider
        threshold_label = create_styled_label(sidebar, text="Segmentation Threshold", font=CustomTheme.FONTS["subtitle"], text_color=CustomTheme.COLORS["text_light"])
        threshold_label.grid(row=3, column=0, pady=(0, 5), padx=20, sticky="w")
        
        self.threshold_var = ctk.DoubleVar(value=0.5)
        threshold_slider = ctk.CTkSlider(sidebar, from_=0, to=1, number_of_steps=100, variable=self.threshold_var)
        threshold_slider.grid(row=4, column=0, pady=(0, 20), padx=20, sticky="ew")

        load_button = create_styled_button(sidebar, text="Load Image", command=self.upload_image)
        load_button.grid(row=5, column=0, pady=(0, 10), padx=20, sticky="ew")

        process_button = create_styled_button(sidebar, text="Process Image", command=self.process_image)
        process_button.grid(row=6, column=0, pady=(0, 10), padx=20, sticky="ew")

        # Botón para descargar la imagen procesada
        self.download_button = create_styled_button(sidebar, text="Download Processed Image", command=self.download_processed_image, state="disabled")
        self.download_button.grid(row=7, column=0, pady=(0, 10), padx=20, sticky="ew")

        self.results_text = ctk.CTkTextbox(sidebar, height=150, width=250)
        self.results_text.grid(row=9, column=0, pady=(0, 20), padx=20, sticky="nsew")
        self.results_text.configure(font=CustomTheme.FONTS["default"], text_color=CustomTheme.COLORS["text_light"], fg_color=CustomTheme.COLORS["primary"])

        self.cell_count_label = ctk.CTkTextbox(sidebar, height=150, width=250)
        self.cell_count_label.grid(row=9, column=0, pady=(0, 20), padx=20, sticky="nsew")
        self.cell_count_label.configure(font=CustomTheme.FONTS["default"], text_color=CustomTheme.COLORS["text_light"], fg_color=CustomTheme.COLORS["primary"])

    def create_main_content(self):
        main_frame = create_styled_frame(self)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20, rowspan=2)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Fila de controles (Original, Processed, Values)
        controls_frame = create_styled_frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        controls_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.view_mode = ctk.StringVar(value="Original")
        self.original_radio = ctk.CTkRadioButton(controls_frame, text="Original", variable=self.view_mode, value="Original", command=self.show_original_image)
        self.original_radio.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.processed_radio = ctk.CTkRadioButton(controls_frame, text="Processed", variable=self.view_mode, value="Processed", command=self.show_processed_image)
        self.processed_radio.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.values_radio = ctk.CTkRadioButton(controls_frame, text="Values", variable=self.view_mode, value="Values", command=self.show_values_image)
        self.values_radio.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Panel de imágenes
        self.image_frame = create_styled_frame(main_frame)
        self.image_frame.grid(row=1, column=0, sticky="nsew")
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)

        # Etiqueta para mostrar la imagen (original, procesada o valores)
        self.image_label = ctk.CTkLabel(self.image_frame, text="", fg_color=CustomTheme.COLORS["bg_secondary"])
        self.image_label.grid(row=0, column=0, sticky="nsew")

        # Etiqueta para mostrar los valores de las células
        self.value_label = ctk.CTkLabel(self.image_frame, text="", fg_color=CustomTheme.COLORS["bg_secondary"])
        self.value_label.grid(row=1, column=0, sticky="nsew")

    def show_original_image(self):
        """Muestra la imagen original."""
        if self.original_image:
            self.display_highlighted_image(self.original_image)

    def show_processed_image(self):
        """Muestra la imagen procesada."""
        if self.processed_image:
            self.display_highlighted_image(self.processed_image)

    def show_values_image(self):
        """Muestra la imagen segmentada y habilita la visualización de valores."""
        if self.segmented_image:
            self.display_highlighted_image(self.segmented_image)
            self.image_label.bind("<Motion>", self.show_cell_value)

    def toggle_values(self):
        """Activa o desactiva la visualización de los valores y el resaltado de células."""
        if self.segmented_image:
            self.show_values = not self.show_values
            if self.show_values:
                self.image_label.bind("<Motion>", self.show_cell_value)
            else:
                self.image_label.unbind("<Motion>")
                self.value_label.configure(text="")
                self.display_highlighted_image(self.segmented_image)



    def show_cell_value(self, event):
        """Muestra el valor de la célula bajo el cursor y la resalta."""
        if self.segmented_image:
            x, y = event.x, event.y
            cell_value = self.get_cell_value(x, y)
            if cell_value is not None:
                self.value_label.configure(text=f"Value: {cell_value}")
                self.highlight_cell(x, y)  # Resaltar la célula
            else:
                self.value_label.configure(text="Background")
                self.display_highlighted_image(self.segmented_image)  # Restaurar la imagen original

    def get_cell_value(self, x, y):
        """Obtiene el valor de la célula en (x, y) con corrección de posición y escalado."""
        if not self.segmented_image:
            return None

        # Dimensiones del widget y de la imagen mostrada
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()
        img_width, img_height = self.segmented_image.size

        # Verificar si las dimensiones del widget son válidas
        if label_width <= 1 or label_height <= 1:
            return None

        # Calcular las proporciones de escalado utilizadas
        image_ratio = img_width / img_height
        label_ratio = label_width / label_height

        if image_ratio > label_ratio:
            # La imagen se ajusta en ancho
            scale_factor = img_width / label_width
            offset_y = (label_height - (img_height / scale_factor)) / 2
            offset_x = 0
        else:
            # La imagen se ajusta en altura
            scale_factor = img_height / label_height
            offset_x = (label_width - (img_width / scale_factor)) / 2
            offset_y = 0

        # Ajustar las coordenadas del cursor
        img_x = int((x - offset_x) * scale_factor)
        img_y = int((y - offset_y) * scale_factor)

        # Verificar si las coordenadas ajustadas están dentro de la imagen
        if img_x < 0 or img_x >= img_width or img_y < 0 or img_y >= img_height:
            return None

        # Obtener el valor del píxel
        return self.segmented_image.getpixel((img_x, img_y))


    def get_cell_value(self, x, y):
        """Obtiene el valor de la célula en la posición (x, y) del cursor, ajustando por escalado."""
        if not self.segmented_image:
            return None

        # Ajustar las coordenadas del cursor según la escala
        img_x = int(x * self.scale_x)
        img_y = int(y * self.scale_y)

        # Verificar si las coordenadas están dentro de la imagen
        img_width, img_height = self.segmented_image.size
        if 0 <= img_x < img_width and 0 <= img_y < img_height:
            pixel_value = self.segmented_image.getpixel((img_x, img_y))

            # Considerar un umbral para distinguir el fondo
            background_threshold = 10
            return pixel_value if pixel_value > background_threshold else None

        return None


    def highlight_cell(self, x, y):
        """Resalta la célula con el color original de la imagen."""
        if not self.segmented_image:
            return

        # Copiar la imagen segmentada
        highlighted_image = self.segmented_image.copy()
        img_array = np.array(highlighted_image)

        # Obtener el valor de la célula en las coordenadas proporcionadas
        cell_value = self.get_cell_value(x, y)
        
        if cell_value is None:  # Si es fondo, no hacer nada
            return

        # Resaltar la célula en el color original
        mask = np.all(img_array == cell_value, axis=-1)  # Mascaramos la célula por su color
        img_array[mask] = [0, 0, 255]  # Resaltamos la célula con color azul, por ejemplo

        # Convertir el array de nuevo a una imagen
        highlighted_image = Image.fromarray(img_array)

        # Redimensionar la imagen para ajustarse al espacio disponible en el label
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()

        # Redimensionar la imagen para ajustarse al tamaño del label
        highlighted_image = highlighted_image.resize((label_width, label_height), Image.LANCZOS)
        
        # Convertir la imagen a un objeto CTkImage para el widget
        ctk_image = ctk.CTkImage(highlighted_image, size=(label_width, label_height))
        
        # Mostrar la imagen resaltada en el label
        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image


    
    def display_highlighted_image(self, highlighted_image):
        """Muestra la imagen destacada en el image_label, ajustando su tamaño al espacio disponible."""
        # Redimensionar la imagen para que se ajuste al espacio disponible
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()

        if label_width > 1 and label_height > 1:  # Evitar divisiones por cero
            image_ratio = highlighted_image.width / highlighted_image.height
            label_ratio = label_width / label_height

            if image_ratio > label_ratio:
                new_width = label_width
                new_height = int(label_width / image_ratio)
            else:
                new_height = label_height
                new_width = int(label_height * image_ratio)

            # Guardar las escalas de redimensionamiento
            self.scale_x = highlighted_image.width / new_width
            self.scale_y = highlighted_image.height / new_height

            # Redimensionar la imagen
            resized_image = highlighted_image.resize((new_width, new_height), Image.LANCZOS)
            ctk_image = ctk.CTkImage(resized_image, size=(new_width, new_height))
            self.image_label.configure(image=ctk_image, text="")
            self.image_label.image = ctk_image


    def display_image(self, image):
        """Muestra una imagen en el image_label, ajustando su tamaño al espacio disponible."""
        # Redimensionar la imagen para que se ajuste al espacio disponible
        label_width = self.image_label.winfo_width()
        label_height = self.image_label.winfo_height()

        if label_width > 1 and label_height > 1:  # Evitar divisiones por cero
            image_ratio = image.width / image.height
            label_ratio = label_width / label_height

            if image_ratio > label_ratio:
                new_width = label_width
                new_height = int(label_width / image_ratio)
            else:
                new_height = label_height
                new_width = int(label_height * image_ratio)

            # Guardar las escalas de redimensionamiento
            self.scale_x = image.width / new_width
            self.scale_y = image.height / new_height

            # Redimensionar la imagen
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            ctk_image = ctk.CTkImage(resized_image, size=(new_width, new_height))
            self.image_label.configure(image=ctk_image, text="")
            self.image_label.image = ctk_image  # Evitar garbage collection

    def show_original_image(self):
        """Muestra la imagen original."""
        if hasattr(self, "original_image"):
            self.display_highlighted_image(self.original_image)

    def show_processed_image(self):
        """Muestra la imagen procesada."""
        if hasattr(self, "segmented_image"):
            self.display_highlighted_image(self.segmented_image)


    def upload_image(self):
        # Seleccionar archivo
        file_path = filedialog.askopenfilename(filetypes=[("Imagen TIFF", "*.tiff")])
        if not file_path:
            return

        # Cargar y mostrar la imagen original
        self.original_image = Image.open(file_path)
        # Mostrar un mensaje de éxito
        self.results_text.delete("1.0", ctk.END)
        self.results_text.insert(ctk.END, "Image loaded successfully.\n")
        #Mostrar la imagen
        self.display_highlighted_image(self.original_image)

        # Guardar la ruta del archivo para procesamiento
        self.file_path = file_path

    def process_image(self):
        if not hasattr(self, "file_path"):
            self.results_text.delete("1.0", ctk.END)
            self.results_text.insert(ctk.END, "Please load an image first.\n")
            return

        # Enviar imagen a la API
        response = self.send_to_api(self.file_path)
        if response is not None:
            # Mostrar resultados
            segmented_image_url = response["segmented_image_url"]
            cell_count = response["cell_count"]

            # Descargar la imagen segmentada desde la URL
            segmented_image = self.download_image(segmented_image_url)

            # Guardar y mostrar la imagen procesada
            if segmented_image:
                self.segmented_image = segmented_image
                self.display_highlighted_image(self.segmented_image)
                self.download_button.configure(state="normal")  # Habilitar el botón de descarga

            # Mostrar número de células
            self.cell_count_label.delete("1.0", ctk.END)
            self.cell_count_label.insert(ctk.END, f"Número de células: {cell_count}. \n")

    def download_processed_image(self):
        """Guarda la imagen procesada en el dispositivo del usuario."""
        if hasattr(self, "segmented_image"):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    self.segmented_image.save(file_path)
                    messagebox.showinfo("Success", "Processed image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "No processed image available to download.")



    def send_to_api(self, file_path):
        api_url = "https://8856-35-240-237-146.ngrok-free.app/predict"  # Cambia TU_NGROK_URL con tu URL de ngrok
        try:
            with open(file_path, "rb") as file:
                files = {"image": file}
                response = requests.post(api_url, files=files)
            if response.status_code == 200:
                return response.json()
            else:
                print("Error en la API:", response.text)
                return None
        except Exception as e:
            print(f"Error al enviar la imagen a la API: {e}")
            return None

    def download_image(self, url):
        """
        Descarga la imagen desde la URL y la devuelve como un objeto Image.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                return Image.open(image_data)
            else:
                print(f"Error al descargar la imagen: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error al descargar la imagen: {e}")
            return None