![Banner](https://github.com/flooki10/TFG/blob/main/banner.png)


# 📊 Segmentación automática de células en imágenes FISH
_Proyecto de investigación y análisis de imágenes biomédicas_

---

## 🌟 **Resumen**
> Con el fin de mejorar el diagnóstico de oligodendroglioma, se desarrolló un modelo de segmentación de células basado en aprendizaje automático mediante fine-tuning y entrenamiento supervisado. Este enfoque permite no solo contar de manera precisa el número de células en imágenes, sino también diferenciar entre células adyacentes a través de segmentación de instancia, abordando un desafío habitual en el análisis manual. Actualmente, este proceso se realiza de forma manual por los profesionales de salud, utilizando tinción nuclear e imágenes de hibridación in situ.

Para hacer más accesible esta solución tecnológica y simplificar el trabajo de los profesionales de la salud, se diseñó una aplicación de escritorio de segmentación de células a partir de imágenes FISH. Posteriormente, el modelo entrenado fue integrado en Google Colab a esta aplicación mediante una API, optimizando el flujo de trabajo en el entorno de laboratorio.

---

## 🎯 **Objetivos**
- [ ] Implementar un modelo eficiente para segmentación de células en imágenes FISH 3D.
- [ ] Contar automáticamente el número de células segmentadas.
- [ ] Analizar fluorescencias de color verde y rojo para cada célula.

---

## ⚙️ **Tecnologías y Herramientas**
- **Lenguaje:** Python
- **Framework:** PyTorch
- **Modelo:** MEDIAR para segmentación de imágenes
- **Backend:** Flask
- **Base de datos:** MongoDB
- **Frontend:** React

---

## 📁 **Estructura del Proyecto**
```bash
project-root/
├── src/
│   ├── data_processing.py   # Procesamiento de datos
│   ├── model_training.py    # Entrenamiento del modelo
│   ├── inference.py         # Segmentación de imágenes
│   └── visualization.py     # Visualización de resultados
├── models/                  # Pesos del modelo entrenado
├── README.md                # Este archivo
└── requirements.txt         # Dependencias del proyecto

In order to improve the diagnosis of oligodendroglioma, a cell segmentation model was developed based on machine learning through fine-tuning and supervised training. This approach not only allows for the precise counting of cells in images but also differentiates between adjacent cells using instance segmentation, addressing a common challenge in manual analysis. Currently, this process is performed manually by healthcare professionals using nuclear staining and in situ hybridization images.

To make this technological solution more accessible and simplify the work of healthcare professionals, a desktop application for cell segmentation from FISH images was designed. Subsequently, the trained model was integrated from Google Colab into this application via an API, optimizing the workflow in the laboratory environment.

![Plan General](https://github.com/flooki10/TFG/blob/main/planificaci%C3%B3n_TFG.png)

## Acceder al fichero estudio_calidad.ipynb en la carpeta estudio_calidad para más detalles sobre los resultados
![Resultados](https://github.com/flooki10/TFG/blob/main/superposici%C3%B3n_original_segmentada.png)
