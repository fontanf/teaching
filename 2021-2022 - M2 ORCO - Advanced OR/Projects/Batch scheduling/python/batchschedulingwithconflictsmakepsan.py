import json
import columngenerationsolverpy


class Job:
    id = -1
    processing_time = None
    size = None
    conflicting_jobs = None


class Instance:

    def __init__(self, filepath=None):
        self.jobs = []
        self.batch_capacity = 1
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.batch_capacity = data["batch_capacity"]
                jobs = zip(
                        data["job_processing_times"],
                        data["job_sizes"])
                for (processing_time, size) in jobs:
                    self.add_job(processing_time, size)
                for job_id_1, job_id_2 in data["conflicts"]:
                    self.add_conflict(job_id_1, job_id_2)

    def add_job(self, processing_time, size):
        job = Job()
        job.id = len(self.jobs)
        job.processing_time = processing_time
        job.size = size
        job.conflicting_jobs = []
        self.jobs.append(job)

    def add_conflict(self, job_id_1, job_id_2):
        self.jobs[job_id_1].conflicting_jobs.append(job_id_2)
        self.jobs[job_id_2].conflicting_jobs.append(job_id_1)

    def write(self, filepath):
        data = {"batch_capacity": self.batch_capacity,
                "job_processing_times": [job.processing_time
                                         for job in self.jobs],
                "job_sizes": [job.size for job in self.jobs],
                "conflicts": [
                    (job_1.id, job_2.id)
                    for job_1 in self.jobs
                    for job_2 in self.jobs
                    if job_1.id in job_2.conflicting_jobs
                    and job_1.id < job_2.id]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute makespan.
            makespan = sum(max(self.jobs[job_id].processing_time
                               for job_id in batch)
                           for batch in data["jobs"])
            # Compute number_of_overweighted_batches.
            number_of_overweighted_batches = sum(
                    sum(self.jobs[job_id].size for job_id in batch)
                    > self.batch_capacity
                    for batch in data["jobs"])
            # Compute number_of_scheduled jobs and number_of_duplicates.
            job_list = [job_id
                        for batch in data["jobs"]
                        for job_id in batch]
            job_set = set(job_list)
            number_of_scheduled_jobs = len(job_set)
            number_of_duplicates = len(job_list) - len(job_set)
            # Compute number_of_conflicts.
            number_of_conflicts = sum(
                    sum(
                        job_id_1 in self.jobs[job_id_2].conflicting_jobs
                        and job_id_1 < job_id_2
                        for job_id_1 in batch
                        for job_id_2 in batch)
                    for batch in data["jobs"])

            is_feasible = (
                    (number_of_scheduled_jobs == len(self.jobs)) and
                    (number_of_duplicates == 0) and
                    (number_of_overweighted_batches == 0) and
                    (number_of_conflicts == 0))
            print(f"Makespan: {makespan}")
            print(f"Number of scheduled jobs: {number_of_scheduled_jobs}")
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Number of overweighted batches: "
                  f"{number_of_overweighted_batches}")
            print(f"Number of conflicts: {number_of_conflicts}")
            print(f"Feasible: {is_feasible}")
            return (is_feasible, makespan)


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
        for number_of_jobs in range(101):
            instance = Instance()
            instance.batch_capacity = 1000
            for job_id in range(number_of_jobs):
                processing_time = random.randint(100, 500)
                size = random.randint(100, 500)
                instance.add_job(processing_time, size)
            conflicts = set()
            n = number_of_jobs * (number_of_jobs - 1) // 2
            d = random.randint(1, 25)  # density between 1% and 25%
            number_of_conflicts = n * d // 100
            for _ in range(number_of_conflicts):
                job_id_1 = random.randint(0, number_of_jobs - 1)
                job_id_2 = random.randint(0, number_of_jobs - 2)
                if job_id_2 >= job_id_1:
                    job_id_2 += 1
                conflicts.add((
                    min(job_id_1, job_id_2),
                    max(job_id_1, job_id_2)))
            for job_id_1, job_id_2 in conflicts:
                instance.add_conflict(job_id_1, job_id_2)
            instance.write(
                    args.instance + "_" + str(number_of_jobs) + ".json")

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
