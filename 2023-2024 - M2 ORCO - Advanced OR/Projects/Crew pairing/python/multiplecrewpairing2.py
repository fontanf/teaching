import columngenerationsolverpy

import json


class Edge:
    id = -1
    node_1_id = -1
    node_2_id = -1
    weight = 1


class Node:
    id = -1
    edges = None  # list of (edge_id, node_id)


class Instance:

    def __init__(self, filepath=None):
        self.nodes = []
        self.edges = []
        self.selfless_donors = []
        self.maximum_length = 1
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.maximum_length = data["maximum_cycle_length"]
                self.maximum_length = data["maximum_path_length"]
                self.selfless_donors = data["selfless_donors"]
                edges = zip(
                        data["edge_heads"],
                        data["edge_tails"],
                        data["edge_weights"])
                for (node_1_id, node_2_id, weight) in edges:
                    self.add_edge(node_1_id, node_2_id, weight)

    def add_node(self):
        node = Node()
        node.id = len(self.nodes)
        node.edges = []
        self.nodes.append(node)

    def add_edge(self, node_id_1, node_id_2, weight):
        edge = Edge()
        edge.id = len(self.edges)
        edge.node_1_id = node_id_1
        edge.node_2_id = node_id_2
        edge.weight = weight
        self.edges.append(edge)
        while max(node_id_1, node_id_2) >= len(self.nodes):
            self.add_node()
        self.nodes[node_id_1].edges.append((edge.id, node_id_2))

    def write(self, filepath):
        data = {"maximum_cycle_length": self.maximum_cycle_length,
                "maximum_path_length": self.maximum_path_length,
                "selfless_donors": self.selfless_donors,
                "edge_heads": [edge.node_1_id for edge in self.edges],
                "edge_tails": [edge.node_2_id for edge in self.edges],
                "edge_weights": [edge.weight for edge in self.edges]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute number of duplicates.
            nodes_in = [0] * len(self.nodes)
            nodes_out = [0] * len(self.nodes)
            for edges in data["cycles"] + data["paths"]:
                for edge_id in edges:
                    edge = self.edges[edge_id]
                    nodes_in[edge.node_1_id] += 1
                    nodes_out[edge.node_2_id] += 1
            number_of_duplicates = sum(v > 1 for v in nodes_in)
            number_of_duplicates += sum(v > 1 for v in nodes_out)
            # Compute number_of_wrong_cycles.
            number_of_wrong_cycles = 0
            for edges in data["cycles"]:
                is_connected = True
                node_id_prec = None
                for edge_id in edges:
                    edge = self.edges[edge_id]
                    if node_id_prec is not None:
                        if edge.node_1_id != node_id_prec:
                            is_connected = False
                    node_id_prec = edge.node_2_id
                is_cycle = (node_id_prec == self.edges[edges[0]].node_1_id)
                length = len(edges)
                if (
                        not is_connected
                        or not is_cycle
                        or length > self.maximum_cycle_length):
                    number_of_wrong_cycles += 1
            # Compute number_of_wrong_paths.
            number_of_wrong_paths = 0
            for edges in data["paths"]:
                is_connected = True
                node_id_prec = None
                for edge_id in edges:
                    edge = self.edges[edge_id]
                    if node_id_prec is not None:
                        if edge.node_1_id != node_id_prec:
                            is_connected = False
                    node_id_prec = edge.node_2_id
                length = len(edges)
                if (
                        # not an altruistic donner.
                        not self.edges[edges[0]].node_1_id in self.selfless_donors
                        or not is_connected
                        or length > self.maximum_path_length):
                    number_of_wrong_paths += 1
            # Compute weight.
            weight = sum(self.edges[edge_id].weight
                         for edge_id in edges
                         for edges in data["cycles"] + data["paths"])

            is_feasible = (
                    (number_of_duplicates == 0)
                    and (number_of_wrong_cycles == 0)
                    and (number_of_wrong_paths == 0))
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Number of wrong cycles: {number_of_wrong_cycles}")
            print(f"Number of wrong paths: {number_of_wrong_paths}")
            print(f"Feasible: {is_feasible}")
            print(f"Weight: {weight}")
            return (is_feasible, weight)


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

        # Retrieve column.
        column = columngenerationsolverpy.Column()
        # TODO START
        # TODO END

        return [column]


def get_parameters(instance):
    # TODO START
    number_of_constraints = None
    p = columngenerationsolverpy.Parameters(number_of_constraints)
    # TODO END
    # Pricing solver.
    p.pricing_solver = PricingSolver(instance)
    return p


def to_solution(columns, fixed_columns):
    solution = {'cycles': [], 'paths': []}
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
        for number_of_nodes in range(101):
            instance = Instance()
            number_of_edges = 6*number_of_nodes if number_of_nodes >= 2 else 0
            number_of_selfless = random.randint(number_of_nodes//16, number_of_nodes//5)
            edges = set()
            for _ in range(number_of_edges):
                node_id_1 = random.randint(0, number_of_nodes - 1)
                node_id_2 = random.randint(0, number_of_nodes - 2)
                while node_id_2 < number_of_selfless:
                    node_id_2 = random.randint(0, number_of_nodes - 2)
                if node_id_2 >= node_id_1:
                    node_id_2 += 1
                edges.add((node_id_1, node_id_2))
            for node_id_1, node_id_2 in edges:
                weight = random.randint(10, 100)
                instance.add_edge(node_id_1, node_id_2, weight)
            instance.maximum_cycle_length = 4
            instance.maximum_path_length = 15
            instance.selfless_donors = [i for i in range(number_of_selfless)]
            instance.write(
                    args.instance + "_" + str(number_of_nodes) + ".json")

    elif args.algorithm == "column_generation":
        instance = Instance(args.instance)
        output = columngenerationsolverpy.column_generation(
                get_parameters(instance))

    else:
        instance = Instance(args.instance)
        parameters = get_parameters(instance)
        if args.algorithm == "greedy":
            output = columngenerationsolverpy.greedy(
                    parameters)
        elif args.algorithm == "limited_discrepancy_search":
            output = columngenerationsolverpy.limited_discrepancy_search(
                    parameters)
        solution = to_solution(parameters.columns, output["solution"])
        if args.certificate is not None:
            with open(args.certificate, 'w') as json_file:
                json.dump(solution, json_file)
            print()
            instance.check(args.certificate)
