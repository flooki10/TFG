#paso 2
model_path1 = "/content/drive/MyDrive/ejecucion_local/from_phase1.pth"
model_path2 = "/content/drive/MyDrive/ejecucion_local/from_phase2.pth"

import torch
weights1 = torch.load(model_path1, map_location="cpu")
weights2 = torch.load(model_path2, map_location="cpu")

#paso 3
# Definir ruta de tu modelo
model_path = "/content/drive/MyDrive/ejecucion_local/TFGWalid_EG1.pth"

import sys
sys.path.append("/content/drive/MyDrive/ejecucion_local/custom/")  # Añade la ruta /content/ al PATH de Python

# Ahora puedes importar custom directamente
from custom import *
import torch
from MEDIARFormer import *
from predictor import *
from utils import compute_masks
from BasePredictor import BasePredictor
from transforms import *

# Definir los parámetros del modelo según tu configuración
model_args = {
    "classes": 3,
    "decoder_channels": [1024, 512, 256, 128, 64],
    "decoder_pab_channels": 256,
    "encoder_name": 'mit_b5',
    "in_channels": 3
}

# Crear una instancia del modelo
model = MEDIARFormer(**model_args)

# Cargar los pesos del modelo desde la ruta proporcionada
weights = torch.load(model_path, map_location="cpu")
model.load_state_dict(weights, strict=False)

# Definir ruta de imágenes de entrada
input_path = "/content/drive/MyDrive/ejecucion_local/img/"  # Ruta de las imágenes

# Definir ruta de salida para las predicciones
output_path = "/content/drive/MyDrive/ejecucion_local/img"

# Usar el predictor para hacer la predicción
predictor = Predictor(model, "cuda:0", input_path, output_path, algo_params={"use_tta": False})
_ = predictor.conduct_prediction()

