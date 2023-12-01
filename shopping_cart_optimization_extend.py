import random
import pulp as pl
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Número de productos y sellers

N = 30 # Products
M = 300 # sellers

# Datos de ejemplo
productos = [j for j in range(N)]
proveedores = [i for i in range(M)]

precio = {}
disponibilidad = {}
cantidad = {producto: random.randint(1,3) for producto in productos}
costo_envio = {proveedor: random.randint(10,20) for proveedor in proveedores}
for j in range(M):
    for i in range(N):
        precio[(j,i)] = random.randint(10,40)
        disponibilidad[(j,i)] = random.randint(1,3)

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
# for proveedor in proveedores:
#     for producto in productos:
#         if int(x[proveedor][producto].value()) > 0:
#             print(f"{proveedor} - {producto}: {int(x[proveedor][producto].value())}")
