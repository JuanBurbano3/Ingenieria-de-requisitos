# Creado Por Fernando Rosero y Juan José Burbano -- 16 - agosto - 2023.

class TrainTicketApp:
    def __init__(self):
        self.destinations = ["Miranda", "Villa Nueva", "San Jorge", "San Gregorio", "Ciudad Grande"]
        self.selected_destinations = []
        self.total_cost = 0

    def add_destination(self, destination):
        if destination and destination not in self.selected_destinations and len(self.selected_destinations) < 5:
            self.selected_destinations.append(destination)
            self.total_cost += 6000  #Definimos un precio que en este caso decidimos que sean $6000 COP
            print(f"Destino '{destination}' agregado. Costo total: ${self.total_cost}")
        else:
            print("No se pudo agregar el destino.")

    def clear_form(self): #Creamos la función para limpiar el formulario.
        self.selected_destinations = []
        self.total_cost = 0
        print("Formulario limpiado.")

    def process_payment(self): #Ahora creamos la función para realizar el pago
        if self.selected_destinations:
            print("Proceso de pago:")
            card_number = input("Número de tarjeta: ")
            card_holder = input("Titular de la tarjeta: ")
            card_cvv = input("Ingrese su CVV")
            card_date = input("Fecha de vencimiento")
            print("Pago exitoso.")

        else:
            print("Debe seleccionar al menos un destino antes de continuar con el pago.")

    def show_cart(self):
        if self.selected_destinations:
            print("Carrito de Compras:")
            for destination in self.selected_destinations:
                print(f"- {destination}")
        else:
            print("El carrito de compras está vacío.")

if __name__ == "__main__":
    app = TrainTicketApp()

                #ESTE ES UN MENÚ DE SELECCIÓN.

    while True:
        print("\n===== Menú Principal =====")
        print("1. Agregar Destino")
        print("2. Limpiar Formulario")
        print("3. Continuar con el Pago")
        print("4. Ver Carrito de Compras")
        print("5. Salir")

        choice = input("Seleccione una opción: ")

        if choice == "1":
            destination = input("Ingrese el destino que desea agregar: ")
            app.add_destination(destination)
        elif choice == "2":
            app.clear_form()
        elif choice == "3":
            app.process_payment()
        elif choice == "4":
            app.show_cart()
        elif choice == "5":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

#GRACIAS POR SU ATENCIóN
