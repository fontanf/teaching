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
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute number of duplicates.
            nodes_in = [0] * len(self.nodes)
            nodes_out = [0] * len(self.nodes)
            for edge_id in data["edges"]:
                edge = self.edges[edge_id]
                nodes_in[edge.node_1_id] += 1
                nodes_out[edge.node_2_id] += 1
            number_of_duplicates = sum(v > 1 for v in nodes_in)
            number_of_duplicates += sum(v > 1 for v in nodes_out)
            # Compute is_connected and is_cycle.
            is_connected = True
            node_id_prec = None
            for edge_id in data["edges"]:
                edge = self.edges[edge_id]
                if node_id_prec is not None:
                    if edge.node_1_id != node_id_prec:
                        is_connected = False
                node_id_prec = edge.node_2_id
            is_cycle = (node_id_prec == self.edges[data["edges"][0]].node_1_id)
            # Compute lenght.
            length = len(data["edges"])
            # Compute weight.
            weight = sum(self.edges[edge_id].weight
                         for edge_id in data["edges"])

            is_feasible = (
                    (number_of_duplicates == 0)
                    and is_connected
                    and is_cycle
                    and length <= self.maximum_length)
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Length: {length}")
            print(f"Is cycle: {is_cycle}")
            print(f"Is connected: {is_connected}")
            print(f"Feasible: {is_feasible}")
            print(f"Weight: {weight}")
            return (is_feasible, weight)


def dynamic_programming(instance):
    # TODO START
    pass
    # TODO END


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
            "-a", "--algorithm",
            type=str,
            default="dynamic_programming",
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

    if args.algorithm == "dynamic_programming":
        instance = Instance(args.instance)
        solution = dynamic_programming(instance)
        if args.certificate is not None:
            data = {"edges": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)
