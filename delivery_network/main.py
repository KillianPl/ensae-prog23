
from graph import Graph, graph_render, time_measure
import collections as c
import bisect


data_path = "input/"
file_name = "network.01.in"

#g = Graph.graph_from_file(data_path + file_name)
g1 = Graph.graph_from_file("input/network.00.in")
#print(g)
#graph_render(g1,path=[9,8,1,2,3,4,10])
time_measure(graph_render(g1,path=[9,8,1,2,3,4,10]))

def route_proccessing(i):
    """
        Computes the cost of each route in routes.i.out and 
        writes a file named routes.processed.i.in  with format:
            The first line is the number of routes.
            Each following line is of the form 'utility cost'
            where utility and cost are integers.

        Parameters: 
        -----------
            i: int
                The number of the truck file

        Outputs: 
        -----------
            Nonetype
    """
    #putting all trucks in a dictionary
    with open(f"input/trucks.{i}.in", 'r'):
        readline()
        trucks = c.OrderedDict() # format : power:int -> cost:int

        for truck in readlines():
            cost, power = map(int, truck)
            trucks[power] = cost
    #if one truck is less efficient than another, we may not add it
    # i.e. if a truck with greater power costs less, we only keep this one

    #idea to solve the problem : 
    #iterating through the keys in decreasing order (of power)
    # if the cost is more than that of the previous route
    # we remove the truck from the dictionary
    keys = list(trucks.keys()).sorted()
    cost = trucks[keys[-1]]
    for power in reversed(keys):
        if trucks[power] > cost:
            trucks.popitem(power)
        else:
            cost = trucks[power]

    with open(f"input/routes.{i}.out", 'r'):
        processed = open(f"input/routes.processed.{i}.out", 'w')
        readline()
        for _, _, utility, pmin in readlines():
            # computing the cost of the path
            # bisect is the reason we use an ordered dictionary
            ind_right = bisect.bisect_right(keys, pmin) 
            cost = truck[ind_right]
            #writing down the result
            processed.write(f"{utility} {cost}\n")
        processed.close()



def recuit_simule():
    







if __name__ == '___main___':
    main()