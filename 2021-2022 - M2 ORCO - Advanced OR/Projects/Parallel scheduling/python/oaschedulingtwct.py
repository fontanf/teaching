import json


class Job:
    id = -1
    processing_time = 0
    weight = 0
    profit = 0


class Instance:

    def __init__(self, filepath=None):
        self.jobs = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                jobs = zip(
                        data["processing_times"],
                        data["weights"],
                        data["profits"])
                for (processing_time, weight, profit) in jobs:
                    self.add_job(processing_time, weight, profit)

    def add_job(self, processing_time, weight, profit):
        job = Job()
        job.id = len(self.jobs)
        job.processing_time = processing_time
        job.weight = weight
        job.profit = profit
        self.jobs.append(job)

    def write(self, filepath):
        data = {"processing_time": [job.processing_time for job in self.jobs],
                "weights": [job.weight for job in self.jobs],
                "profits": [job.profit for job in self.jobs]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            # Compute total profit.
            profit = sum(self.jobs[job_id].profit
                         for job_id in data["jobs"])
            # Compute total weighted tardiness.
            total_weighted_completion_time = 0
            current_time = 0
            for job_id in data["jobs"]:
                job = self.jobs[job_id]
                current_time += job.processing_time
                total_weighted_completion_time += current_time
            # Compute number of duplicates.
            number_of_duplicates = len(data["jobs"]) - len(set(data["jobs"]))
            is_feasible = (
                    (number_of_duplicates == 0))
            objective_value = profit - total_weighted_completion_time
            print(f"Profit: {profit}")
            print(f"Total weighted completion time: "
                  f"{total_weighted_completion_time}")
            print(f"Number of duplicates: {number_of_duplicates}")
            print(f"Feasible: {is_feasible}")
            print(f"Objective value: {objective_value}")
            return (is_feasible, objective_value)


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
        solution = dynamic_programming()
        if args.certificate is not None:
            data = {"jobs": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            instance.check(args.certificate)

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)
