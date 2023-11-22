import os  
import mainESP
import requests
import matplotlib.pyplot as plt
from collections import Counter
import datetime 

fecha_hora_actual = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


for folder in ["graficas", "imagenes", "consulta_API"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

respuesta = requests.get("http://swapi.dev/api", verify=False)

def menu_personajes():
    opcion = 0
    lista_personajes = []  
    print("\nInformación de personajes:")
    while True:
        print("\n**** Personaje ****")
        print("1. Listar todos los personajes y guardar la lista")
        print("2. Ver detalle de un personaje por ID")
        print("3. Buscar personaje por nombre")
        print("4. Generar gráfica de género")
        print("5. Generar gráfica de color de ojos")
        print("6. Volver al menú principal")
        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            listar_todos_los_personajes(lista_personajes)
        elif opcion == "2":
            id = int(input("Ingrese el ID del personaje: "))
            obtener_personaje_por_id(id)
        elif opcion == "3":
            buscar_personaje_por_nombre()
        elif opcion == "4":
            generar_grafica_distribucion_genero(lista_personajes)
        elif opcion == "5":
            generar_grafica_distribucion_color_ojos(lista_personajes)
        elif opcion == "6":
            mainESP.main_menu()
        else:
            print("Opción inválida")

def listar_todos_los_personajes(lista_personajes):
    url = "https://swapi.dev/api/people/"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos_json = respuesta.json()
        personajes = datos_json['results']
        lista_personajes.extend(personajes)
        for personaje in personajes:
            print(personaje['name'])
    else:
        print(f"Error al realizar la petición: {respuesta.status_code}")

    guardar_lista = input("¿Deseas guardar la lista de personajes? (S/N): ")
    if guardar_lista.upper() == "S":
        guardar_lista_personajes(lista_personajes)

def obtener_personaje_por_id(id):
    respuesta = requests.get(f"https://swapi.dev/api/people/{id}/")
    respuesta.raise_for_status()
    personaje = respuesta.json()

    print(f"Nombre: {personaje['name']}")
    print(f"Altura: {personaje['height']}")
    print(f"Peso: {personaje['mass']}")
    print(f"Año de nacimiento: {personaje['birth_year']}")
    print(f"Género: {personaje['gender']}")
    if personaje['starships']:
        print(f"Naves espaciales en las que ha estado: {obtener_naves_por_urls(personaje['starships'])}")
    else:
        print("No ha estado en ninguna nave espacial.")

def obtener_naves_por_urls(urls):
    naves = []
    for url in urls:
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()
            nombre_nave = respuesta.json()["name"]
            naves.append(nombre_nave)
        except (requests.exceptions.RequestException, KeyError):
            continue
    return naves

def buscar_personaje_por_nombre():
    nombre = input("\nIngresa el nombre del personaje: ")
    respuesta = requests.get(f"https://swapi.dev/api/people/?search={nombre}")
    datos = respuesta.json()

    if datos["count"] == 0:
        print(f"No se encontró el personaje '{nombre}'")
    else:
        for personaje in datos["results"]:
            print("\nNombre:", personaje["name"])
            print("Género:", personaje["gender"])
            print("Altura:", personaje["height"])
            print("Peso:", personaje["mass"])
            print("Color de pelo:", personaje["hair_color"])
            print("Color de ojos:", personaje["eye_color"])
            print("Fecha de nacimiento:", personaje["birth_year"])
            print("Películas:")
            for url_pelicula in personaje["films"]:
                respuesta_pelicula = requests.get(url_pelicula)
                datos_pelicula = respuesta_pelicula.json()
                print("-", datos_pelicula["title"])

def guardar_lista_personajes(lista_personajes):
    fecha_hora_actual = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    with open(f"consulta_API/lista_personajes_{fecha_hora_actual}.txt", "w") as archivo:
        for personaje in lista_personajes:
            archivo.write(personaje["name"] + "\n")
    print("La lista de personajes se ha guardado correctamente.")

def generar_grafica_distribucion_genero(lista_personajes):
    generos = [personaje["gender"] for personaje in lista_personajes]
    conteo_generos = dict(sorted(Counter(generos).items()))

    plt.bar(conteo_generos.keys(), conteo_generos.values())
    plt.title("Distribución de Género de Personajes")
    plt.xlabel("Género")
    plt.ylabel("Cantidad")

    plt.savefig(f"imagenes/distribucion_genero_{fecha_hora_actual}.png")
    plt.show()

def generar_grafica_distribucion_color_ojos(lista_personajes):
    colores_ojos = [personaje["eye_color"] for personaje in lista_personajes]
    conteo_colores_ojos = dict(sorted(Counter(colores_ojos).items()))

    plt.bar(conteo_colores_ojos.keys(), conteo_colores_ojos.values())
    plt.title("Distribución de Color de Ojos de Personajes")
    plt.xlabel("Color de Ojos")
    plt.ylabel("Cantidad")
    
    plt.savefig(f"imagenes/distribucion_color_ojos_{fecha_hora_actual}.png")
    plt.show()