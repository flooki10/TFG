![Banner](https://github.com/flooki10/TFG/blob/main/banner.png)


# Segmentación automática de células en imágenes FISH
_Proyecto de investigación y análisis de imágenes biomédicas_

---

## 1. **Resumen**
> Con el fin de mejorar el diagnóstico de oligodendroglioma, se desarrolló un modelo de segmentación de células basado en aprendizaje automático mediante fine-tuning y entrenamiento supervisado. Este enfoque permite no solo contar de manera precisa el número de células en imágenes, sino también diferenciar entre células adyacentes a través de segmentación de instancia, abordando un desafío habitual en el análisis manual. Actualmente, este proceso se realiza de forma manual por los profesionales de salud, utilizando tinción nuclear e imágenes de hibridación in situ.

Para hacer más accesible esta solución tecnológica y simplificar el trabajo de los profesionales de la salud, se diseñó una aplicación de escritorio de segmentación de células a partir de imágenes FISH. Posteriormente, el modelo entrenado fue integrado en Google Colab a esta aplicación mediante una API, optimizando el flujo de trabajo en el entorno de laboratorio.

### Superposición de la imagen segmentada sobre la imagen Groudtruth original

![Alt img](https://github.com/flooki10/TFG/blob/main/superposition.png)
---

## 2. **Objetivos**
- [ ] Implementar un modelo eficiente para segmentación de células en imágenes FISH.
- [ ] Contar automáticamente el número de células segmentadas.
- [ ] Crear contornos para las células segmentadas.
- [ ] Extraer características morfológicas de las células, como el área, perímetro y forma.

---

## 3. **Tecnologías y Herramientas**
- **Lenguaje:** Python
- **Framework:** PyTorch
- **Modelo:** MEDIAR para segmentación de imágenes
- **Backend:** Flask
- **Frontend:** Customtkinter
- **API:** Ngrok

---

## 4. **Fuentes propias del Proyecto**
```bash
- Visualizar las predicciones https://www.dropbox.com/scl/fi/0xhvpypr6w5d8hs7bf1g4/ejecucion_local.zip?rlkey=4m09gpca0suau43j90uaq8iqd&st=uq5mgke2&dl=0
- Entrenar el modelo https://www.dropbox.com/scl/fi/0oq3e0tslsbetnzics9lg/MEDIAR.zip?rlkey=jp0avsefnlopj8jqy7kzhdw4s&st=pt2av0cm&dl=0
