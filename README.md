# 🛠️ Script Tools: Linux, Bash & Python

Colección personal de herramientas y scripts desarrollados en **Python** y **Bash** enfocados en la automatización de tareas, flujos DevOps y administración de sistemas Linux.

## 🎯 Objetivo del Repositorio

Centralizar utilidades prácticas para optimizar procesos repetitivos en entornos Linux, gestionar descargas masivas de contenido y facilitar tareas de administración de sistemas desde la terminal.

## 📂 Estructura de Proyectos

### 🐍 Python Tools
* **[`internet-images-download-manager-with-python`](./internet-images-download-manager-with-python)**: Gestor de descarga masiva de imágenes desde internet mediante una cola de enlaces (`queue.txt`).
* **[`facebook-images-download-manager-automatized-with-python`](./facebook-images-download-manager-automatized-with-python)**: Herramienta automatizada para la extracción y descarga de álbumes completos de imágenes.

### 🐧 Bash & Linux SysAdmin *(Próximamente)*
* Scripts de monitorización de recursos, copias de seguridad automatizadas y utilidades de mantenimiento del sistema.

## 🚀 Instalación y Uso

Cada herramienta en Python cuenta con su propio archivo de dependencias aislado para evitar conflictos en el sistema:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com
   cd script-tools-linux-bash-python
   ```

2. **Preparar el entorno virtual (ejemplo con uno de los proyectos):**
   ```bash
   cd internet-images-download-manager-with-python
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Ejecutar el script:**
   ```bash
   python3 descargar_fotos.py
   ```

---
*Repositorio en constante crecimiento. Nuevos scripts de Bash y utilidades DevOps en camino.*
