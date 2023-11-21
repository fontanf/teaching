import json


class Edge:
    """Class for an edge between two flights.

    Attributes
    ----------

    destination : int
        Id of the destination flight.

    cost : float
        Cost of the edge.

    """

    destination = -1
    cost = -1


class Flight:
    """Class for a flight.

    Attributes
    ----------

    id : int
        Unique id of the flight.

    profit : float
        Profit of the flight.

    successors : list(Edge)
        Edges from this flight.

    """

    id = -1
    profit = 0.0
    successors = None


class Instance:
    """Instance class for a crewpairing1 problem."""

    def __init__(self, filepath=None):
        self.flights = []
        self.add_flight(0)

        self.maximum_number_of_flights = float("inf")
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                # Read flights.
                for profit in data["flight_profits"]:
                    self.add_flight(profit)
                # Read edges.
                edges = zip(
                        data["edge_heads"],
                        data["edge_tails"],
                        data["edge_costs"])
                for (flight_id_1, flight_id_2, cost,) in edges:
                    self.add_edge(flight_id_1, flight_id_2, cost)
                # Read other parameters.
                self.maximum_number_of_flights = (
                        data["maximum_number_of_flights"])

    def add_flight(
            self,
            profit):
        """Add a flight to the instance."""

        flight = Flight()
        flight.id = len(self.flights)
        flight.profit = profit
        flight.successors = []
        self.flights.append(flight)

    def add_edge(
            self,
            flight_id_1,
            flight_id_2,
            cost):
        """Add an edge to the instance."""

        edge = Edge()
        edge.destination = flight_id_2
        edge.cost = cost
        self.flights[flight_id_1].edges.append(edge)

    def check(self, filepath):
        """Check the validity of a solution file."""

        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            number_of_flights = len(data["flights"])
            flights = [0] * len(self.nodes)
            number_of_wrong_edges = 0
            profit = 0
            flight_id_prev = 0
            for flight_id in data["flights"]:
                profit += self.flights[flight_id].profit
                flights[flight_id] += 1
                edge = None
                for e in self.flights[flight_id_prev].successors:
                    if e.destination == flight_id:
                        edge = e
                if edge is None:
                    number_of_wrong_edges += 1
                else:
                    profit -= edge.cost
                flight_id_prev = flight_id
            number_of_duplicates = sum(v > 1 for v in flights)

            final_edge = None
            for e in self.flights[flight_id_prev].successors:
                if e.destination == 0:
                    final_edge = e
            if final_edge is None:
                number_of_wrong_edges += 1

            is_feasible = (
                    number_of_duplicates == 0
                    and number_of_wrong_edges == 0
                    and number_of_flights <= self.maximum_number_of_flights)
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Number of wrong edges: {number_of_wrong_edges}")
            print(f"Number of flights: {number_of_flights}"
                  f" / {self.maximum_number_of_flights}")
            print(f"Feasible: {is_feasible}")
            print(f"Profit: {profit}")
            return (is_feasible, profit)


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
