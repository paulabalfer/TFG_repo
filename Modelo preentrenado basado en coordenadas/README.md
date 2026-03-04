# Modelo Preentrenado Basado en Coordenadas

Directorio que implementa un pipeline de clasificación alternativo fundamentado en **estimación de pose**. En lugar de procesar la imagen en bruto, este enfoque extrae las coordenadas tridimensionales de los puntos clave del cuerpo humano y entrena clasificadores clásicos de machine learning sobre dichos vectores de coordenadas.

---

## Contenido

```
Modelo preentrenado basado en coordenadas/
└── MediaPipe_Pose_Classifier.ipynb    # Pipeline completo de extracción y clasificación
```

---

## Motivación

Los modelos que trabajan directamente sobre la imagen completa pueden verse afectados por variaciones en el fondo, la iluminación, el color del bañador o el ángulo de la cámara. Este enfoque desacopla el problema en dos etapas:

1. **Extracción de estructura corporal** — reducir la imagen a una representación compacta e invariante: las posiciones relativas de las articulaciones.
2. **Clasificación sobre geometría** — entrenar modelos de ML clásico sobre dichas coordenadas, que son intrínsecamente agnósticas al contexto visual.

---

## Pipeline

### Etapa 1: Extracción de Keypoints con MediaPipe

Se utiliza el modelo **MediaPipe PoseLandmarker Heavy** para detectar y extraer los **33 puntos de referencia 3D** del cuerpo humano definidos por el estándar MediaPipe (caderas, rodillas, tobillos, hombros, codos, muñecas, etc.).

- **Entrada**: imagen RGB de la nadadora.
- **Salida**: vector de 33 × 3 coordenadas normalizadas `(x, y, z)`, donde `x` e `y` son fracciones del ancho y alto de la imagen, y `z` representa la profundidad relativa.
- **Modelo**: `pose_landmarker_heavy.task` (descargado automáticamente en la primera ejecución si no está presente).

> La variante *heavy* ofrece mayor precisión en la detección de poses complejas o parcialmente ocluidas, a costa de un mayor coste computacional respecto a las variantes *lite* y *full*.

### Etapa 2: Clasificación con ML Clásico

Sobre los vectores de coordenadas extraídos se entrenan y evalúan dos clasificadores:

| Clasificador | Descripción |
|---|---|
| **Random Forest** | Ensemble de árboles de decisión; robusto a features irrelevantes y con baja varianza |
| **SVM** (Support Vector Machine) | Clasificador de margen máximo; efectivo en espacios de alta dimensión con pocos ejemplos |

Ambos modelos son entrenados con validación cruzada sobre el dataset de natación artística y evaluados mediante métricas estándar (accuracy, precisión, recall, F1, matriz de confusión).

---

## Ventajas de este enfoque

- **Invarianza al fondo e iluminación**: el clasificador solo ve coordenadas de articulaciones, no píxeles.
- **Bajo coste computacional**: los clasificadores clásicos son órdenes de magnitud más ligeros que una CNN.
- **Interpretabilidad**: es posible analizar qué coordenadas (articulaciones) son más discriminativas mediante la importancia de características del Random Forest.
- **Menor requisito de datos**: los modelos de ML clásico generalizan bien con conjuntos pequeños cuando las features son informativas.

---

## Tecnologías

| Componente | Librería / Herramienta |
|---|---|
| Estimación de pose | MediaPipe (`mediapipe`) |
| Clasificadores | scikit-learn (Random Forest, SVM) |
| Procesamiento de imagen | OpenCV, Pillow |
| Cálculo numérico | NumPy, pandas |
| Visualización | matplotlib |
| Entorno de ejecución | Jupyter Notebook |

---

## Ejecución

```bash
pip install -r requirements.txt
jupyter notebook "Modelo preentrenado basado en coordenadas/MediaPipe_Pose_Classifier.ipynb"
```

> En la primera ejecución, el notebook descarga automáticamente el fichero `pose_landmarker_heavy.task` (~25 MB) desde los servidores de Google si no se encuentra en el directorio de trabajo. Es necesaria conexión a internet para este paso.
