import json


class Instance:

    def __init__(self, filepath=None):
        self.maximum_work_time = 1
        self.maximum_number_of_shifts = [1, 1, 1]
        self.profits = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.maximum_work_time = data["maximum_work_time"]
                self.profits = data["profits"]

    def write(self, filepath):
        data = {"profits": self.profits,
                "maximum_work_time": self.maximum_work_time}
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

            is_feasible = (
                    (number_of_maximum_shifts_per_day_violations == 0)
                    and (number_of_shift_rotation_violations == 0)
                    and (number_of_maximum_work_time_violations == 0))
            print("Number of maximum shifts per day violations:"
                  f" {number_of_maximum_shifts_per_day_violations}")
            print("Number of shift rotation violations:"
                  f" {number_of_shift_rotation_violations}")
            print("Number of maximum work time violations:"
                  f" {number_of_maximum_work_time_violations}")
            print(f"Profit: {total_profit}")
            print(f"Feasible: {is_feasible}")
            return (is_feasible, total_profit)


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
            data = {"locations": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)
