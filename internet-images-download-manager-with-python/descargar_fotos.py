import os
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# ==========================================
# CONFIGURACIÓN DE RUTAS Y ARCHIVOS
# ==========================================
# Cambia 'mi_usuario' por tu nombre de usuario real de Linux Mint
CARPETA_DESTINO = "/home/knoppix/Pictures/Portfolio/images"
ARCHIVO_COLA = "queue.txt"
# ==========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def obtener_nombre_unico(ruta_carpeta, nombre_base):
    """
    Verifica si un archivo existe en la carpeta de destino.
    Si ya existe, añade un sufijo numérico (_001, _002, etc.) en runtime.
    """
    nombre, extension = os.path.splitext(nombre_base)
    contador = 1
    nuevo_nombre = nombre_base
    ruta_completa = os.path.join(ruta_carpeta, nuevo_nombre)
    
    while os.path.exists(ruta_completa):
        nuevo_nombre = f"{nombre}_{contador:03d}{extension}"
        ruta_completa = os.path.join(ruta_carpeta, nuevo_nombre)
        contador += 1
        
    return nuevo_nombre

def procesar_url(url_objetivo, ruta_final):
    """
    Procesa una única URL: busca enlaces y descarga las imágenes en alta resolución.
    Retorna True si tuvo éxito, False si falló o no encontró imágenes válidas.
    """
    try:
        respuesta = requests.get(url_objetivo, headers=HEADERS, timeout=15)
        respuesta.raise_for_status()
    except Exception as e:
        print(f"   [!] Error de conexión en esta URL: {e}")
        return False

    soup = BeautifulSoup(respuesta.text, "html.parser")
    enlaces = soup.find_all("a", href=True)
    urls_imagenes = []
    patron_imagen = re.compile(r"\.(jpg|jpeg|png|webp)", re.IGNORECASE)

    for enlace in enlaces:
        href = enlace["href"]
        # Filtrado de imágenes por extensión
        if patron_imagen.search(href):
            url_completa = urljoin(url_objetivo, href)
            if url_completa not in urls_imagenes:
                urls_imagenes.append(url_completa)

    # Si no se encontraron imágenes, se considera fallo/aborto de URL
    if not urls_imagenes:
        print("   [!] No se encontraron enlaces de imágenes válidos en esta URL.")
        return False

    print(f"   [+] Se encontraron {len(urls_imagenes)} imágenes. Descargando...")

    for i, url in enumerate(urls_imagenes, start=1):
        nombre_archivo_original = os.path.basename(url.split("?")[0])

        if not nombre_archivo_original or not patron_imagen.search(nombre_archivo_original):
            nombre_archivo_original = f"imagen_{i}.jpg"

        # Manejo de nombres duplicados ON RUNTIME (_001.jpg, etc.)
        nombre_final = obtener_nombre_unico(ruta_final, nombre_archivo_original)
        ruta_completa = os.path.join(ruta_final, nombre_final)

        try:
            img_data = requests.get(url, headers=HEADERS, timeout=15).content
            with open(ruta_completa, "wb") as handler:
                handler.write(img_data)
        except Exception as e:
            print(f"   [!] Error al descargar {nombre_archivo_original}: {e}")
            
    return True

def main():
    ruta_final = os.path.abspath(os.path.expanduser(CARPETA_DESTINO))
    if not os.path.exists(ruta_final):
        os.makedirs(ruta_final)

    # Validar que el archivo de la cola existe al lado del script
    if not os.path.exists(ARCHIVO_COLA):
        print(f"Error: No se encuentra el archivo '{ARCHIVO_COLA}'. Por favor, créalo junto al script.")
        return

    # Leer URLs omitiendo líneas vacías
    with open(ARCHIVO_COLA, "r", encoding="utf-8") as f:
        urls = [linea.strip() for linea in f if linea.strip()]

    if not urls:
        print(f"El archivo '{ARCHIVO_COLA}' está vacío. Añade algunas URLs.")
        return

    print(f"Se han cargado {len(urls)} URLs desde la cola.\n" + "="*50)

    urls_fallidas = []

    for idx, url in enumerate(urls, start=1):
        print(f"\n[{idx}/{len(urls)}] Procesando: {url}")
        
        # Ejecuta la descarga. Si aborta/falla, la añadimos a la lista negra
        exito = procesar_url(url, ruta_final)
        
        if not exito:
            urls_fallidas.append(url)
            print(f"   [!] Pasando a la siguiente URL debido a errores.")

    # ==========================================
    # REPORTES Y CIERRE FINAL
    # ==========================================
    print("\n" + "="*50)
    print("Hecho.")
    print("="*50)

    if urls_fallidas:
        print(f"\n[ALERTA] No se pudieron descargar imágenes de las siguientes {len(urls_fallidas)} URLs:")
        for url_error in urls_fallidas:
            print(f" - {url_error}")
    else:
        print("\n[ÉXITO] ¡Todas las URLs de la cola se procesaron limpiamente sin errores!")

if __name__ == "__main__":
    main()

