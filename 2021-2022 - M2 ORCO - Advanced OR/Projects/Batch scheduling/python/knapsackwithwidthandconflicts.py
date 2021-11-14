import treesearchsolverpy
import json
from functools import total_ordering


class Item:
    id = -1
    weight = 0
    width = 0
    profit = 0
    conflicting_items = None


class Instance:

    def __init__(self, filepath=None):
        self.items = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.capacity = data["capacity"]
                items = zip(
                        data["item_weights"],
                        data["item_widths"],
                        data["item_profits"])
                for (weight, width, profit) in items:
                    self.add_item(weight, width, profit)
                for item_id_1, item_id_2 in data["conflicts"]:
                    self.add_conflict(item_id_1, item_id_2)

    def add_item(self, weight, width, profit):
        item = Item()
        item.id = len(self.items)
        item.weight = weight
        item.width = width
        item.profit = profit
        item.conflicting_items = []
        self.items.append(item)

    def add_conflict(self, item_id_1, item_id_2):
        self.items[item_id_1].conflicting_items.append(item_id_2)
        self.items[item_id_2].conflicting_items.append(item_id_1)

    def write(self, filepath):
        data = {"capacity": self.capacity,
                "item_weights": [item.weight for item in self.items],
                "item_widths": [item.width for item in self.items],
                "item_profits": [item.profit for item in self.items],
                "conflicts": [
                    (item_1.id, item_2.id)
                    for item_1 in self.items
                    for item_2 in self.items
                    if item_1.id in item_2.conflicting_items
                    and item_1.id < item_2.id]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            profit = sum(self.items[item_id].profit
                         for item_id in data["items"])
            weight = sum(self.items[item_id].weight
                         for item_id in data["items"])
            width = max((self.items[item_id].width
                         for item_id in data["items"]),
                        default=0)
            number_of_conflicts = sum(
                    1
                    for item_id_1 in data["items"]
                    for item_id_2 in data["items"]
                    if item_id_1 in self.items[item_id_2].conflicting_items
                    and item_id_1 < item_id_2)
            number_of_duplicates = len(data["items"]) - len(set(data["items"]))
            is_feasible = (
                    (number_of_duplicates == 0)
                    and (number_of_conflicts == 0)
                    and (weight <= self.capacity))
            objective_value = profit - width
            print(f"Profit: {profit}")
            print(f"Weight: {weight} / {self.capacity}")
            print(f"Width: {width}")
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Number of conflicts: {number_of_conflicts}")
            print(f"Feasible: {is_feasible}")
            print(f"Objective value: {objective_value}")
            return (is_feasible, objective_value)


class BranchingScheme:

    @total_ordering
    class Node:

        father = None
        # TODO START
        # TODO END
        guide = None
        next_child_pos = 0

        def __lt__(self, other):
            return self.guide < other.guide

    def __init__(self, instance):
        self.instance = instance

    def root(self):
        node = self.Node()
        node.father = None
        # TODO START
        # TODO END
        node.guide = 0
        return node

    def next_child(self, father):
        # TODO START
        pass
        # TODO END

    def infertile(self, node):
        # TODO START
        pass
        # TODO END

    def leaf(self, node):
        # TODO START
        pass
        # TODO END

    def bound(self, node_1, node_2):
        # TODO START
        pass
        # TODO END

    # Solution pool.

    def better(self, node_1, node_2):
        # TODO START
        pass
        # TODO END

    def equals(self, node_1, node_2):
        # TODO START
        pass
        # TODO END

    # Dominances.

    def comparable(self, node):
        # TODO START
        pass
        # TODO END

    class Bucket:

        def __init__(self, node):
            self.node = node

        def __hash__(self):
            # TODO START
            pass
            # TODO END

        def __eq__(self, other):
            # TODO START
            pass
            # TODO END

    def dominates(self, node_1, node_2):
        # TODO START
        pass
        # TODO END

    # Outputs.

    def display(self, node):
        # TODO START
        pass
        # TODO END

    def to_solution(self, node):
        # TODO START
        pass
        # TODO END


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
            "-a", "--algorithm",
            type=str,
            default="iterative_beam_search",
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

    if args.algorithm == "generator":
        import random
        random.seed(0)
        for number_of_items in range(101):
            instance = Instance()
            total_weight = 0
            for item_id in range(number_of_items):
                profit = random.randint(100, 200)
                width = random.randint(100, 200)
                weight = random.randint(100, 200)
                total_weight += weight
                instance.add_item(weight, width, profit)
            instance.capacity = random.randint(
                    total_weight * 1 // 4,
                    total_weight * 2 // 4)
            conflicts = set()
            n = number_of_items * (number_of_items - 1) // 2
            d = random.randint(1, 25)  # density between 1% and 25%
            number_of_conflicts = n * d // 100
            for _ in range(number_of_conflicts):
                item_id_1 = random.randint(0, number_of_items - 1)
                item_id_2 = random.randint(0, number_of_items - 2)
                if item_id_2 >= item_id_1:
                    item_id_2 += 1
                conflicts.add((
                    min(item_id_1, item_id_2),
                    max(item_id_1, item_id_2)))
            for item_id_1, item_id_2 in conflicts:
                instance.add_conflict(item_id_1, item_id_2)
            instance.write(
                    args.instance + "_" + str(number_of_items) + ".json")

    elif args.algorithm == "iterative_beam_search":
        instance = Instance(args.instance)
        branching_scheme = BranchingScheme(instance)
        output = treesearchsolverpy.iterative_beam_search(
                branching_scheme,
                time_limit=30)
        solution = branching_scheme.to_solution(output["solution_pool"].best)
        if args.certificate is not None:
            data = {"items": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            instance.check(args.certificate)

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)
