import highspy
from pyomo.environ import *
from pyomo.opt import SolverFactory

model = ConcreteModel()

# Sets and parameters
model.P = RangeSet(1, 5)  # Products
model.L = RangeSet(1, 5)  # Stores

model.Costs = Param(model.P, model.L, mutable=True)
model.DeliveryCosts = Param(model.L, mutable=True)

# Costos del seller 1 (columna, fila)
model.Costs[1, 1] = 10
model.Costs[2, 1] = 5
model.Costs[3, 1] = 10
model.Costs[4, 1] = 10
model.Costs[5, 1] = 20
# Costos del seller 2
model.Costs[1, 2] = 20
model.Costs[2, 2] = 10
model.Costs[3, 2] = 10
model.Costs[4, 2] = 8
model.Costs[5, 2] = 18
# Costos del seller 3
model.Costs[1, 3] = 30
model.Costs[2, 3] = 12
model.Costs[3, 3] = 5
model.Costs[4, 3] = 11
model.Costs[5, 3] = 19
# Costos del seller 4
model.Costs[1, 4] = 10
model.Costs[2, 4] = 20
model.Costs[3, 4] = 10
model.Costs[4, 4] = 12
model.Costs[5, 4] = 20
# Costos del seller 5
model.Costs[1, 5] = 15
model.Costs[2, 5] = 5
model.Costs[3, 5] = 30
model.Costs[4, 5] = 13
model.Costs[5, 5] = 21

# disponibilidad
disponibilidad = {
    (0, 0): 1,
    (0, 1): 2,
    (0, 2): 1,
    (0, 3): 2,
    (0, 4): 1,

    (1, 0): 1,
    (1, 1): 1,
    (1, 2): 1,
    (1, 3): 1,
    (1, 4): 1,

    (2, 0): 2,
    (2, 1): 1,
    (2, 2): 2,
    (2, 3): 1,
    (2, 4): 2,

    (3, 0): 1,
    (3, 1): 2,
    (3, 2): 1,
    (3, 3): 2,
    (3, 4): 1,

    (4, 0): 1,
    (4, 1): 2,
    (4, 2): 1,
    (4, 3): 1,
    (4, 4): 2,
}

# Delivery costs per store
model.DeliveryCosts[1] = 10
model.DeliveryCosts[2] = 11
model.DeliveryCosts[3] = 9
model.DeliveryCosts[4] = 8
model.DeliveryCosts[5] = 12

# Cantidad de productos a comprar

cantidad = [2, 5, 3, 1, 2]

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
#highs_path = "/home/sevito/HiGHS/build/bin/highs"
# SolverFactory('highs').solve(model, executable=highs_path)
SolverFactory('appsi_highs').solve(model)
model.display()