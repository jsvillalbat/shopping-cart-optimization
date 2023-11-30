from brute_force_algorithm import main, Matrix

# Define cost of product in all stores
product_costs = Matrix(5, 5)
# Precios de la Varilla
product_costs.insert(0, 0, 10)
product_costs.insert(1, 0, 20)
product_costs.insert(2, 0, 30)
product_costs.insert(3, 0, 10)
product_costs.insert(4, 0, 15)
# Precios del Cemento
product_costs.insert(0, 1, 5)
product_costs.insert(1, 1, 10)
product_costs.insert(2, 1, 12)
product_costs.insert(3, 1, 20)
product_costs.insert(4, 1, 5)
# Precios de la Malla
product_costs.insert(0, 2, 10)
product_costs.insert(1, 2, 10)
product_costs.insert(2, 2, 5)
product_costs.insert(3, 2, 10)
product_costs.insert(4, 2, 30)
# Precios de la Teja
product_costs.insert(0, 3, 10)
product_costs.insert(1, 3, 8)
product_costs.insert(2, 3, 11)
product_costs.insert(3, 3, 12)
product_costs.insert(4, 3, 13)
# Precios de la Cinta
product_costs.insert(0, 4, 20)
product_costs.insert(1, 4, 18)
product_costs.insert(2, 4, 19)
product_costs.insert(3, 4, 20)
product_costs.insert(4, 4, 21)

# Define delivery costs of stores
store_delivery_costs = [30, 11, 9, 8, 12]

# cantidad de productos que el usuario quiere comprar
# cantidad = {
#         'Varilla': 2,
#         'Cemento': 5,
#         'Malla': 3,
#         'Teja': 1,
#         'Cinta': 2,
#     }

cantidad = [2, 5, 3, 1, 2]
print("Matriz de precios Seller-Product")
product_costs.print_matrix()
print("Inicia algoritmo de fuerza bruta")
main(store_delivery_costs, cantidad, product_costs)