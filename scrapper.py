import csv
import time
from datetime import datetime
import pytz
from playwright.sync_api import sync_playwright

# Lista de tus sitios
sitios = {
    "Hertz": "https://www.hertzmexico.com/",
    "Dollar": "https://dollarmexico.com.mx/",
    "Thrifty": "https://www.thrifty.com.mx/",
    "Firefly": "https://www.fireflycarrental.com.mx/",
    "Avis": "https://avis.mx/",
    "National": "https://nationalcar.com.mx/",
    "Alamo": "https://www.alamo.com.mx/es",
    "Mex Rent A Car": "https://mexrentacar.com/es/index",
    "Budget": "https://budget.com.mx/#/",
    "Localiza": "https://www.localiza.com/mexico/es-mx",
    "Enterprise": "https://enterprise.mx/",
    "Europcar": "https://www.europcar.com.mx/"
}

# Configuración de hora local
zona_horaria = pytz.timezone('America/Mexico_City')
fecha_hora_actual = datetime.now(zona_horaria)
fecha = fecha_hora_actual.strftime("%Y-%m-%d")
hora = fecha_hora_actual.strftime("%H:%M:%S")

resultados = []

with sync_playwright() as p:
    # Simulamos ser un navegador Chrome normal en Windows para evitar bloqueos
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for nombre, url in sitios.items():
        start_time = time.time()
        estado = "Error"
        codigo = 0
        tiempo_carga = 0
        try:
            # Va a la página y espera a que el contenido básico cargue (sin esperar trackers pesados)
            response = page.goto(url, timeout=45000, wait_until="domcontentloaded")
            tiempo_carga = round(time.time() - start_time, 2)
            if response:
                codigo = response.status
                estado = "OK" if response.ok else "Fallo"
        except Exception as e:
            tiempo_carga = round(time.time() - start_time, 2)
            estado = "Error de conexión o Bloqueo"

        resultados.append([fecha, hora, nombre, url, estado, codigo, tiempo_carga])
        time.sleep(2) # Pequeña pausa para que parezca comportamiento humano

    browser.close()

# Abre el archivo CSV existente y agrega los nuevos datos sin borrar los anteriores
with open('reporte_carga.csv', 'a', newline='', encoding='utf-8') as archivo:
    writer = csv.writer(archivo)
    writer.writerows(resultados)
