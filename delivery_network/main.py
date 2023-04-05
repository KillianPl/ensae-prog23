
from graph import Graph, graph_render, time_measure
import collections as c
import bisect
import random as rd

data_path = "input/"
file_name = "network.01.in"

#g = Graph.graph_from_file(data_path + file_name)
g1 = Graph.graph_from_file("input/network.00.in")
#print(g)
#graph_render(g1,path=[9,8,1,2,3,4,10])
time_measure(graph_render(g1,path=[9,8,1,2,3,4,10]))

def truck_from_file(i):
    """
    Reads a text file containing truck information 
    and returns a list containing all useful trucks, sorted
    in decreasing order of both power and cost.
    The file should have the following format: 
        The first line of the file is 'n' the number of trucks
        The next n lines have 'power cost'
        All values are integers.

    Parameters:
    ------------
        i : int
            Number of the truck file

    Output:
    ----------
    trucks[cost, power] : list[int, int]
    
    with
        cost : int
            The cost of the truck
        power: int
            The power of the truck
    The list is sorted in decreasing order of both power and cost.
    """

    with open(f"input/trucks.{i}.in", 'r'):
        readline()
        all_trucks = {} # power:int -> cost:int
        for truck in readlines():
            cost, power = map(int, truck)
            if power in all_trucks: #only keeping smallest cost for each power
                all_trucks[power] = min(all_trucks[power], cost)
            else:
                all_trucks[power] = cost
    
    all_trucks = list(all_trucks.items())
    # sorting in decreasing order of power
    all_trucks.sort(key=lambda x:x[0], reverse=True)
    trucks = [all_trucks[0]]
    
    previous_cost = all_trucks[0][1]
    for power, cost in reversed(all_trucks):
        #not adding trucks with stricly less power costing more
        if cost < previous_cost:
            trucks.append(power, cost) 
            previous_cost = cost
    return trucks


def route_proccessing(i, trucks, filewrite=False):
    """
        Computes the cost of each route in routes.i.out and 
        outputs a list of routes with associated cost sorted by 
        utility/cost. NodeType is assumed to be int.
        
        Optionally if filewrite is True, 
        writes a file named routes.processed.i.in  with format:
            Each line is of the form 'a b powermin utility cost utility/cost'
            where powermin, utility, cost are integers
            and a, b are node tags.

        Parameters: 
        -----------
            i: int
                The number of the truck file
            filewrite: bool
                indicates if a file containing the result is written
            trucks : list[(int, int)]
                Entries represent the couple (power, cost) for a truck

        Outputs: 
        -----------
            routes : list[NodeType, NodeType, int, int, float]
                Each tupple in the list indicates in order: the two nodes of the path,
                the minimal power necessary, the utility gained from it and the ratio of
                utility/cost
    """
    n_trucks = len(trucks)
    routes = []
    with open(f"input/routes.{i}.out", 'r'):
        readline()
        for line in readlines(): # readlines is a generator
            a, b, utility, pmin = map(int, line.split(" ").rstrip()) 
            # cost is the closest key, on the right
            ind = bisect.bisect_right(trucks, pmin)
            if ind < n_trucks-1: # route with too great power necessary
                cost = trucks[ind][1]
                routes.append(a, b, pmin, utility, cost, utility/cost)
    #sorting on ratio utility cost
    routes.sort(key=lambda x : x[5])
    if filewrite:
        processed = open(f"input/routes.processed.{i}.out", 'w')
        for a, b, pmin, utility, cost, u_c in routes:
            processed.write(f"{a} {b} {pmin} {utility} {cost} {u_c}\n")
        processed.close()
    return routes


def simulated_annealing(i, trucks, routes):
    """
    cf explication
    """


    budget = 25 * 10**9
    while budget > min_cost:
    





if __name__ == '___main___':
    main()