import json
import columngenerationsolverpy


class Instance:

    def __init__(self, filepath=None):
        self.maximum_work_time = 1
        self.maximum_number_of_shifts = [1, 1, 1]
        self.requests = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.maximum_work_time = data["maximum_work_time"]
                self.maximum_number_of_shifts = (
                        data["maximum_number_of_shifts"])
                self.requests = data["requests"]

    def write(self, filepath):
        data = {"requests": self.requests,
                "maximum_work_time": self.maximum_work_time,
                "maximum_number_of_shifts": self.maximum_number_of_shifts}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)

            number_of_nurses = len(data["nurses"])
            number_of_maximum_shifts_per_day_violations = 0
            number_of_shift_rotation_violations = 0
            number_of_maximum_work_time_violations = 0
            number_of_maximum_number_of_shifts_violations = 0
            number_of_unmet_requests = 0

            # Compute the number of unmet requests.
            for day, requests in enumerate(self.requests):
                for shift in range(3):
                    n = sum(nurse[day][shift]
                            for nurse in data["nurses"])
                    if n != requests[shift]:
                        number_of_unmet_requests += 1

            for nurse in data["nurses"]:
                for day, requests in enumerate(self.requests):
                    if (nurse[day][0]
                            + nurse[day][1]
                            + nurse[day][1] > 1):
                        number_of_maximum_shifts_per_day_violations += 1
                    if (day > 0 and nurse[day - 1][2]
                            + nurse[day][0] > 1):
                        number_of_shift_rotation_violations += 1
                work_time = sum(
                        nurse[day][shift]
                        for day, requests in enumerate(self.requests)
                        for shift in range(3))
                if work_time > self.maximum_work_time:
                    number_of_maximum_work_time_violations += 1
                for shift in range(3):
                    number_of_shifts = sum(
                            nurse[day][shift]
                            for day, requests in enumerate(self.requests))
                    if (number_of_shifts
                            > self.maximum_number_of_shifts[shift]):
                        number_of_maximum_number_of_shifts_violations += 1

            is_feasible = (
                    (number_of_maximum_shifts_per_day_violations == 0)
                    and (number_of_shift_rotation_violations == 0)
                    and (number_of_maximum_work_time_violations == 0)
                    and (number_of_unmet_requests == 0)
                    and (number_of_maximum_number_of_shifts_violations == 0))
            print("Number of maximum shifts per day violations:"
                  f" {number_of_maximum_shifts_per_day_violations}")
            print("Number of shift rotation violations:"
                  f" {number_of_shift_rotation_violations}")
            print("Number of maximum work time violations:"
                  f" {number_of_maximum_work_time_violations}")
            print("Number of unmet requests:"
                  f" {number_of_unmet_requests}")
            print("Number of maximum numbers of shifts of each type"
                  " violations:"
                  f" {number_of_maximum_number_of_shifts_violations}")
            print(f"Number of nurses: {number_of_nurses}")
            print(f"Feasible: {is_feasible}")
            return (is_feasible, number_of_nurses)


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
        for days in range(1, 101):
            instance = Instance()
            requests = [None for _ in range(days)]
            for day in range(days):
                requests[day] = (
                        random.randint(1, 5),
                        random.randint(1, 5),
                        random.randint(1, 5))
            instance.requests = requests
            instance.maximum_work_time = random.randint(int(days / 2), days)
            instance.maximum_number_of_shifts = (
                    random.randint(1, int(days / 3) + 1),
                    random.randint(1, int(days / 3) + 1),
                    random.randint(1, int(days / 5) + 1))
            instance.write(
                    args.instance + "_" + str(days) + ".json")

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
            data = {"nurses": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
