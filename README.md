# TFG: Automatización de la Identificación de Posiciones de Natación Artística (CAMBIAR TITULO CUANDO SE DECIDA)

> Trabajo de Fin de Grado — Paula Ballesteros

## Descripción y objetivo

*primera versión, cambiar cuando proyecto entero*

Este proyecto explora la automatización del reconocimiento y clasificación de posiciones corporales reglamentarias en **natación artística (sincronizada)** mediante técnicas de visión por computador e inteligencia artificial.

El objetivo principal es comparar distintos enfoques de clasificación de imágenes, desde modelos de aprendizaje profundo hasta sistemas basados en coordenadas de pose, evaluando su viabilidad para identificar automáticamente figuras de natación artística a partir de fotografías. Se incluye además un análisis de interpretabilidad mediante **Grad-CAM** para entender qué regiones de la imagen son determinantes en la clasificación.

---

## Dataset y sus clases

El sistema utiliza un conjunto de datos como imágenes original, recogido a mano y que clasifica **5 posiciones násicas de la disciplina**:

*Incluir en la columna definición algo más explicativo*

| Clase | Descripción |
|---|---|
| `Bent Knee Surface Arch Position` | Posición de arco en superficie con rodilla flexionada |
| `Bent Knee Vertical` | Posición vertical con rodilla flexionada |
| `Double Leg Vertical` | Posición vertical con ambas piernas |
| `Fishtail` | Posición de cola de pez |
| `Knight` | Posición de caballero |

---

## Estructura del repositorio

```
TFG_repo/
│
├── Data/                                          # Dataset e índices de imágenes
│   ├── synchronized_swimming.csv                 # Índice del dataset original (ruta → etiqueta)
│   ├── synchronized_swimming_aug.csv             # Índice del dataset aumentado
│   ├── Fotos/                                    # Imágenes originales por clase (no incluidas en el repo)
│   │   ├── Bent Knee Surface Arch Position/
│   │   ├── Bent Knee Vertical/
│   │   ├── Double Leg Vertical/
│   │   ├── Fishtail/
│   │   └── Knight/
│   └── Augmented/                                # Imágenes generadas por data augmentation
│       └── <Clase>/
│           └── IMG_*_aug[1-25].jpg               # 25 versiones aumentadas por imagen original
│
├── Modelos Naïve/                                # Enfoque 1: modelos sobre imagen completa
│   └── Automatización Natación Artistica_Paula Ballesteros.ipynb
│
├── Modelo preentrenado basado en coordenadas/    # Enfoque 2: clasificación por keypoints
│   └── MediaPipe_Pose_Classifier.ipynb
│
├── requirements.txt                              # Toda librería requerida para la ejecución del proyecto
└── README.md
```

### `Data/`

Contiene los metadatos del dataset en formato CSV y las imágenes organizadas por clase. El directorio `Augmented/` almacena las versiones generadas mediante técnicas de data augmentation (rotaciones, volteos, ajustes de brillo y contraste), produciendo **25 imágenes derivadas por cada imagen original**.

- Dataset original: ~264 imágenes
- Dataset aumentado: ~6 600 imágenes

### `Modelos Naïve/`

Notebook de experimentación con modelos que operan directamente sobre la imagen completa. Contiene tres enfoques progresivos:

1. **CNN con *transfer learning*** — red convolucional preentrenada con fine-tuning supervisado sobre el dataset etiquetado.
2. **CLIP (zero-shot)** — modelo visión-lenguaje CLIP que clasifica imágenes comparando sus embeddings con descripciones textuales de cada posición extraídas del reglamento oficial.
3. **CLIP multi-prompt** — extensión del anterior que combina múltiples definiciones por clase (reglamentarias y coloquiales) usando tres estrategias de agregación de embeddings.
4. **CLIP + imágenes de referencia (few-shot)** — enriquece las definiciones textuales con ejemplos visuales de referencia.
5. **Grad-CAM** — análisis de interpretabilidad aplicado sobre CLIP para visualizar qué regiones de la imagen influyen en cada clasificación.

### `Modelo preentrenado basado en coordenadas/`

Notebook que implementa un pipeline alternativo basado en **estimación de poses**:

1. **Extracción de keypoints** con MediaPipe PoseLandmarker (`pose_landmarker_heavy.task`), obteniendo las coordenadas 3D de los 33 puntos de referencia del cuerpo humano.
2. **Clasificación** sobre los vectores de coordenadas con modelos clásicos de ML:
   - Random Forest
   - SVM (Support Vector Machine)

Este enfoque es más ligero computacionalmente y agnóstico al fondo o iluminación de la imagen.

---

## Tecnologías y dependencias principales

| Área | Librería / Herramienta |
|---|---|
| Entorno | Python 3, Jupyter Notebook |
| Deep Learning | TensorFlow / Keras, PyTorch |
| Visión-Lenguaje | CLIP (`transformers`, HuggingFace) |
| Estimación de pose | MediaPipe |
| Procesamiento de imagen | OpenCV, Pillow |
| ML clásico | scikit-learn (Random Forest, SVM) |
| Datos | pandas, NumPy, SciPy |
| Visualización | matplotlib |

### Instalación del entorno

```bash
# 1. Clonar el repositorio
git clone <URL-del-repositorio>
cd TFG_repo

# 2. Instalar todas las dependencias
pip install -r requirements.txt
```

> **Nota:** `torch` y `tensorflow` se descargan desde sus índices oficiales. Si se dispone de GPU, consultar las instrucciones de instalación de [PyTorch con CUDA](https://pytorch.org/get-started/locally/) y [TensorFlow con GPU](https://www.tensorflow.org/install/pip) para sustituir los paquetes CPU por sus versiones aceleradas.

```bash
# 3. Ejecución de cada notebook

```

---

Ejecutar las celdas en orden. Cada notebook es autocontenido e incluye la carga de datos, preprocesado, entrenamiento/evaluación y visualización de resultados.

> Para el notebook de MediaPipe, el modelo `pose_landmarker_heavy.task` se descarga automáticamente en la primera ejecución si no está presente.

---

## Autor

**Paula Ballesteros**
Grado en Ciencia de Datos e Inteligencia Artíficial. Universidad Politécnica de Madrid. 
