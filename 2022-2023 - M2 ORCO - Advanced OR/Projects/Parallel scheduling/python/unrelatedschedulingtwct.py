import json
import columngenerationsolverpy


class Job:
    id = -1
    processing_times = None
    weight = 0


class Instance:

    def __init__(self, filepath=None):
        self.jobs = []
        self.number_of_machines = 1
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.number_of_machines = data["number_of_machines"]
                jobs = zip(
                        data["processing_times"],
                        data["weights"])
                for (processing_times, weight) in jobs:
                    self.add_job(processing_times, weight)

    def add_job(self, processing_times, weight):
        job = Job()
        job.id = len(self.jobs)
        job.processing_times = processing_times
        job.weight = weight
        self.jobs.append(job)

    def write(self, filepath):
        data = {"number_of_machines": self.number_of_machines,
                "processing_times": [job.processing_times
                                     for job in self.jobs],
                "weights": [job.weight for job in self.jobs]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute total weighted completion time.
            total_weighted_completion_time = 0
            for i in range(self.number_of_machines):
                current_time = 0
                for job_id in data["jobs"][i]:
                    job = self.jobs[job_id]
                    current_time += job.processing_times[i]
                    total_weighted_completion_time += job.weight * current_time
            # Compute number of scheduled jobs and number of duplicates.
            job_list = [job_id
                        for i in range(self.number_of_machines)
                        for job_id in data["jobs"][i]]
            job_set = set(job_list)
            number_of_scheduled_jobs = len(job_set)
            number_of_duplicates = len(job_list) - len(job_set)

            is_feasible = (
                    (number_of_scheduled_jobs == len(self.jobs))
                    (number_of_duplicates == 0))
            print(f"Total weighted completion time: "
                  f"{total_weighted_completion_time}")
            print(f"Number of scheduled jobs: {number_of_scheduled_jobs}")
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Feasible: {is_feasible}")
            return (is_feasible, total_weighted_completion_time)


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
            data = {"jobs": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
