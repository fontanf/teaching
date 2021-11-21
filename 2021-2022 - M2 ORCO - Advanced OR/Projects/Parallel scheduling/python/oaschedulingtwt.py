import json
import treesearchsolverpy
from functools import total_ordering


class Job:
    id = -1
    processing_time = 0
    due_date = 0
    profit = 0
    weight = 0


class Instance:

    def __init__(self, filepath=None):
        self.jobs = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                jobs = zip(
                        data["processing_times"],
                        data["due_dates"],
                        data["profits"],
                        data["weights"])
                for (processing_time, due_date, profit, weight) in jobs:
                    self.add_job(processing_time, due_date, profit, weight)

    def add_job(self, processing_time, due_date, profit, weight):
        job = Job()
        job.id = len(self.jobs)
        job.processing_time = processing_time
        job.due_date = due_date
        job.profit = profit
        job.weight = weight
        self.jobs.append(job)

    def write(self, filepath):
        data = {"processing_time": [job.processing_time for job in self.jobs],
                "due_dates": [job.due_date for job in self.jobs],
                "profits": [job.profit for job in self.jobs],
                "weights": [job.weight for job in self.jobs]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        print("Checker")
        print("-------")
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute total profit.
            profit = sum(self.jobs[job_id].profit
                         for job_id in data["jobs"])
            # Compute total weighted tardiness.
            total_weighted_tardiness = 0
            current_time = 0
            for job_id in data["jobs"]:
                job = self.jobs[job_id]
                current_time += job.processing_time
                if current_time > job.due_date:
                    total_weighted_tardiness \
                            += job.weight * (job.due_date - current_time)
            # Compute number of duplicates.
            number_of_duplicates = len(data["jobs"]) - len(set(data["jobs"]))
            is_feasible = (
                    (number_of_duplicates == 0))
            objective_value = profit - total_weighted_tardiness
            print(f"Profit: {profit}")
            print(f"Total weighted tardiness: {total_weighted_tardiness}")
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Feasible: {is_feasible}")
            print(f"Objective value: {objective_value}")
            return (is_feasible, objective_value)


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
        for number_of_jobs in range(101):
            instance = Instance()
            processing_times = []
            for job_id in range(number_of_jobs):
                processing_times.append(random.randint(10, 100))
            total_time = sum(processing_times)
            for job_id in range(number_of_jobs):
                processing_time = processing_times[job_id]
                x = random.randint(1, 5)
                profit = x * processing_times[job_id]
                weight = random.randint(1, 5)
                due_date = random.randint(1, total_time // 2)
                total_time += weight
                instance.add_job(processing_time, due_date, profit, weight)
            instance.write(
                    args.instance + "_" + str(number_of_jobs) + ".json")

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
            data = {"jobs": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            print()
            instance.check(args.certificate)
