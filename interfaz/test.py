import requests
from PIL import Image
import io

# Cargar una imagen de prueba en formato RGB
imagen = Image.open("C:/Users/walid/OneDrive/Desktop/interfaz/img/cell_00007.jpg")

# Convertir la imagen a escala de grises
imagen_gris = imagen.convert("L")

# Convertir la imagen a bytes en formato TIFF
image_bytes = io.BytesIO()
imagen_gris.save(image_bytes, format="TIFF")
image_bytes.seek(0)

# Enviar la imagen a la API
url = "https://13fd-35-197-141-118.ngrok-free.app/segmentar"  # Reemplaza con la nueva URL de ngrok
response = requests.post(url, files={'imagen': image_bytes})

# Verificar la respuesta
if response.status_code == 200:
    data = response.json()
    print("Células detectadas:", data["cell_count"])
else:
    print("Error:", response.text)