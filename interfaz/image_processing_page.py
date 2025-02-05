import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
import requests
from io import BytesIO
from skimage import measure, morphology
import numpy as np
import plotly.graph_objects as go
from utils import create_styled_frame, create_styled_button, create_styled_label, create_styled_optionemenu, CustomTheme

def hex_to_rgba(hex_color, alpha=0.2):
    """Convierte un color hexadecimal a formato RGBA con opacidad alpha."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

class ImageProcessingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        CustomTheme.apply(self)
        self.configure(fg_color=CustomTheme.COLORS["bg_primary"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Imágenes y análisis
        self.original_image = None
        self.segmented_image = None
        self.analysis_image = None  # Imagen de análisis generada por Plotly (tamaño de referencia)
        self.labels = None          # Matriz de etiquetas obtenida de la imagen segmentada
        self.regions = {}           # Propiedades de cada célula
        
        # Tamaño objetivo para la visualización en modo nativo
        self.target_size = None   # (width, height) a usar para todas las imágenes
        
        # Variables para conversión de coordenadas en el display
        self.scale_x = self.scale_y = 1.0
        self.displayed_image_size = (0, 0)
        self.image_offset = (0, 0)
        
        # Variables para el tooltip flotante
        self.current_highlighted_label = None  
        self.base_image = None      # Imagen usada en modo "Values"
        self.resized_display_image = None
        
        self.tooltip_window = None

        self.create_sidebar()
        self.create_main_content()

    # Nueva función para crear el Label del contador de células alineado a la esquina superior izquierda
    def _create_countlabel(self, parent):
        label = ctk.CTkLabel(
            parent, 
            text="Número de células: 0", 
            font=CustomTheme.FONTS["default"],
            text_color="white", 
            fg_color=CustomTheme.COLORS["primary"],
            anchor="nw"  # Alineación superior izquierda
        )
        return label

    # Función para los otros cuadros (resultados)
    def _create_textbox(self, parent):
        t = ctk.CTkTextbox(parent, height=100, width=250)
        t.configure(
            font=CustomTheme.FONTS["default"], 
            text_color=CustomTheme.COLORS["text_light"],
            fg_color=CustomTheme.COLORS["primary"]
        )
        return t

    def create_sidebar(self):
        sidebar = create_styled_frame(self)
        sidebar.grid(row=0, column=0, sticky="nsew", rowspan=12)
        # Configurar filas para una distribución compacta
        for i in range(12):
            sidebar.grid_rowconfigure(i, weight=0)
        sidebar.grid_rowconfigure(10, weight=1)
        sidebar.grid_rowconfigure(11, weight=1)
        sidebar.configure(fg_color=CustomTheme.COLORS["barra"], corner_radius=0)
        
        # Título
        create_styled_label(
            sidebar, 
            text="Image Analysis", 
            font=CustomTheme.FONTS["title"],
            text_color=CustomTheme.COLORS["success"]
        ).grid(row=0, column=0, pady=(20,10), padx=20, sticky="ew")
        
        # Modelo y umbral
        create_styled_label(
            sidebar, 
            text="Segmentation Model", 
            font=CustomTheme.FONTS["subtitle"],
            text_color=CustomTheme.COLORS["text_light"]
        ).grid(row=1, column=0, pady=(0,5), padx=20, sticky="w")
        self.model_var = ctk.StringVar(value="Modelos")
        create_styled_optionemenu(
            sidebar, 
            variable=self.model_var, 
            values=["TFGWalid_EG1"]
        ).grid(row=2, column=0, pady=(0,10), padx=20, sticky="ew")
        create_styled_label(
            sidebar, 
            text="Segmentation Threshold", 
            font=CustomTheme.FONTS["subtitle"],
            text_color=CustomTheme.COLORS["text_light"]
        ).grid(row=3, column=0, pady=(0,5), padx=20, sticky="w")
        self.threshold_var = ctk.DoubleVar(value=0.5)
        ctk.CTkSlider(
            sidebar, 
            from_=0, 
            to=1, 
            number_of_steps=100, 
            variable=self.threshold_var
        ).grid(row=4, column=0, pady=(0,10), padx=20, sticky="ew")
        
        # Botones de carga y proceso
        create_styled_button(
            sidebar, 
            text="Load Image", 
            command=self.upload_image
        ).grid(row=5, column=0, pady=(10,5), padx=20, sticky="ew")
        create_styled_button(
            sidebar, 
            text="Process Image", 
            command=self.process_image
        ).grid(row=6, column=0, pady=(5,5), padx=20, sticky="ew")
        create_styled_button(
            sidebar, 
            text="Show Analysis", 
            command=self.show_analysis
        ).grid(row=7, column=0, pady=(5,5), padx=20, sticky="ew")
        
        # Botones de descarga
        create_styled_button(
            sidebar, 
            text="Download Processed Image", 
            command=self.download_processed_image
        ).grid(row=8, column=0, pady=(5,5), padx=20, sticky="ew")
        create_styled_button(
            sidebar, 
            text="Download Analysis Image", 
            command=self.download_analysis_image
        ).grid(row=9, column=0, pady=(5,5), padx=20, sticky="ew")
        
        # Cuadros de resultados y contador
        self.results_text = self._create_textbox(sidebar)
        self.results_text.grid(row=10, column=0, pady=(5,5), padx=20, sticky="nsew")
        self.cell_count_label = self._create_countlabel(sidebar)
        self.cell_count_label.grid(row=11, column=0, pady=(5,20), padx=20, sticky="nsew")

    def create_main_content(self):
        main_frame = create_styled_frame(self)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20, rowspan=12)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        controls_frame = create_styled_frame(main_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        controls_frame.grid_columnconfigure((0,1,2), weight=1)
        self.view_mode = ctk.StringVar(value="Original")
        for i, (txt, val, cmd) in enumerate([
            ("Original", "Original", self.show_original_image),
            ("Processed", "Processed", self.show_processed_image),
            ("Values", "Values", self.show_values_image)
        ]):
            ctk.CTkRadioButton(
                controls_frame, 
                text=txt, 
                variable=self.view_mode, 
                value=val, 
                command=cmd
            ).grid(row=0, column=i, padx=10, pady=10, sticky="w")
        self.display_frame = create_styled_frame(main_frame)
        self.display_frame.grid(row=1, column=0, sticky="nsew")
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.image_label = ctk.CTkLabel(
            self.display_frame, 
            text="", 
            fg_color=CustomTheme.COLORS["bg_secondary"]
        )
        self.image_label.grid(row=0, column=0, sticky="nsew")
        # Se usará una ventana flotante para el tooltip

    # ------------------ Métodos de Visualización ------------------
    def _update_image_label(self, img, w, h):
        im = ctk.CTkImage(img, size=(w, h))
        self.image_label.configure(image=im, text="")
        self.image_label.image = im

    def display_image(self, img, use_native_size=False):
        """
        Si use_native_size es True se muestra la imagen usando el tamaño objetivo (self.target_size)
        si ya se definió; de lo contrario, se usa el tamaño nativo de la imagen.
        Esto garantiza que todas las imágenes se visualicen con las mismas dimensiones.
        """
        if use_native_size:
            if self.target_size is not None:
                new_w, new_h = self.target_size
            else:
                new_w, new_h = img.width, img.height
            offset_x, offset_y = 0, 0
        else:
            lw, lh = self.image_label.winfo_width(), self.image_label.winfo_height()
            if lw <= 1 or lh <= 1:
                return
            image_aspect = img.width / img.height
            label_aspect = lw / lh
            if image_aspect > label_aspect:
                new_w = lw
                new_h = int(lw / image_aspect)
                offset_x = 0
                offset_y = (lh - new_h) // 2
            else:
                new_h = lh
                new_w = int(lh * image_aspect)
                offset_y = 0
                offset_x = (lw - new_w) // 2
        self.scale_x = img.width / new_w
        self.scale_y = img.height / new_h
        self.displayed_image_size = (new_w, new_h)
        self.image_offset = (offset_x, offset_y)
        resized_img = img.resize((new_w, new_h), Image.LANCZOS)
        self.resized_display_image = resized_img
        self._update_image_label(resized_img, new_w, new_h)

    def show_original_image(self):
        if self.original_image:
            self.display_image(self.original_image, use_native_size=True)
            self.image_label.unbind("<Motion>")
            self.hide_tooltip()

    def show_processed_image(self):
        if self.segmented_image:
            self.display_image(self.segmented_image, use_native_size=True)
            self.image_label.unbind("<Motion>")
            self.hide_tooltip()

    def show_values_image(self):
        self.base_image = self.analysis_image if self.analysis_image else self.segmented_image
        if self.base_image:
            self.display_image(self.base_image, use_native_size=True)
            self.current_highlighted_label = None
            self.image_label.bind("<Motion>", self.show_cell_value)

    # ------------------ Método de Análisis ------------------
    def show_analysis(self):
        if self.original_image is None or self.segmented_image is None:
            return messagebox.showerror("Error", "Please load and process an image first.")
        try:
            # Convertir la imagen original a escala de grises
            img_gray = np.array(self.original_image.convert('L'))
            # Usar la imagen segmentada para obtener los labels (se asume que es etiquetada)
            labels = np.array(self.segmented_image.convert('I'))
            self.labels = labels

            # Extraer propiedades de cada región
            self.regions = {}
            for prop in measure.regionprops(labels, img_gray):
                self.regions[prop.label] = {
                    'area': prop.area,
                    'eccentricity': prop.eccentricity,
                    'perimeter': prop.perimeter,
                    'intensity_mean': prop.intensity_mean
                }

            # Paleta de colores para contornos
            colors = [
                "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
                "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
                "#A3A500", "#00A08A", "#FFB500", "#6A4C93"
            ]

            # Obtener dimensiones de la imagen original
            w_orig, h_orig = self.original_image.size
            print(f"Original dimensions: width={w_orig}, height={h_orig}")

            # Crear figura usando traza Heatmap sin márgenes
            fig = go.Figure(data=go.Heatmap(
                z=img_gray,
                colorscale='gray',
                showscale=False,
                zmin=0,
                zmax=255
            ))
            fig.update_layout(
                autosize=False,
                width=w_orig,
                height=h_orig,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            fig.update_xaxes(visible=False, showgrid=False, zeroline=False, range=[0, w_orig], constrain='domain')
            fig.update_yaxes(visible=False, showgrid=False, zeroline=False, range=[0, h_orig],
                             autorange="reversed", constrain='domain', scaleanchor="x", scaleratio=1)

            # Agregar contornos para cada región con relleno transparente y borde visible
            for i, prop in enumerate(measure.regionprops(labels, img_gray)):
                cnts = measure.find_contours(labels == prop.label, 0.5)
                if cnts:
                    y, x = cnts[0].T
                    hoverinfo = ''.join(
                        f'<b>{p}: {getattr(prop, p):.2f}</b><br>'
                        for p in ['area', 'eccentricity', 'perimeter', 'intensity_mean']
                    )
                    color = colors[i % len(colors)]
                    fill_color = hex_to_rgba(color, alpha=0.2)
                    fig.add_trace(go.Scatter(
                        x=x,
                        y=y,
                        mode='lines',
                        fill='toself',
                        line=dict(color=color),
                        fillcolor=fill_color,
                        showlegend=False,
                        hovertemplate=hoverinfo,
                        hoveron='points+fills'
                    ))
            # Exportar la figura a imagen EXACTAMENTE con dimensiones originales
            img_bytes = fig.to_image(format="png", width=w_orig, height=h_orig, scale=1)
            analysis_img = Image.open(BytesIO(img_bytes))
            print(f"Analysis image dimensions (exported): width={analysis_img.width}, height={analysis_img.height}")
            if analysis_img.width != w_orig:
                new_img = Image.new("RGB", (w_orig, h_orig), "white")
                offset_x = (w_orig - analysis_img.width) // 2
                new_img.paste(analysis_img, (offset_x, 0))
                analysis_img = new_img
                print("Adjusted analysis image width.")
            print(f"Final analysis image dimensions: width={analysis_img.width}, height={analysis_img.height}")
            self.analysis_image = analysis_img
            self.target_size = (analysis_img.width, analysis_img.height)

            # Actualizar el label del contador de células
            self.cell_count_label.configure(text=f"Número de células: {len(self.regions)}")

            if self.view_mode.get() == "Values":
                self.show_values_image()

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error during analysis: {e}")

    # ------------------ Métodos para el Tooltip ------------------
    def show_tooltip(self, text, x, y):
        self.hide_tooltip()
        self.tooltip_window = ctk.CTkToplevel(self)
        self.tooltip_window.overrideredirect(True)
        self.tooltip_window.configure(bg="white")
        label = ctk.CTkLabel(self.tooltip_window, text=text, fg_color="white", text_color="black", font=CustomTheme.FONTS["default"])
        label.pack(padx=5, pady=5)
        self.tooltip_window.geometry(f"+{x+10}+{y+10}")

    def hide_tooltip(self):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def get_cell_label(self, x, y):
        # En modo nativo se usa self.target_size para conversión sin offsets
        new_w, new_h = self.target_size if self.target_size is not None else (self.segmented_image.width, self.segmented_image.height)
        scale_x = self.segmented_image.width / new_w
        scale_y = self.segmented_image.height / new_h
        image_x = int(x * scale_x)
        image_y = int(y * scale_y)
        if image_x < 0 or image_x >= self.segmented_image.width or image_y < 0 or image_y >= self.segmented_image.height:
            return None
        return self.labels[image_y, image_x]

    def show_cell_value(self, event):
        label = self.get_cell_label(event.x, event.y)
        if label == self.current_highlighted_label:
            return
        self.current_highlighted_label = label
        if label and label in self.regions:
            props = self.regions[label]
            tooltip_text = f"Cell {label}:\n" + "\n".join([f"{k}: {v:.2f}" for k, v in props.items()])
            self.show_tooltip(tooltip_text, event.x_root, event.y_root)
        else:
            self.hide_tooltip()

    # ------------------ Métodos de Carga y Procesado de Imagen ------------------
    def upload_image(self):
        fp = filedialog.askopenfilename(filetypes=[("Imagen TIFF", "*.tiff")])
        if not fp:
            return
        self.original_image = Image.open(fp)
        self.results_text.delete("1.0", ctk.END)
        self.results_text.insert(ctk.END, "Image loaded successfully.\n")
        self.display_image(self.original_image, use_native_size=True)
        self.file_path = fp

    def process_image(self):
        if not hasattr(self, "file_path"):
            self.results_text.delete("1.0", ctk.END)
            self.results_text.insert(ctk.END, "Please load an image first.\n")
            return
        resp = self.send_to_api(self.file_path)
        if resp:
            seg_url, cnt = resp["segmented_image_url"], resp["cell_count"]
            seg = self.download_image(seg_url)
            if seg:
                self.segmented_image = seg
                self.display_image(self.segmented_image, use_native_size=True)
                self.download_button.configure(state="normal")
            self.cell_count_label.configure(text=f"Número de células: {cnt}")
            
    def download_processed_image(self):
        if hasattr(self, "segmented_image"):
            fp = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if fp:
                try:
                    self.segmented_image.save(fp)
                    messagebox.showinfo("Success", "Processed image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {e}")
        else:
            messagebox.showwarning("Warning", "No processed image available to download.")

    def download_analysis_image(self):
        if self.analysis_image is not None:
            fp = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if fp:
                try:
                    self.analysis_image.save(fp)
                    messagebox.showinfo("Success", "Analysis image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save analysis image: {e}")
        else:
            messagebox.showwarning("Warning", "No analysis image available to download.")

    def send_to_api(self, fp):
        url = "https://8093-34-126-118-125.ngrok-free.app/predict"
        try:
            with open(fp, "rb") as f:
                r = requests.post(url, files={"image": f})
            return r.json() if r.status_code == 200 else (print("API Error:", r.text) or None)
        except Exception as e:
            print(f"API Error: {e}")
            return None

    def download_image(self, url):
        try:
            r = requests.get(url)
            return Image.open(BytesIO(r.content)) if r.status_code == 200 else (print(f"Download error: {r.status_code}") or None)
        except Exception as e:
            print(f"Download error: {e}")
            return None

    def on_leave(self, event):
        self.hide_tooltip()
        self.current_highlighted_label = None

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Image Processing App")
    app = ImageProcessingPage(root)
    app.pack(expand=True, fill="both")
    app.image_label.bind("<Leave>", app.on_leave)
    root.mainloop()
