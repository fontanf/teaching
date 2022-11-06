import treesearchsolverpy

import json
import math
from functools import total_ordering

# Sequential Ordering Problem.
# (Asymmetric Travelling Salesman Problem with Precedence Constraints)
#
# Input:
# - n locations and an n×n matrix containing the distances between each pair of
#   locations (not necessarily symmetric)
# - a directed acyclic graph such that each vertex corresponds to a location
# Problem:
# - find a route from location 1 such that:
#   - each location is visited exactly once
#   - precedence constraints are satisfied
#   - if there exists an arc from vertex j1 to vertex j2 in G, then location
#     j1 is visited before location j2
# Objective:
# - Minimize the total length of the route
#
# Fill skeleton given below of the branching scheme for the Sequential
# Ordering Problem.
# Start from the provided example for the Travelling Salesman Problem:
# https://github.com/fontanf/treesearchsolverpy/blob/main/examples/travellingsalesman.py


class Location:
    id = -1
    x = 0
    y = 0
    predecessors = None


class Instance:

    def __init__(self, filepath=None):
        self.locations = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                locations = zip(
                        data["xs"],
                        data["ys"])
                for (x, y) in locations:
                    self.add_location(x, y)
                for location_id_2, location_id_1 in data["precedences"]:
                    self.add_predecessor(location_id_2, location_id_1)

    def add_location(self, x, y):
        location = Location()
        location.id = len(self.locations)
        location.x = x
        location.y = y
        location.predecessors = []
        self.locations.append(location)

    def add_predecessor(self, location_id_1, location_id_2):
        self.locations[location_id_1].predecessors.append(location_id_2)

    def distance(self, location_id_1, location_id_2):
        xd = self.locations[location_id_2].x - self.locations[location_id_1].x
        yd = self.locations[location_id_2].y - self.locations[location_id_1].y
        d = round(math.sqrt(xd * xd + yd * yd))
        return d

    def write(self, filepath):
        data = {"xs": [location.x for location in self.locations],
                "ys": [location.y for location in self.locations],
                "precedences": [(j1, j2)
                                for j2, location in enumerate(self.locations)
                                for j1 in location.predecessors]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            n = len(self.locations)
            data = json.load(json_file)
            locations = data["locations"]
            length = 0
            location_pred_id = 0
            number_of_precedences_violations = 0
            visited = set()
            visited.add(0)
            for location_id in data["locations"]:
                for location_id_2 in self.locations[location_id].predecessors:
                    if location_id_2 not in visited:
                        number_of_precedences_violations += 1
                length += self.distance(location_pred_id, location_id)
                visited.add(location_id)
                location_pred_id = location_id
            number_of_duplicates = len(locations) - len(set(locations))

            is_feasible = (
                    (number_of_duplicates == 0)
                    and len(locations) == n - 1
                    and 0 not in locations
                    and number_of_precedences_violations == 0)
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Number of locations: {len(locations) + 1} / {n}")
            print(f"Number of precedences violations:"
                  f"{number_of_precedences_violations}")
            print(f"Feasible: {is_feasible}")
            print(f"Length: {length}")
            return (is_feasible, length)


class BranchingScheme:

    @total_ordering
    class Node:

        id = None
        father = None
        # TODO START
        # TODO END
        guide = None
        next_child_pos = 0

        def __lt__(self, other):
            if self.guide != other.guide:
                return self.guide < other.guide
            return self.id < other.id

    def __init__(self, instance):
        self.instance = instance
        self.id = 0

    def root(self):
        node = self.Node()
        node.father = None
        # TODO START
        # TODO END
        node.guide = 0
        node.id = self.id
        self.id += 1
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
        for number_of_locations in range(1, 101):
            instance = Instance()
            total_weight = 0
            for location_id in range(number_of_locations):
                x = random.randint(0, 1000)
                y = random.randint(0, 1000)
                instance.add_location(x, y)
            precedences = set()
            n = (number_of_locations - 1) * (number_of_locations - 2) // 2
            d = random.randint(10, 30)  # density
            number_of_precedences = n * d // 100
            for _ in range(number_of_precedences):
                location_id_1 = random.randint(1, number_of_locations - 1)
                location_id_2 = random.randint(1, number_of_locations - 2)
                if location_id_2 >= location_id_1:
                    location_id_2 += 1
                precedences.add((
                    min(location_id_1, location_id_2),
                    max(location_id_1, location_id_2)))
            for location_id_1, location_id_2 in precedences:
                instance.add_predecessor(location_id_2, location_id_1)
            instance.write(
                    args.instance + "_" + str(number_of_locations) + ".json")

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)

    else:
        instance = Instance(args.instance)
        branching_scheme = BranchingScheme(instance)
        if args.algorithm == "greedy":
            output = treesearchsolverpy.greedy(
                    branching_scheme)
        elif args.algorithm == "best_first_search":
            output = treesearchsolverpy.best_first_search(
                    branching_scheme,
                    time_limit=30)
        elif args.algorithm == "iterative_beam_search":
            output = treesearchsolverpy.iterative_beam_search(
                    branching_scheme,
                    time_limit=30)
        solution = branching_scheme.to_solution(output["solution_pool"].best)
        if args.certificate is not None:
            data = {"locations": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
