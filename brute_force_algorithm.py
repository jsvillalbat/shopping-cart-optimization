from itertools import product
from dataclasses import dataclass
import time


@dataclass
class Matrix:
    size_x: int
    size_y: int
    matrix: list[list] = None

    def __post_init__(self):
        if self.matrix is None:
            self.matrix = [[999] * self.size_x for _ in range(self.size_y)]

    def insert(self, x, y, value):
        self.matrix[x][y] = value

    def print_matrix(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                print(f"Precio del seller {i+1} y del producto {j+1}: {self.matrix[i][j]}")
        print("\n")


def main(sdc, sp, pc):
    store_delivery_costs, shopping_cart, price_matrix = sdc, sp, pc
    perm_array = [i for i in range(1, len(store_delivery_costs)+1)]
    permutations = [list(p) for p in product(perm_array, repeat=len(perm_array))]
    costs = list()

    t1 = time.time()

    for permutation in permutations:
        total_cost = 0
        for i in range(len(permutation)):
            if permutation[i] != 0:
                # Costo * Cantidad de productos en ese seller
                total_cost += price_matrix.matrix[permutation[i]-1][i] * shopping_cart[i]

        # Se suma el costo de envio de ese seller
        stores = list(set(permutation))
        for i in range(len(stores)):
            if stores[i] != 0:
                total_cost += store_delivery_costs[stores[i]-1]

        costs.append(total_cost)

    t2 = time.time()

    minimum = min(costs)
    index = costs.index(minimum)
    permutation = permutations[index]
    print(f"Minimum cost: {minimum}")
    print(f"Time: {t2-t1}")
    print(f"Permutation: {permutation}")