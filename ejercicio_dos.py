class Cliente:
    def __init__(self, codigo, dni, nombre, direccion, telefono, avalado_por=None):
        self.codigo = codigo
        self.dni = dni
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.avalado_por = avalado_por

class Coche:
    def __init__(self, matricula, modelo, color, marca):
        self.matricula = matricula
        self.modelo = modelo
        self.color = color
        self.marca = marca

class Reserva:
    def __init__(self, cliente, coches, agencia, fecha_inicio, fecha_final, precio_alquiler, litros_gasolina, precio_total, puede_cambiar):
        self.cliente = cliente
        self.coches = coches
        self.agencia = agencia
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.precio_alquiler = precio_alquiler
        self.litros_gasolina = litros_gasolina
        self.precio_total = precio_total
        self.puede_cambiar = puede_cambiar

class Agencia:
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion

# Crear instancias de clientes, coches, agencias y reservas
cliente1 = Cliente(codigo=1, dni="12345678A", nombre="Cliente 1", direccion="Dirección 1", telefono="123456789")
cliente2 = Cliente(codigo=2, dni="87654321B", nombre="Cliente 2", direccion="Dirección 2", telefono="987654321")

coche1 = Coche(matricula="ABC123", modelo="Modelo 1", color="Rojo", marca="Marca 1")
coche2 = Coche(matricula="XYZ789", modelo="Modelo 2", color="Azul", marca="Marca 2")

agencia1 = Agencia(nombre="Agencia 1", direccion="Dirección de Agencia 1")

reserva1 = Reserva(cliente=cliente1, coches=[coche1, coche2], agencia=agencia1, fecha_inicio="2023-09-21", fecha_final="2023-09-30", precio_alquiler=500, litros_gasolina=30, precio_total=550, puede_cambiar=True)

# Operaciones adicionales (por ejemplo, buscar clientes, calcular precios, etc.) pueden ser añadidas aquí según tus necesidades.

# Ejemplo de cómo imprimir información de una reserva
print("Información de la Reserva:")
print(f"Cliente: {reserva1.cliente.nombre}")
print(f"Coches: {', '.join([coche.matricula for coche in reserva1.coches])}")
print(f"Agencia: {reserva1.agencia.nombre}")
print(f"Fecha de Inicio: {reserva1.fecha_inicio}")
print(f"Fecha de Final: {reserva1.fecha_final}")
print(f"Precio Total: {reserva1.precio_total}€")
