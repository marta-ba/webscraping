import requests
from bs4 import BeautifulSoup
import pandas as pd

# Función para extraer datos de Wikipedia
def extraer_datos_wikipedia(url):
    # Encabezados para simular un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    # Realizamos la solicitud HTTP
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error en la solicitud: {response.status_code}")
        return None

    # Parseamos la información a HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar la tabla específica de los premios Nobel
    tabla = soup.find("table", class_="wikitable")

    # Validamos si encontramos la tabla
    if not tabla:
        print("Tabla no encontrada en la página.")
        return None

    # Extraemos las filas de la tabla
    filas = tabla.find_all("tr")  # Cada fila corresponde a un premio Nobel
    datos = []

       # Iteramos sobre las filas, saltando el encabezado
    for fila in filas[1:]:
        celdas = fila.find_all("td") # busca todas las celdas
        if len(celdas) >= 5:  # Asegurarnos de que la fila tiene al menos 4 celdas para evitar errores con celdas vacías
            anio = celdas[0].text.strip()  # Año del premio y elimina espacios
            nombre = celdas[2].text.strip()  # Nombre del ganador
            pais = celdas[3].text.strip()  # País del ganador
            idioma = celdas[4].text.strip()  # Idioma
            datos.append({"Año": anio, "Nombre": nombre, "País": pais, "Idioma": idioma}) # Agregar a la lista de datos
        else:
            print(f"Fila incompleta encontrada, ignorada: {fila}")

    return datos

# URL de la página de Wikipedia de los premios Nobel de Literatura
url = "https://es.wikipedia.org/wiki/Anexo:Premio_Nobel_de_Literatura"

# Llamamos a la función para obtener los datos
datos_premios = extraer_datos_wikipedia(url)

# Verificamos los datos extraídos
if datos_premios:
    for dato in datos_premios[:5]:  # Mostramos los primeros 5 premios
        print(dato)

# Si quieres guardar los datos en un CSV
import pandas as pd

if datos_premios:
    df = pd.DataFrame(datos_premios)
    df.to_csv("premios_nobel_literatura.csv", index=False)
    print("Datos guardados en 'premios_nobel_literatura.csv'")

    print("\nPrimeros 5 registros del DataFrame:")
    print(df.head())

    