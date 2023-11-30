from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Datos de ejemplo
proveedores = ['Proveedor1', 'Proveedor2', 'Proveedor3', 'Proveedor4', 'Proveedor5']
productos = ['Varilla', 'Cemento', 'Malla', 'Teja', 'Cinta']

# Precios de los productos por proveedor
precio = {
    ('Proveedor1', 'Varilla'): 10,
    ('Proveedor1', 'Cemento'): 5,
    ('Proveedor1', 'Malla'): 10,
    ('Proveedor1', 'Teja'): 10,
    ('Proveedor1', 'Cinta'): 20,

    ('Proveedor2', 'Varilla'): 20,
    ('Proveedor2', 'Cemento'): 10,
    ('Proveedor2', 'Malla'): 10,
    ('Proveedor2', 'Teja'): 8,
    ('Proveedor2', 'Cinta'): 18,

    ('Proveedor3', 'Varilla'): 30,
    ('Proveedor3', 'Cemento'): 12,
    ('Proveedor3', 'Malla'): 5,
    ('Proveedor3', 'Teja'): 11,
    ('Proveedor3', 'Cinta'): 19,

    ('Proveedor4', 'Varilla'): 10,
    ('Proveedor4', 'Cemento'): 20,
    ('Proveedor4', 'Malla'): 10,
    ('Proveedor4', 'Teja'): 12,
    ('Proveedor4', 'Cinta'): 20,

    ('Proveedor5', 'Varilla'): 15,
    ('Proveedor5', 'Cemento'): 5,
    ('Proveedor5', 'Malla'): 30,
    ('Proveedor5', 'Teja'): 13,
    ('Proveedor5', 'Cinta'): 21,
}

# Cantidades disponibles de cada producto por proveedor
disponibilidad = {
    ('Proveedor1', 'Varilla'): 1,
    ('Proveedor1', 'Cemento'): 2,
    ('Proveedor1', 'Malla'): 1,
    ('Proveedor1', 'Teja'): 2,
    ('Proveedor1', 'Cinta'): 1,

    ('Proveedor2', 'Varilla'): 1,
    ('Proveedor2', 'Cemento'): 1,
    ('Proveedor2', 'Malla'): 1,
    ('Proveedor2', 'Teja'): 1,
    ('Proveedor2', 'Cinta'): 1,

    ('Proveedor3', 'Varilla'): 2,
    ('Proveedor3', 'Cemento'): 1,
    ('Proveedor3', 'Malla'): 2,
    ('Proveedor3', 'Teja'): 1,
    ('Proveedor3', 'Cinta'): 2,

    ('Proveedor4', 'Varilla'): 1,
    ('Proveedor4', 'Cemento'): 2,
    ('Proveedor4', 'Malla'): 1,
    ('Proveedor4', 'Teja'): 2,
    ('Proveedor4', 'Cinta'): 1,

    ('Proveedor5', 'Varilla'): 1,
    ('Proveedor5', 'Cemento'): 2,
    ('Proveedor5', 'Malla'): 1,
    ('Proveedor5', 'Teja'): 1,
    ('Proveedor5', 'Cinta'): 2,
}

# Costos de envío por proveedor
costo_envio = {
    'Proveedor1': 10,
    'Proveedor2': 11,
    'Proveedor3': 9,
    'Proveedor4': 8,
    'Proveedor5': 12,
}

# Cantidad de productos a comprar
cantidad = {
    'Varilla': 2,
    'Cemento': 5,
    'Malla': 3,
    'Teja': 1,
    'Cinta': 2,
}

# Crear el problema de optimización
problema = LpProblem("OptimizacionCarrito", LpMinimize)

# Crear variables
x = LpVariable.dicts("Compra", (proveedores, productos), lowBound=0, cat='Integer')

# Crear variables binarias
y = LpVariable.dicts("ProveedorUsado", proveedores, cat='Binary')



# Función objetivo: solo se paga el costo de envío una vez por proveedor
problema += lpSum(precio[proveedor, producto] * x[proveedor][producto] for proveedor in proveedores for producto in productos) + \
            lpSum(costo_envio[proveedor] * y[proveedor] for proveedor in proveedores)

# Restricciones: la cantidad de cada producto que se compra de cada proveedor no puede ser mayor que la cantidad disponible
for proveedor in proveedores:
    for producto in productos:
        problema += x[proveedor][producto] <= disponibilidad[proveedor, producto]

# Restricciones: cantidad de productos a comprar
for producto in productos:
    problema += lpSum(x[proveedor][producto] for proveedor in proveedores) == cantidad[producto]

# Restricciones: si se compra algo de un proveedor, la variable binaria correspondiente debe ser 1
for proveedor in proveedores:
    problema += lpSum(x[proveedor][producto] for producto in productos) <= 1000000 * y[proveedor]  # 10000 es un número grande arbitrario

# Resolver el problema
problema.solve()

# Mostrar resultados
print("Estado:", problema.status)
print("Costo total:", round(problema.objective.value(), 2))

# Mostrar cantidades a comprar por proveedor y producto
for proveedor in proveedores:
    for producto in productos:
        if int(x[proveedor][producto].value()) > 0:
            print(f"{proveedor} - {producto}: {int(x[proveedor][producto].value())}")
