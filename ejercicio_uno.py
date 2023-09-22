class Empleado:
    def __init__(self, nombre, edad, sueldo_bruto, categoria=None, subordinados=None):
        self.nombre = nombre
        self.edad = edad
        self.sueldo_bruto = sueldo_bruto
        self.categoria = categoria
        self.subordinados = subordinados if subordinados is not None else []

class Cliente:
    def __init__(self, nombre, edad, telefono):
        self.nombre = nombre
        self.edad = edad
        self.telefono = telefono

class Empresa:
    def __init__(self, nombre, empleados=None, clientes=None):
        self.nombre = nombre
        self.empleados = empleados if empleados is not None else []
        self.clientes = clientes if clientes is not None else []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def mostrar_empleados(self):
        print("Empleados de", self.nombre)
        for empleado in self.empleados:
            print(f"Nombre: {empleado.nombre}, Edad: {empleado.edad}, Sueldo Bruto: {empleado.sueldo_bruto}")
            if empleado.categoria:
                print(f"Categoría: {empleado.categoria}")
            if empleado.subordinados:
                print("Subordinados:")
                for subordinado in empleado.subordinados:
                    print(f"- {subordinado.nombre}")

    def mostrar_clientes(self):
        print("Clientes de", self.nombre)
        for cliente in self.clientes:
            print(f"Nombre: {cliente.nombre}, Edad: {cliente.edad}, Teléfono: {cliente.telefono}")

# Ejemplo de uso:
if __name__ == "__main__":
    empleado1 = Empleado("Juan", 30, 50000, "Gerente")
    empleado2 = Empleado("Maria", 25, 40000)
    empleado3 = Empleado("Pedro", 35, 55000, "Supervisor")
    empleado4 = Empleado("Laura", 28, 42000)

    empleado1.subordinados = [empleado2, empleado3]
    
    cliente1 = Cliente("Carlos", 40, "123-456-7890")
    cliente2 = Cliente("Ana", 35, "987-654-3210")

    empresa = Empresa("Mi Empresa")
    empresa.agregar_empleado(empleado1)
    empresa.agregar_empleado(empleado4)
    empresa.agregar_cliente(cliente1)
    empresa.agregar_cliente(cliente2)

    empresa.mostrar_empleados()
    empresa.mostrar_clientes()
