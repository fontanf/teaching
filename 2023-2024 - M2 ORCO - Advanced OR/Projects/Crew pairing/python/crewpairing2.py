import json
from functools import total_ordering
import treesearchsolverpy


class Edge:
    """Class for an edge between two flights.

    Attributes
    ----------

    destination : int
        Id of the destination flight.

    cost : float
        Cost of the edge.

    duration : float
        Duration of the edge.

    """

    destination = -1
    cost = -1
    duration = -1


class Flight:
    """Class for a flight.

    The flight with id 0 corresponds to the base.

    Attributes
    ----------

    id : int
        Unique id of the flight.

    profit : float
        Profit of the flight.

    successors : list(Edge)
        Edges from this flight.

    departure_time : float
        Departure time of the flight.

    arrival_time : float
        Arrival time of the flight.

    """

    id = -1
    profit = 0.0
    successors = None
    departure_time = -1
    arrival_time = -1


class Instance:
    """Instance class for a crewpairing2 problem."""

    def __init__(self, filepath=None):
        self.flights = []
        self.add_flight(
                0,
                float("inf"),
                0)

        self.maximum_number_of_flights = float("inf")
        self.maximum_duration = float("inf")
        self.maximum_flying_time = float("inf")
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                # Read flights.
                flights = zip(
                        data["flight_profits"],
                        data["flight_departure_time"],
                        data["flight_arrival_time"])
                for (profit, departure_time, arrival_time) in flights:
                    self.add_flight(profit, departure_time, arrival_time)
                # Read edges.
                edges = zip(
                        data["edge_heads"],
                        data["edge_tails"],
                        data["edge_costs"],
                        data["edge_durations"])
                for (flight_id_1, flight_id_2, cost, duration) in edges:
                    self.add_edge(flight_id_1, flight_id_2, cost, duration)
                # Read other parameters.
                self.maximum_number_of_flights = (
                        data["maximum_number_of_flights"])
                self.maximum_duration = data["maximum_duration"]
                self.maximum_flying_time = data["maximum_flying_time"]

    def add_flight(
            self,
            profit,
            departure_time,
            arrival_time):
        """Add a flight to the instance."""

        flight = Flight()
        flight.id = len(self.flights)
        flight.profit = profit
        flight.departure_time = departure_time
        flight.arrival_time = arrival_time
        flight.successors = []
        self.flights.append(flight)

    def add_edge(
            self,
            flight_id_1,
            flight_id_2,
            cost,
            duration):
        """Add an edge to the instance."""

        edge = Edge()
        edge.destination = flight_id_2
        edge.cost = cost
        edge.duration = duration
        self.flights[flight_id_1].successors.append(edge)

    def write(self, filepath):
        """Write the instance to a file."""

        # for flight_id, flight in enumerate(self.flights):
        #     print("flight_id_1", flight_id)
        #     for edge in flight.successors:
        #         print("  flight_id_2", edge.destination)

        data = {"maximum_number_of_flights": self.maximum_number_of_flights,
                "maximum_flying_time": self.maximum_flying_time,
                "maximum_duration": self.maximum_duration,
                "flight_profits": [
                    flight.profit
                    for flight in self.flights[:-1]],
                "flight_departure_times": [
                    flight.departure_time
                    for flight in self.flights[:-1]],
                "flight_arrival_times": [
                    flight.arrival_time
                    for flight in self.flights[:-1]],
                "edge_heads": [
                    flight_id_1
                    for flight_id_1, flight in enumerate(self.flights)
                    for edge in flight.successors],
                "edge_tails": [
                    edge.destination
                    for flight_id_1, flight in enumerate(self.flights)
                    for edge in flight.successors],
                "edge_costs": [
                    edge.cost
                    for flight_id_1, flight in enumerate(self.flights)
                    for edge in flight.successors],
                "edge_durations": [
                    edge.duration
                    for flight_id_1, flight in enumerate(self.flights)
                    for edge in flight.successors]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        """Check the validity of a solution file."""

        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            number_of_flights = len(data["flights"])
            flights = [0] * len(self.nodes)
            number_of_wrong_edges = 0
            duration = 0
            departure_time = None
            current_time = 0
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
                    if departure_time is None:
                        departure_time = (
                            self.flights[flight_id].departure_time
                            - edge.duration)
                    current_time = self.flights[flight_id].arrival_time
                    profit -= edge.cost
                flight_id_prev = flight_id
            number_of_duplicates = sum(v > 1 for v in flights)

            final_edge = None
            for e in self.flights[flight_id_prev].successors:
                if e.destination == 0:
                    final_edge = e
            if final_edge is None:
                number_of_wrong_edges += 1
            arrival_time = current_time + final_edge.duration
            duration = arrival_time - departure_time

            # Compute duration.
            flying_time = sum(self.flights[flight_id].arrival_time
                              - self.flights[flight_id].departure_time
                              for flight_id in data["flights"])

            is_feasible = (
                    number_of_duplicates == 0
                    and number_of_wrong_edges == 0
                    and number_of_flights <= self.maximum_number_of_flights
                    and flying_time <= self.maximum_flying_time
                    and duration <= self.maximum_duration)
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Number of wrong edges: {number_of_wrong_edges}")
            print(f"Number of flights: {number_of_flights}"
                  f" / {self.maximum_number_of_flights}")
            print(f"Flying time: {flying_time}"
                  f" / {self.maximum_flying_time}")
            print(f"Duration: {duration}"
                  f" / {self.maximum_duration}")
            print(f"Feasible: {is_feasible}")
            print(f"Profit: {profit}")
            return (is_feasible, profit)


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
        for number_of_flights in range(101):
            instance = Instance()

            instance.maximum_number_of_flights = (
                    random.randint(3, 10))
            instance.maximum_flying_time = (
                    random.randint(100, 500))
            instance.maximum_duration = (
                    random.randint(200, 1000))

            # Add flights.
            for _ in range(number_of_flights):
                departure_time = random.randint(0, 1000)
                arrival_time = departure_time + random.randint(10, 100)
                profit = departure_time + random.randint(10, 100)
                instance.add_flight(
                        profit,
                        departure_time,
                        arrival_time)
            # Add edges.
            for flight_id_1 in range(number_of_flights + 1):
                flight_1 = instance.flights[flight_id_1]
                for flight_id_2 in range(number_of_flights + 1):
                    if flight_id_1 == flight_id_2:
                        continue
                    flight_2 = instance.flights[flight_id_2]
                    duration = random.randint(10, 100)
                    if (flight_1.arrival_time + duration
                            > flight_2.departure_time):
                        continue
                    cost = random.randint(10, 50)
                    instance.add_edge(
                            flight_id_1,
                            flight_id_2,
                            cost,
                            duration)
            instance.write(
                    args.instance + "_" + str(number_of_flights) + ".json")

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
            data = {"edges": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
