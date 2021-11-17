import json
from functools import total_ordering
import treesearchsolverpy


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
        self.maximum_length = 1
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.maximum_length = data["maximum_length"]
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
        data = {"maximum_length": self.maximum_length,
                "edge_heads": [edge.node_1_id for edge in self.edges],
                "edge_tails": [edge.node_2_id for edge in self.edges],
                "edge_weights": [edge.weight for edge in self.edges]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute number of duplicates.
            nodes = {}
            for edge_id in data["edges"]:
                edge = self.edges[edge_id]
                nodes[edge.node_1_id] = nodes.get(edge.node_1_id, 0)
                nodes[edge.node_2_id] = nodes.get(edge.node_2_id, 0)
            number_of_duplicates = sum(1 for v in nodes.values() if v > 2)
            # Compute is_connected.
            is_connected = True
            node_id_prec = None
            for edge_id in data["edges"]:
                edge = self.edges[edge_id]
                if node_id_prec is not None:
                    if edge.node_1_id != node_id_prec:
                        is_connected = False
                node_id_prec = edge.node_2_id
            # Compute lenght.
            length = len(data["edges"])
            # Compute weight.
            weight = sum(self.edges[edge_id].weight
                         for edge_id in data["edges"])
            is_feasible = (
                    (number_of_duplicates == 0)
                    and is_connected
                    and length <= self.maximum_length)
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Length: {length}")
            print(f"Is connected: {is_connected}")
            print(f"Feasible: {is_feasible}")
            print(f"Weight: {weight} / {self.capacity}")
            return (is_feasible, weight)


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
            if self.guide == other.guide:
                return self.id < other.id
            return self.guide < other.guide

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
        for number_of_nodes in range(101):
            instance = Instance()
            number_of_edges = 6*number_of_nodes if number_of_nodes >= 2 else 0
            edges = set()
            for _ in range(number_of_edges):
                node_id_1 = random.randint(0, number_of_nodes - 1)
                node_id_2 = random.randint(0, number_of_nodes - 2)
                if node_id_2 >= node_id_1:
                    node_id_2 += 1
                edges.add((node_id_1, node_id_2))
            for node_id_1, node_id_2 in edges:
                weight = random.randint(-100, 100)
                instance.add_edge(node_id_1, node_id_2, weight)
            instance.maximum_length = 4
            instance.write(
                    args.instance + "_" + str(number_of_nodes) + ".json")

    elif args.algorithm == "iterative_beam_search":
        instance = Instance(args.instance)
        branching_scheme = BranchingScheme(instance)
        output = treesearchsolverpy.iterative_beam_search(
                branching_scheme,
                time_limit=30)
        solution = branching_scheme.to_solution(output["solution_pool"].best)
        if args.certificate is not None:
            data = {"edges": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            instance.check(args.certificate)

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)
