import json


class Item:
    id = -1
    weight = 0
    width = 0
    profit = 0


class Instance:

    def __init__(self, filepath=None):
        self.items = []
        if filepath is not None:
            with open(filepath) as json_file:
                data = json.load(json_file)
                self.capacity = data["capacity"]
                items = zip(
                        data["item_weights"],
                        data["item_widths"],
                        data["item_profits"])
                for (weight, width, profit) in items:
                    self.add_item(weight, width, profit)

    def add_item(self, weight, width, profit):
        item = Item()
        item.id = len(self.items)
        item.weight = weight
        item.width = width
        item.profit = profit
        self.items.append(item)

    def write(self, filepath):
        data = {"capacity": self.capacity,
                "item_weights": [item.weight for item in self.items],
                "item_widths": [item.width for item in self.items],
                "item_profits": [item.profit for item in self.items]}
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file)

    def check(self, filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            profit = sum(self.items[item_id].profit
                         for item_id in data["items"])
            weight = sum(self.items[item_id].weight
                         for item_id in data["items"])
            width = max((self.items[item_id].width
                         for item_id in data["items"]),
                        default=0)
            number_of_duplicates = len(data["items"]) - len(set(data["items"]))
            is_feasible = (
                    (number_of_duplicates == 0)
                    and (weight <= self.capacity))
            objective_value = profit - width
            print(f"Profit: {profit}")
            print(f"Weight: {weight} / {self.capacity}")
            print(f"Width: {width}")
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
            data = {"items": solution}
            with open(args.certificate, 'w') as json_file:
                json.dump(data, json_file)
            instance.check(args.certificate)

    elif args.algorithm == "checker":
        instance = Instance(args.instance)
        instance.check(args.certificate)
