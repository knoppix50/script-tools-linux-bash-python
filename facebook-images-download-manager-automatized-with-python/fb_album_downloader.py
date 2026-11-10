import os
import time
import shutil  # NUEVO: Para duplicar el perfil de manera segura
import requests
import pyautogui  # Para simular la pulsación física de la flecha derecha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# ==========================================
# CONFIGURACIÓN 
# ==========================================

# 1. Pega la URL de la primera imagen en grande (Modo Teatro)
URL_PRIMERA_FOTO = "https://www.facebook.com/photo/?fbid=122126901123433295&set=pcb.122126903451433295"

# 2. TRUCO DE CONTROL: Pon aquí el número exacto de fotos a descargar
TOTAL_DIAPOSITIVAS = 55

# 3. Tu ruta real de perfil detectada
RUTA_COMPLETA_PERFIL = "/home/knoppix/.config/mozilla/firefox/gmomol3r.default-release"

# NUEVO: Ruta aislada para la copia de seguridad que usará el script
RUTA_PERFIL_TEMPORAL = "/home/knoppix/.config/mozilla/firefox/perfil_bot_fb"

# 4. Carpeta de destino
CARPETA_DESTINO = "/home/knoppix/Pictures/FB_PicsDownloaded/DataCache"


# ==========================================

def configurar_navegador():
    opciones = Options()
    opciones.set_preference("dom.webnotifications.enabled", False)
    
    # -------------------------------------------------------------------
    # ¡EL CAMBIO CRUCIAL!: Duplicar el perfil para proteger el original
    # -------------------------------------------------------------------
    if os.path.exists(RUTA_PERFIL_TEMPORAL):
        try:
            shutil.rmtree(RUTA_PERFIL_TEMPORAL)
        except Exception as e:
            print(f"[!] Nota: No se pudo limpiar el perfil temporal anterior: {e}")
    
    print(f"[+] Generando copia segura del perfil en: {RUTA_PERFIL_TEMPORAL}")
    # Copiamos ignorando archivos de bloqueo activos de tu Firefox real
    shutil.copytree(
        RUTA_COMPLETA_PERFIL, 
        RUTA_PERFIL_TEMPORAL, 
        ignore=shutil.ignore_patterns('lock', 'parent.lock', '.parentlock', 'sessionstore*')
    )
    
    print(f"[+] Cargando sesión aislada desde la copia...")
    opciones.add_argument("-profile")
    opciones.add_argument(RUTA_PERFIL_TEMPORAL)  # Usamos la copia, no el original
    # -------------------------------------------------------------------
    
    servicio = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=servicio, options=opciones)

def descargar_imagen_real(url_img, ruta_guardado):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}
    try:
        contenido = requests.get(url_img, headers=headers, timeout=10).content
        with open(ruta_guardado, "wb") as f:
            f.write(contenido)
        return True
    except Exception as e:
        print(f" [!] Error al escribir en disco: {e}")
        return False

def main():
    if not os.path.exists(CARPETA_DESTINO):
        os.makedirs(CARPETA_DESTINO)
        
    print("[+] Inicializando Firefox con tu sesión...")
    driver = configurar_navegador()
    
    contador = 1
    ultima_url_img = ""
    
    try:
        print(f"[+] Abriendo la primera foto del manual...")
        driver.get(URL_PRIMERA_FOTO)
        
        print("\n" + "="*60)
        print("[!] ATENCIÓN: Haz un clic físico con tu ratón en el centro de la")
        print(" pantalla negra de Firefox para asegurar el foco de la ventana.")
        print("="*60)
        
        # Margen de cortesía para que hagas clic en la foto y se estabilice
        time.sleep(15)
        
        # --- BUCLE CON LÍMITE ESTRICTO ---
        while contador <= TOTAL_DIAPOSITIVAS:
            url_imagen_alta = None
            
            # Buscamos las etiquetas img visibles en pantalla
            elementos_img = driver.find_elements(By.TAG_NAME, "img")
            
            for img in elementos_img:
                try:
                    src = img.get_attribute("src")
                    if src and "fbcdn" in src:
                        if "p100x100" not in src and "p50x50" not in src:
                            url_imagen_alta = src
                            break
                except:
                    continue
                    
            if not url_imagen_alta:
                try:
                    url_imagen_alta = driver.find_element(By.XPATH, "//img").get_attribute("src")
                except:
                    pass
                    
            # Si no hay imagen válida, esperamos un poco e intentamos de nuevo antes de rendirnos
            if not url_imagen_alta:
                print(" [!] Esperando a que renderice la imagen...")
                time.sleep(4)
                continue
                
            nombre_archivo = f"diapositiva_{contador:03d}.jpg"
            ruta_completa = os.path.join(CARPETA_DESTINO, nombre_archivo)
            
            print(f"[{contador:03d}/{TOTAL_DIAPOSITIVAS}] Descargando: {nombre_archivo}")
            if descargar_imagen_real(url_imagen_alta, ruta_completa):
                contador += 1
            
            ultima_url_img = url_imagen_alta
            
            # Si ya hemos descargado la última que queríamos, rompemos el bucle
            if contador > TOTAL_DIAPOSITIVAS:
                break
                
            # Avanzar diapositiva simulando teclado
            print(" [→] Avanzando diapositiva...")
            pyautogui.press('right')
            
            # Pausa para que cambie la diapositiva tranquilamente
            time.sleep(5)
            
    finally:
        print("\n==========================================")
        print(f"Hecho. Total descargado con éxito: {contador - 1} imágenes.")
        print("==========================================")
        driver.quit()

if __name__ == "__main__":
    main()

