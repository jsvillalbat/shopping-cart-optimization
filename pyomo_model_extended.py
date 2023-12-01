import random
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

# Cnatidad de productos y sellers
N = 20 # Productos
M = 100 # sellers

# Sets and parameters
model.P = RangeSet(1, N)  # Products
model.L = RangeSet(1, M)  # Stores

model.Costs = Param(model.P, model.L, mutable=True)
model.DeliveryCosts = Param(model.L, mutable=True)

cantidad = [random.randint(1, 3) for _ in range(N)]

disponibilidad = {}
for j in range(1, M+1):
    model.DeliveryCosts[j] = random.randint(10, 20)
    for i in range(1, N+1):
        model.Costs[i, j] = random.randint(10, 40)
        disponibilidad[j-1, i-1] = random.randint(1, 3)

# Variables
model.x = Var(model.P, model.L, domain=Integers, bounds=(0, None))  # Products Quantity selected
model.y = Var(model.L, domain=Binary)  # Purchase in shop

"""
Objective function
"""
model.targetFunc = Objective(expr=sum(sum(model.Costs[j, l]*model.x[j, l] for j in model.P) + model.DeliveryCosts[l] * model.y[l] for l in model.L), sense=minimize)


# Constraints
def activate_y_if_l_is_chosen(model, l):
    """
    This restriction indicates that if at least one product is chosen from a store l,
    the variable Y must be activated, since it means that a purchase
    is being made in store l.
    """
    return sum(model.x[j, l] - len(model.P)*model.y[l] for j in model.P) <= 0


def wanted_products_must_be_bought(model, j):
    """
    This restriction indicates that for each available product that the buyer wants,
    exactly 1 of them must be purchased. That is, it is not possible to buy more than
    one specific product per store.
    """
    return sum(model.x[j, l] for l in model.L) == cantidad[j-1]

def product_availability(model, j, l):
    """
    This restriction indicates that the quantity of each product that is bought from each store
    cannot be greater than the available quantity.
    """
    return model.x[j, l] <= disponibilidad[l-1, j-1]

model.product_availability = Constraint(model.P, model.L, rule=product_availability)
model.activate_y = Constraint(model.L, rule=activate_y_if_l_is_chosen)
model.wanted_products = Constraint(model.P, rule=wanted_products_must_be_bought)

# Applying the solver
SolverFactory('appsi_highs').solve(model)
model.display()