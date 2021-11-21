"""Multiple Knapsack Problem

Input:
- m containers (knapsacks); for each knapsack i = 1..m,  a capacity cᵢ
- n items; for each item j = 1..n, a profit pⱼ and a weight wⱼ
Problem:
- select m disjoint subsets of items (one per knapsack) such that the total
  weight of the items in a knapsack does not exceed its capacity
Objective:
- Maximize the overall profit of the selected items

The linear programming formulation of the problem based on Dantzig–Wolfe
decomposition is written as follows:

Variables:
- yᵢᵏ ∈ {0, 1} representing a set of items for knapsack i.
  yᵢᵏ = 1 iff the corresponding set of items is selected for knapsack i.
  xⱼᵢᵏ = 1 iff yᵢᵏ contains item j, otherwise 0.

Program:

max ∑ᵢ ∑ₖ (∑ⱼ cⱼ xⱼᵢᵏ) yᵢᵏ
                                     Note that (∑ⱼ cⱼ xⱼᵢᵏ) is a constant.

1 <= ∑ₖ yᵢᵏ <= 1        for all knapsack i
                      (not more than 1 packing selected for each knapsack)
                                                        Dual variables: uᵢ
0 <= ∑ₖ xⱼᵢᵏ yᵢᵏ <= 1   for all items j
                                         (each item selected at most once)
                                                        Dual variables: vⱼ

The pricing problem consists in finding a variable of positive reduced cost.
The reduced cost of a variable yᵢᵏ is given by:
rc(yᵢᵏ) = ∑ⱼ cⱼ xⱼᵢᵏ - uᵢ - ∑ⱼ xⱼᵢᵏ vⱼ
        = ∑ⱼ (cⱼ - vⱼ) xⱼᵢᵏ - uᵢ

Therefore, finding a variable of maximum reduced cost reduces to solving
m Knapsack Problems with items with profit (cⱼ - vⱼ).

"""

# import sys
# sys.path.append("/home/florian/Dev/columngenerationsolverpy/")
import columngenerationsolverpy

import json


class ItemType:
    id = -1
    weight = 0
    profit = 0


class Instance:

    def __init__(self, filepath=None):
        self.items = []
        self.capacities = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.capacities = data["knapsack_capacities"]
                items = zip(
                        data["item_weights"],
                        data["item_profits"])
                for (weight, profit) in items:
                    self.add_item(weight, profit)

    def add_item(self, weight, profit):
        item = ItemType()
        item.id = len(self.items)
        item.weight = weight
        item.profit = profit
        self.items.append(item)

    def write(self, filepath):
        data = {"knapsack_capacities": self.capacities,
                "item_weights": [item.weight for item in self.items],
                "item_profits": [item.profit for item in self.items]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute profit.
            profit = sum(self.items[item_id].profit
                         for i, capacity in enumerate(self.capacities)
                         for item_id in data["items"][i])
            # Compute number_of_overweighted_knapsacks.
            number_of_overweighted_knapsacks = 0
            for knapsack_id, capacity in enumerate(self.capacities):
                weight = sum(self.items[item_id].weight
                             for item_id in data["items"][knapsack_id])
                if weight > capacity:
                    number_of_overweighted_knapsacks += 1
            # Compute number_of_items.
            number_of_items = sum(len(items) for items in data["items"])
            # Compute number_of_duplicates.
            demands = {item_id: 0
                       for item_id in range(len(self.items))}
            for items in data["items"]:
                for item_id in items:
                    demands[item_id] += 1
            number_of_duplicates = 0
            for item_id, item in enumerate(self.items):
                if demands[item_id] > 1:
                    number_of_duplicates += 1

            is_feasible = (
                    (number_of_duplicates == 0)
                    and (number_of_overweighted_knapsacks == 0))
            objective_value = profit
            print(f"Number of items: {number_of_items}")
            print(f"Number of overweighted knapsacks: "
                  f"{number_of_overweighted_knapsacks}")
            print(f"Number of duplicates: "
                  f"{number_of_duplicates}")
            print(f"Feasible: {is_feasible}")
            print(f"Objective value: {objective_value}")
            return (is_feasible, objective_value)


class PricingSolver:

    def __init__(self, instance):
        self.instance = instance
        # TODO START
        # TODO END

    def initialize_pricing(self, columns, fixed_columns):
        # TODO START
        pass
        # TODO END

    def solve_pricing(self, duals):
        # Build subproblem instance.
        # TODO START
        # TODO END

        # Solve subproblem instance.
        # TODO START
        # TODO END

        # Retrieve columns.
        columns = []
        # TODO START
        # TODO END

        return columns


def get_parameters(instance):
    # TODO START
    p = None
    # TODO END
    # Pricing solver.
    p.pricing_solver = PricingSolver(instance)
    return p


def to_solution(instance, columns, fixed_columns):
    m = len(instance.capacities)
    solution = [None] * m
    for column, value in fixed_columns:
        # TODO START
        pass
        # TODO END
    return solution


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
            "-a", "--algorithm",
            type=str,
            default="column_generation",
            help='')
    parser.add_argument(
            "-i", "--instance",
            type=str,
            help='')
    parser.add_argument(
            "-c", "--certificate",
            type=str,
            default=None,
            help='')

    args = parser.parse_args()

    if args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)

    elif args.algorithm == "generator":
        import random
        random.seed(0)
        for number_of_items in range(1, 101):
            instance = Instance()
            number_of_knapsacks = random.randint(
                    number_of_items // 20 + 1,
                    number_of_items // 5 + 1)
            for item_id in range(number_of_items):
                weight = random.randint(10, 50)
                profit = random.randint(100, 500)
                instance.add_item(weight, profit)
            total_weight = sum(item.weight for item in instance.items)
            for _ in range(number_of_knapsacks):
                c = random.randint(
                        total_weight // number_of_knapsacks * 2 // 4,
                        total_weight // number_of_knapsacks * 3 // 4)
                instance.capacities.append(c)
            instance.write(
                    args.instance + "_" + str(number_of_items) + ".json")

    elif args.algorithm == "column_generation":
        instance = Instance(args.instance)
        parameters = get_parameters(instance)
        output = columngenerationsolverpy.column_generation(parameters)

    else:
        instance = Instance(args.instance)
        parameters = get_parameters(instance)
        if args.algorithm == "greedy":
            output = columngenerationsolverpy.greedy(
                    parameters)
        elif args.algorithm == "limited_discrepancy_search":
            output = columngenerationsolverpy.limited_discrepancy_search(
                    parameters,
                    maximum_discrepancy=1)
        solution = to_solution(
                instance, parameters.columns, output["solution"])
        if args.certificate is not None:
            data = {"items": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
