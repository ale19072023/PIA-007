import PersonajesESP
import planetasESP
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main_menu():
    option = 0
    print("\n¡Bienvenido al programa!")
    print("1. Ver información de personajes de Star Wars")
    print("2. Ver información de planetas de Star Wars")
    print("3. Salir del programa")

    option = input("Seleccione una opción: ")

    if option == "1":
        PersonajesESP.menu_personajes()
    elif option == "2":
        planetasESP.menu_planeta()
    elif option == "3":
        print("¡Hasta luego!... ¡Y que la fuerza te acompañe 👋🖖!")
        exit()
    else:
        print("Opción inválida, intente de nuevo.")
        main_menu()

if __name__ == "__main__":
    main_menu()