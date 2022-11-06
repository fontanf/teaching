#######################
# Dynamic Programming #
#######################

from itertools import chain


##############
# Subset sum #
##############


def subsetsum(weights, capacity):
    """Given a set of integers 'weights' and an integer 'capacity', return True
    if there exists a subset of 'weights' that sums to 'capacity', False
    otherwise.

        :Example:

        >>> subsetsum([8,12,5,3,6,9], 20)
        True
        >>> subsetsum([8,12,5,3,6,9], 33)
        False
        >>> subsetsum([1,5,3], 7)
        False
        >>> subsetsum([1,2,4,3,12], 13)
        True
        >>> subsetsum([1,3,5], 5)
        True
        >>> subsetsum([1,5,2,3,2], 8)
        True
        >>> subsetsum([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 15)
        True
        >>> subsetsum([1,1,1,1,1,1,1,1,1,1,1,1,1,1], 15)
        False
        >>> subsetsum([4,8,12,6,14], 19)
        False
        >>> subsetsum([0], 1)
        False
        >>> subsetsum([2], 1)
        False

    """

    # TODO START (9 line(s))

    # TODO END


############
# Knapsack #
############


def knapsack_checker(weights, profits, capacity, solution):
    # Check duplicates.
    if len(solution) != len(set(solution)):
        return -1
    # Check capacity.
    if sum(weights[item_id] for item_id in solution) > capacity:
        return -1
    # Return solution value.
    return sum(profits[j] for j in solution)


def knapsack(weights, profits, capacity):
    """Given a set of items with integer weights 'weights' and integer profits
    'profits' and an integer capacity 'capacity', return a subset of items of
    total weight lesser than 'capacity' that maximizes the sum of the profits
    of the included items.

        The recursion is already written. You only need to implement the
        backtracking step. The function should return a list of item INDICES.
        For example, for the first example, a possible optimal solution is
        [2, 3]

        :Example:

        >>> weights = [3, 7, 4, 5]
        >>> profits = [2, 6, 3, 4]
        >>> capacity = 9
        >>> solution = knapsack(weights, profits, capacity)
        >>> knapsack_checker(weights, profits, capacity, solution)
        7

        >>> weights = [2, 6, 3, 4]
        >>> profits = [3, 7, 4, 5]
        >>> capacity = 9
        >>> solution = knapsack(weights, profits, capacity)
        >>> knapsack_checker(weights, profits, capacity, solution)
        12

        >>> weights = [10, 10, 10, 9,  9,  9,  9]
        >>> profits = [11, 11, 11, 10, 10, 10, 10]
        >>> capacity = 36
        >>> solution = knapsack(weights, profits, capacity)
        >>> knapsack_checker(weights, profits, capacity, solution)
        40

        >>> weights = [3,  4]
        >>> profits = [10, 9]
        >>> capacity = 6
        >>> solution = knapsack(weights, profits, capacity)
        >>> knapsack_checker(weights, profits, capacity, solution)
        10

        >>> weights = [1]
        >>> profits = [1]
        >>> capacity = 1
        >>> solution = knapsack(weights, profits, capacity)
        >>> knapsack_checker(weights, profits, capacity, solution)
        1

    """

    n = len(weights)
    t = [[0 for x in range(capacity + 1)] for y in range(n + 1)]
    for j in range(1, n + 1):
        for x in range(0, weights[j - 1]):
            t[j][x] = t[j - 1][x]
        for x in range(weights[j - 1], capacity + 1):
            t[j][x] = max(t[j - 1][x],
                          t[j - 1][x - weights[j - 1]] + profits[j - 1])

    solution = []

    # TODO START (5 line(s))

    # TODO END

    return solution


##################
# Load balancing #
##################


def loadbalancing_checker(processing_times, solution):
    # Check solution size.
    if len(solution) != 2:
        return -1
    # Check duplicates.
    n = len(solution[0]) + len(solution[1])
    if n != len(set(solution[0] + solution[1])):
        return -1
    # Check that all orders are assigned.
    if n != len(processing_times):
        return -1
    # Compute latest finishing time
    return max(sum(processing_times[j] for j in line) for line in solution)


