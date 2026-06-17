# 🌊 Predicción de la Potabilidad del Agua

Dashboard interactivo para el análisis exploratorio de datos (EDA) y predicción de la potabilidad del agua utilizando técnicas de Machine Learning y visualizaciones interactivas con Dash y Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.18.1-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.24.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [Uso del Dashboard](#-uso-del-dashboard)
- [Dataset](#-dataset)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Autores](#-autores)
- [Licencia](#-licencia)

## 🎯 Descripción

Este proyecto aborda el problema de la potabilidad del agua mediante un enfoque de ciencia de datos. Se desarrolla un dashboard interactivo que permite:

1. **Análisis Exploratorio de Datos (EDA)**: Visualización completa de las características fisicoquímicas del agua
2. **Estadísticas Descriptivas**: Resumen detallado de todas las variables
3. **Análisis de Correlación**: Identificación de relaciones entre variables
4. **Visualizaciones Interactivas**: Gráficos personalizables para explorar los datos
5. **Predicción**: Modelos de Machine Learning para clasificar la potabilidad del agua

### Contexto del Problema

La calidad del agua es un aspecto fundamental para la salud humana. El consumo de agua contaminada puede generar diversas enfermedades y afectar significativamente la calidad de vida de la población. Este proyecto busca responder a la pregunta:

> **¿Es posible predecir la potabilidad del agua a partir de sus características fisicoquímicas mediante el uso de modelos de aprendizaje automático?**

## ✨ Características

- 📊 **Dashboard Interactivo**: Interfaz moderna y responsiva con Bootstrap
- 🎨 **Visualizaciones Dinámicas**: Gráficos interactivos con Plotly
- 📈 **Análisis Estadístico Completo**: Estadísticas descriptivas y correlaciones
- 🔍 **Filtros Personalizables**: Explora los datos según tus intereses
- 📱 **Diseño Responsivo**: Funciona en dispositivos móviles y desktop
- 🚀 **Despliegue Fácil**: Compatible con Docker, Heroku y Render
- 🤖 **Machine Learning**: Modelos predictivos para clasificación

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje de programación |
| Dash | 2.18.1 | Framework para dashboards web |
| Plotly | 5.24.1 | Visualizaciones interactivas |
| Pandas | 2.2.3 | Manipulación de datos |
| NumPy | 2.1.3 | Cálculos numéricos |
| Scikit-learn | 1.5.2 | Machine Learning |
| Statsmodels | 0.14.4 | Análisis estadístico |
| Dash Bootstrap Components | 1.6.0 | Componentes UI |
| Gunicorn | 23.0.0 | Servidor WSGI para producción |

## 📁 Estructura del Proyecto

```
water_potability_project/
│
├── .vscode/
│   └── settings.json          # Configuración de VSCode
│
├── assets/                    # Recursos estáticos (imágenes, CSS)
│   └── (tus imágenes aquí)
│
├── data/
│   ├── water_potability.csv   # Dataset principal
│   └── get_data.py            # Script para cargar datos
│
├── .gitattributes             # Configuración de Git
├── .gitignore                 # Archivos ignorados por Git
├── app.py                     # Aplicación principal Dash
├── Dockerfile                 # Configuración Docker
├── Procfile                   # Configuración para Heroku/Render
├── README.md                  # Documentación del proyecto
└── requirements.txt           # Dependencias de Python
```

## 🚀 Instalación y Ejecución

### 0. Requisitos Previos

Asegúrate de tener instalado:
- Python 3.10 o superior
- Git (opcional, para clonar el repositorio)
- Conda/Miniconda (recomendado) o pip

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Mariacamilamay/potabilidad-agua/tree/master/docs/water_potability_project
cd water_potability_project
```

### 2. Crear Entorno Virtual (Recomendado)

#### Opción A: Con Conda
```bash
conda create -n water_env python=3.10 -y
conda activate water_env
```

#### Opción B: Con venv
```bash
python -m venv water_env
source water_env/bin/activate  # Linux/Mac
water_env\Scripts\activate     # Windows
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Preparar el Dataset

Coloca tu archivo `water_potability.csv` en la carpeta `data/`:

```bash
mv water_potability.csv data/
```

**¿No tienes el dataset?** Descárgalo desde Kaggle:
- URL: https://www.kaggle.com/datasets/adityakadiwal/water-potability

### 5. Ejecutar la Aplicación

```bash
python app.py
```

### 6. Acceder al Dashboard

Abre tu navegador y visita: **http://127.0.0.1:8050/**

## 📖 Uso del Dashboard

### Navegación

El dashboard tiene 5 secciones principales accesibles desde la barra de navegación:

1. **📋 Introducción**: Contexto del proyecto
2. **🎯 Problema**: Planteamiento del problema de investigación
3. **🎯 Objetivos**: Objetivos generales y específicos
4. **💡 Justificación**: Importancia del proyecto
5. **📊 Análisis EDA**: Análisis exploratorio completo

### Sección EDA

La sección de Análisis Exploratorio incluye:

- **Tarjetas de Estadísticas**: Resumen rápido de los datos
- **Vista de Datos**: Primeras filas del dataset
- **Información General**: Tipos de datos y valores nulos
- **Estadísticas Descriptivas**: Media, mediana, desviación estándar, etc.
- **Distribución de Potabilidad**: Gráfico de barras de la variable objetivo
- **Correlación con Potabilidad**: Variables más relacionadas
- **Matriz de Correlación**: Heatmap de todas las correlaciones
- **Visualizaciones Interactivas**:
  - Histogramas, Box plots y Violin plots
  - Scatter plots con línea de tendencia opcional

### Controles Interactivos

- **Selector de Variable**: Elige qué variable visualizar
- **Tipo de Gráfico**: Cambia entre histograma, box plot o violin plot
- **Scatter Plot**: Selecciona variables para ejes X e Y
- **Línea de Tendencia**: Activa/desactiva la regresión lineal

## 📊 Dataset

### Descripción

El dataset contiene 3,276 muestras de agua con 10 características fisicoquímicas:

| Variable | Descripción | Unidad |
|----------|-------------|--------|
| `ph` | Nivel de pH | - |
| `Hardness` | Dureza del agua | mg/L |
| `Solids` | Sólidos totales disueltos | ppm |
| `Chloramines` | Cloraminas | ppm |
| `Sulfate` | Sulfatos | mg/L |
| `Conductivity` | Conductividad eléctrica | μS/cm |
| `Organic_carbon` | Carbono orgánico total | mg/L |
| `Trihalomethanes` | Trihalometanos | μg/L |
| `Turbidity` | Turbidez | NTU |
| `Potability` | Potabilidad (0=No potable, 1=Potable) | - |

### Fuente

Dataset obtenido de Kaggle: [Water Potability](https://www.kaggle.com/datasets/adityakadiwal/water-potability)

## 🖼️ Capturas de Pantalla

### Página Principal
![Hero Section](assets/hero_screenshot.png)

### Análisis EDA
![EDA Section](assets/eda_screenshot.png)

### Visualizaciones Interactivas
![Interactive Plots](assets/interactive_screenshot.png)

*Nota: Agrega tus propias capturas de pantalla en la carpeta `assets/`*

## 🐳 Despliegue con Docker

### Construir la Imagen

```bash
docker build -t water-potability-app .
```

### Ejecutar el Contenedor

```bash
docker run -p 8050:8050 water-potability-app
```

### Acceder

Visita: **http://localhost:8050/**

## ☁️ Despliegue en la Nube

### Heroku

1. Crea una cuenta en [Heroku](https://heroku.com)
2. Instala Heroku CLI
3. Ejecuta:

```bash
heroku login
heroku create tu-app-name
git push heroku main
```

### Render

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente el `Procfile`
4. ¡Listo! Se desplegará automáticamente

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Maria May** - *Desarrolladora*
- **Andrea Padilla** - *Desarrolladora*
- **Alberto Jimenez** - *Desarrollador*
- **Winston Pardo** - *Desarrollador*

## 📞 Contacto

Para preguntas o sugerencias, por favor abre un issue en GitHub.

## 🙏 Agradecimientos

- Dataset proporcionado por [Kaggle](https://www.kaggle.com/)
- Documentación de [Dash](https://dash.plotly.com/)
- Documentación de [Plotly](https://plotly.com/python/)
- Comunidad de [Stack Overflow](https://stackoverflow.com/)

## 📚 Referencias

1. World Health Organization (WHO). Guidelines for drinking-water quality.
2. Environmental Protection Agency (EPA). National Primary Drinking Water Regulations.
3. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR.

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**

**📊 Versión:** 1.0.0  
**📅 Última actualización:** Junio 2026
