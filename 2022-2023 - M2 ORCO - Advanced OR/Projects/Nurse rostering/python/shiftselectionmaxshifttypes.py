import json
import treesearchsolverpy
from functools import total_ordering


class Instance:

    def __init__(self, filepath=None):
        self.maximum_work_time = 1
        self.maximum_number_of_shifts = [1, 1, 1]
        self.profits = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.maximum_work_time = data["maximum_work_time"]
                self.maximum_number_of_shifts = (
                        data["maximum_number_of_shifts"])
                self.profits = data["profits"]

    def write(self, filepath):
        data = {"profits": self.profits,
                "maximum_work_time": self.maximum_work_time,
                "maximum_number_of_shifts": self.maximum_number_of_shifts}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)

            number_of_maximum_shifts_per_day_violations = 0
            number_of_shift_rotation_violations = 0
            number_of_maximum_work_time_violations = 0
            number_of_maximum_number_of_shifts_violations = 0
            total_profit = sum(
                    data["shifts"][day][shift] * self.profits[day][shift]
                    for day, requests in enumerate(self.requests)
                    for shift in range(2))

            for day, requests in enumerate(self.requests):
                if (data["shifts"][day][0]
                        + data["shifts"][day][1]
                        + data["shifts"][day][1] > 1):
                    number_of_maximum_shifts_per_day_violations += 1
                if (day > 0 and data["shifts"][day - 1][2]
                        + data["shifts"][day][0] > 1):
                    number_of_shift_rotation_violations += 1
            work_time = sum(
                    v
                    for day, request in enumerate(self.requests)
                    for shift in range(2)
                    for v in data["shifts"][day][shift])
            if work_time > self.maximum_work_time:
                number_of_maximum_work_time_violations += 1
            for shift in range(2):
                number_of_shifts = sum(
                        v
                        for day, request in enumerate(self.requests)
                        for v in data["shifts"][day][shift])
                if (number_of_shifts
                        > self.maximum_number_of_shifts[shift]):
                    number_of_maximum_number_of_shifts_violations += 1

            is_feasible = (
                    (number_of_maximum_shifts_per_day_violations == 0)
                    and (number_of_shift_rotation_violations == 0)
                    and (number_of_maximum_work_time_violations == 0)
                    and (number_of_maximum_number_of_shifts_violations == 0))
            print("Number of maximum shifts per day violations:"
                  f" {number_of_maximum_shifts_per_day_violations}")
            print("Number of shift rotation violations:"
                  f" {number_of_shift_rotation_violations}")
            print("Number of maximum work time violations:"
                  f" {number_of_maximum_work_time_violations}")
            print("Number of maximum numbers of shifts of each type"
                  " violations:"
                  f" {number_of_maximum_number_of_shifts_violations}")
            print(f"Profit: {total_profit}")
            print(f"Feasible: {is_feasible}")
            return (is_feasible, total_profit)


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

    if args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)

    elif args.algorithm == "generator":
        import random
        random.seed(0)
        for days in range(1, 101):
            instance = Instance()
            profits = [None for _ in range(days)]
            for day in range(days):
                profits[day] = (
                        random.randint(0, 1000),
                        random.randint(0, 1000),
                        random.randint(0, 1000))
            instance.profits = profits
            instance.maximum_work_time = random.randint(int(days / 2), days)
            instance.maximum_number_of_shifts = (
                    random.randint(1, int(days / 3) + 1),
                    random.randint(1, int(days / 3) + 1),
                    random.randint(1, int(days / 5) + 1))
            instance.write(
                    args.instance + "_" + str(days) + ".json")

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
            data = {"nurses": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