def loadbalancing(processing_times):
    """Orders must be assigned to two production lines. Each order i takes the
    same amount of processing time processing_times[i] on each line. The goal
    is to assign all the orders so that the total workload is balanced between
    the two lines. In other words, we must minimize the latest finishing time
    of the two lines.

        This problem is equivalent to the optimization version of the subset
        sum problem (what is the maximum weight of a subset of items not
        exceeding c), with a capacity c = sum(processing_times) / 2. You can
        use the same recursion as in the subset sum exercise.
        Then, you also need to implement the backtracking step as in the
        knapsack exercise.

        Return a list of two lists corresponding to the list of order INDICES
        for each machine.
        For example, for processing_times = [4, 10, 7, 5, 3], a possible
        optimal solution is [[0, 1], [2, 3, 4]]

        :Example:

        >>> processing_times = [4,10,7,5,3]
        >>> solution = loadbalancing(processing_times)
        >>> loadbalancing_checker(processing_times, solution)
        15

        >>> processing_times = [4,4,4,4,4]
        >>> solution = loadbalancing(processing_times)
        >>> loadbalancing_checker(processing_times, solution)
        12

        >>> processing_times = [
        ...     462,220,256,401,273,34,398,375,
        ...     101,72,145,214,382,338,147,298,
        ...     497,472,47,56]
        >>> solution = loadbalancing(processing_times)
        >>> loadbalancing_checker(processing_times, solution)
        2594

        >>> processing_times = [
        ...     1243,40,1115,231,993,621,216,1552,
        ...     773,460,1330,207,672,51,733,287,
        ...     56,111,1362,256,792,1,770,1028,
        ...     737,183,811,838,592,600,1201,323,
        ...     913,1394,453,1043,198,475,656,94]
        >>> solution = loadbalancing(processing_times)
        >>> loadbalancing_checker(processing_times, solution)
        12706

    """

    n = len(processing_times)
    capacity = sum(processing_times) // 2

    # TODO START (19 line(s))

    # TODO END


##########
# Hotels #
##########


def hotels(d):
    """You are going on a long trip. You start on the road at mile post 0.
    Along the way there are n hotels, at mile posts d[1] < d[2] < · · · < d[n],
    where each d[i] is measured from the starting point.  The only places you
    are allowed to stop are at these hotels, but you can choose which of the
    hotels you stop at.  You must stop at the final hotel (at distance d[n]),
    which is your destination.  You’d ideally like to travel 200 miles a day,
    but this may not be possible (depending on the spacing of the hotels).  If
    you travel x miles during a day, the penalty for that day is (200 − x)^2.
    You want to plan your trip so as to minimize the total penalty that is, the
    sum, over all travel days, of the daily penalties.

        d is modeled by a table of integers.
        Ex: d = [0,190,320,360,470,500] means we have 5 hotels with d[1] = 190,
        d[2] = 320, ..., d[5] = 500
        The optimal stops are <1,3> for a penalty of 4600

        Return the penalty of the optimal trip

        :Example:

        >>> hotels([0,190,320,360,470,500])
        4600
        >>> hotels([
        ...     0,180,310,350,460,490,644,720,
        ...     790,810,835,890,940,1030,1090,1190])
        8700
        >>> hotels([
        ...     0,10,170,180,290,310,350,450,
        ...     460,490,500,644,654,720,790,792,
        ...     810,811,835,837,890,899,940,941,
        ...     1030,1031,1090,1092,1190,1212])
        5758
        >>> hotels([0,100,150,190,240,260,320,360,450,470,500])
        3800
        >>> hotels([0,500])
        90000
        >>> hotels([0,100,200,300,400,500,600])
        0

    """

    # TODO START (4 line(s))

    # TODO END


#################
# Cutting cloth #
#################


def cuttingcloth(x, y, a, b, c):
    """You are given a rectangular piece of cloth with dimensions x×y, where x
    and y are positive integers, and a list of n products that can be made
    using the cloth. For each product i ∈ [1, n] you know that a rectangle of
    cloth of dimensions a[i]×b[i] is needed and that the final selling price of
    the product is c[i].  Assume the a[i], b[i], and c[i] are all positive
    integers.  You have a machine that can cut any rectangular piece of cloth
    into two pieces either horizontally or vertically.  Design an algorithm
    that determines the best return on the x×y piece of cloth, that is, a
    strategy for cutting the cloth so that the products made from the resulting
    pieces give the maximum sum of selling prices.  You are free to make as
    many copies of a given product as you wish, or none if desired.

        Return the maximum revenue you can get from the x×y piece of the cloth
        and the n products.

        :Example:

        >>> cuttingcloth(4,4,[2,3],[2,3],[1,1])
        4
        >>> cuttingcloth(4,4,[3,2,1],[3,2,1],[3,2,1])
        16
        >>> cuttingcloth(30,30,[3,2,1],[3,2,1],[7,3,1])
        900
        >>> cuttingcloth(30,30,[3,2,1],[3,2,1],[11,5,1])
        1125
        >>> cuttingcloth(50,50,[7,5],[5,7],[1,1])
        71
        >>> cuttingcloth(50,50,[4,7,9,2],[5,3,2,11],[40,44,32,48])
        5416
        >>> cuttingcloth(1,1,[],[],[])
        0
        >>> cuttingcloth(1,1,[2],[2],[1])
        0

    """

    # TODO START (11 line(s))

    # TODO END


if __name__ == "__main__":
    import doctest
    fonctions = [
            subsetsum,
            knapsack,
            loadbalancing,
            hotels,
            cuttingcloth,
    ]
    for f in fonctions:
        print("*" * 79)
        print(f.__name__)
        doctest.run_docstring_examples(
                f, globals(), optionflags=doctest.FAIL_FAST)
