import json
import math
import columngenerationsolverpy


class Location:
    id = None
    visit_intervals = None
    x = None
    y = None


class Instance:

    def __init__(self, filepath=None):
        self.locations = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                locations = zip(
                        data["visit_intervals"],
                        data["xs"],
                        data["ys"])
                for (intervals, x, y) in locations:
                    self.add_location(intervals, x, y)

    def add_location(self, visit_intervals, x, y):
        location = Location()
        location.id = len(self.locations)
        location.visit_intervals = visit_intervals
        location.x = x
        location.y = y
        self.locations.append(location)

    def duration(self, location_id_1, location_id_2):
        xd = self.locations[location_id_2].x - self.locations[location_id_1].x
        yd = self.locations[location_id_2].y - self.locations[location_id_1].y
        d = round(math.sqrt(xd * xd + yd * yd))
        return d

    def write(self, filepath):
        data = {"visit_intervals": [location.visit_intervals
                                    for location in self.locations],
                "xs": [location.x for location in self.locations],
                "ys": [location.y for location in self.locations]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute total_distance.
            total_travelled_distance = 0
            on_time = True
            for locations in data["locations"]:
                current_time = -math.inf
                location_pred_id = 0
                for location_id in locations + [0]:
                    location = self.locations[location_id]
                    d = self.duration(location_pred_id, location_id)
                    total_travelled_distance += d
                    t = current_time + d
                    try:
                        interval = min(
                                (itrv for itrv in location.visit_intervals
                                 if itrv[0] >= t),
                                key=lambda interval: interval[1])
                        current_time = interval[1]
                    except ValueError:
                        on_time = False
                    location_pred_id = location_id
            # Compute number_of_locations.
            number_of_duplicates = len(locations) - len(set(locations))

            is_feasible = (
                    (number_of_duplicates == 0)
                    and (on_time)
                    and 0 not in locations)
            objective_value = total_travelled_distance
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"On time: {on_time}")
            print(f"Total travelled distance: {total_travelled_distance}")
            print(f"Feasible: {is_feasible}")
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
    solution = []
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
        for number_of_locations in range(101):
            instance = Instance()
            total_weight = 0
            for location_id in range(number_of_locations):
                s1 = random.randint(0, 1000)
                p1 = random.randint(0, 100)
                s2 = random.randint(0, 1000)
                p2 = random.randint(0, 100)
                x = random.randint(0, 100)
                y = random.randint(0, 100)
                instance.add_location(
                        [(s1, s1 + p1), (s2, s2 + p2)], x, y)
            instance.write(
                    args.instance + "_" + str(number_of_locations) + ".json")

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
            data = {"locations": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
