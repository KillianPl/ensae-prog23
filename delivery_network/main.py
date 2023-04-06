
from graph import Graph
import collections as c
import bisect
import random
import numpy as np
import matplotlib.pyplot as plt
data_path = "input/"
file_name = "network.01.in"

#g = Graph.graph_from_file(data_path + file_name)
g1 = Graph.graph_from_file("input/network.00.in")
#print(g)
#graph_render(g1,path=[9,8,1,2,3,4,10])
#time_measure(graph_render(g1,path=[9,8,1,2,3,4,10]))


# def import_camion(nom_fichier):
#   fichier = open(nom_fichier,'r')
#   fligne = fichier.readline.split(" ")
#   Cam = (int(fligne[0]),[])

#   E = fichier.readlines():
#   for ligne in E:
#     ligne = ''.join(ligne.splitlines())
#     Cam[1].append([ligne[0],ligne[1]])
  
#   return Cam

# def import_route(nom_fichier): # let us have a useable format for roads
#     list_route = []

#     with open(f"input/routes.1.in") as route:
#       temps = 0
#       route.readline()
#       for path in route.readlines(): # readlines works as a generator
#         node_a, node_b, utility = map(int, path.rstrip().split(" "))
#         list_route.append([node_a,node_b,utility])

#       return list_route

# def route_synth(nom_fichier,graph): # synthetise roads as a minimal power and a cost
#     route_init = import_route(nom_fichier)
#     synth = []
#     for route in route_init:
#         min_pow = graph.min_optimised(route[0],route[1])[1]
#         synth.append([min_pow, route[2],(route[0],route[1])])
#     return synth

# def order(ilist, composante=0, type = "asc"): # default is 0 ie power
#     if not ilist[:,composante]: 
#         return ilist[:,composante] # empty sequence case

#     pivot = ilist[:,composante][random.choice(range(0, len(truck_list[:,component])))]

#     head = order([x for x in ilist if x[composante] < pivot])
#     tail = order([x for x in ilist if x[composante] > pivot])

  
#     return head + [x for x in ilist if x[composante] == pivot] + tail

# def camion_opti(truck_list, pow, utility):
#     p = utility - truck_list[0][1] ; m = 0
#     for i in range( len(truck_list)):
#         if truck_list[i][0] >= pow:
#             np = utility - truck_list[i][1]
#             if (np) > p:
#                 m = i
#                 p = np
      
#     return [m , truck_list[m], p]


# def profit(routes, truck_list, graph):  #routes au format route_synth
#   truck_list = order(truck_list)
#   profits = []
#   for route in routes:  # format : "avec camion i, on fait profit p entre a et b"
#       i, data, p = camion_opti(truck_list, route[0])
#       profits.append([i, p , route[2]])
#   return profits


# def sac_glouton(fichier_route,fichier_graph,fichier_camions):
#     budget = 25*10**9
#     graph = graph_from_file(fichier_graph)

#     truck_list = import_camion(fichier_camions)
#     truck_list = order(truck_list,0)

#     routes = route_synth(fichier_route, graph)
#     routes = order(routes, 0)

#     profits = profit(routes,truck_list,graph)
#     profits = order(profits,1)

#     commande_camions = {i : [0,[]] for i in range(len(truck_list))}

#     for camion in profit: 
#       """on parcours la liste des profits triée par ordre décroissant et on ajoute 
#       le parcours tant qu'on a le budget pour le camion"""
#         if budget == 0:
#           return commande_camions
#     if budget - camion[1]>=0:
#         commande_camions[i][0] += 1
#         commande_camions[i][1].append(camion[2])


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

    with open(f"input/trucks.{i}.in", 'r') as f:
        f.readline()
        all_trucks = {} # power:int -> cost:int
        for truck in f.readlines():
            cost, power = truck.split()
            cost, power = map(int, (cost, power))
            if power in all_trucks: #only keeping smallest cost for each power
                all_trucks[power] = min(all_trucks[power], cost)
            else:
                all_trucks[power] = cost
    
    all_trucks = list(all_trucks.items())
    # sorting in decreasing order of power
    all_trucks.sort(key=lambda x:x[0], reverse=True)
    trucks = [all_trucks[0]]
    
    previous_cost = all_trucks[0][1]
    for power, cost in all_trucks:
        #not adding trucks with stricly less power costing more
        if cost < previous_cost:
            trucks.append((power, cost))
            previous_cost = cost
    return trucks


def route_proccessing(i, trucks, filewrite=False):
    """
        Computes the cost of each route in routes.i.out and 
        outputs a list of routes with associated cost sorted by 
        utility/cost. NodeType is assumed to be int.
        
        Optionally if filewrite is True, 
        writes a file named routes.processed.i.in  with format:
            Each line is of the form 'a b power utility cost utility/cost'
            where power is that of the truck paired to the route.
            power, utility, cost are integers ; a, b are node tags.

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
            routes : list[NodeType, NodeType, int, int, int, float]
                Each tupple in the list indicates in order: the two nodes of the path,
                the power of the truck, the cost of the truck, the utility gained from the path and the ratio of utility/cost
    """
    n_trucks = len(trucks)
    routes = []
    with open(f"output/routes.{i}.out", 'r') as f:
        f.readline()
        for line in f.readlines(): # readlines is a generator
            a, b, utility, pmin = map(int, line.split(" ")) 
            # cost is the closest key, on the right
            ind = bisect.bisect_right(trucks, pmin, key= lambda x:x[0])
            if ind < n_trucks-1: # route with too great power necessary
                cost = trucks[ind][1]
                routes.append((a, b, trucks[ind][0], utility, cost, utility/cost))
    #sorting on ratio utility cost
    routes.sort(key=lambda x : x[5], reverse=True)
    if filewrite:
        processed = open(f"input/routes.processed.{i}.out", 'w')
        for a, b, pmin, utility, cost, u_c in routes:
            processed.write(f"{a} {b} {pmin} {utility} {cost} {u_c}\n")
        processed.close()
    return routes


def route_out(i):
    """
        Writes a file routes.i.out based on routes.i.in .
        The first line of routes.i.in has format 'n' where n is the number of routes in the file
        The n following lines should have format: 'Node1 Node2 utility'
            with        utility  : int
                    Node1, Node2 : Nodetype
        Output file has the same first line, and the 
        n following lines are in format 'Node1 Node2 utility power_min'
            with       power_min : int

        Parameters
        ----------------
            i : int
                number of the file to convert

        Output
        ---------
            NoneType
    """

    G = Graph.graph_from_file(f"input/network.{i}.in").kruskal()

    with open(f"input/routes.{i}.in") as f:
        output = open(f"output/routes.{i}.out", 'w')
        N = int(f.readline())
        output.write(f"{N}\n")
        for ligne in f.readlines():
            a, b, utility = ligne.split()
            power_min = int(G.min_power(int(a),int(b))[1])
            output.write(a + " " + b + " " + utility + " " + str(power_min)+"\n")
        output.close()


def simulated_annealing(trucks, routes):
    """
    Implements a simulated annealing heuristic to maximize utility.

    Parameters
    -------------
      trucks : list[(int, int)]
        List of useful trucks sorted in decreasing order of both power and cost
        Entries are tuples representing in order: (power, cost)

      routes : list[NodeType, NodeType, int, int, float]
                Each tupple in the list indicates in order: the two nodes of the path,
                the power of the associated truck, its' cost, the utility gained from the path
                 and the ratio of utility/cost. It is sorted in descending utility/cost

    Output
    -----------
      best_chosen_routes: list[NodeType, NodeType, int, int, float]
          Represents the choice of routes giving the maximum utility among 
          those explored. Each route is associated to an unique truck by its cost.
      utility: int
          The maximum utility observed during exploration
    """
    # choosing an inital point,
    # can be random or deterministic 
    # here we start from a greedy approach
    budget = 25 * 10**9
    best_chosen_routes = {}
    max_utility = 0
    min_cost = routes[-1][3]
    for path in routes:
        a, b, power, cost, utility, u_c = path
        if cost < budget:
            best_chosen_routes[path] = 1
            budget -= cost
        if budget < min_cost:
            break
        else:
            pass
    
    def utility(road_choices):
      total = 0
      for _, _, _, _, u, _ in road_choices:
        total += u
      return total    

    historique = []
    chosen_routes = best_chosen_routes.copy()
    T = 10**6 #Temperature
    K_activation = 100 # hyperparameter constant

    while T > 10**-4:
        current_u = utility(chosen_routes)
        if current_u > max_utility:
            max_utility = current_u
            best_chosen_routes = chosen_routes.copy()

        historique.append(current_u)
        # make the change in place
        r_del = random.choice(chosen_routes.keys())
        chosen_routes.pop(r_del)
        r_add = random.choice(routes)
        counter = 1
        while counter < 4 and (r_add in chosen_routes or budget - r_add[3] < 0) :
            r_add = random.choice(routes)
            counter += 1
        chosen_routes[r_add] = 1
        neighbor_u = utility(chosen_routes)
        delta_u = neighbor_u - current_u
        if delta_u > 0:
            # change is accepted
            budget -= r_add[3]
            budget += r_del[3]
        elif rand() < np.exp(K_activation * delta_u / T):
            budget -= r_add[3]
            budget += r_del[3]
        else:
            #reverse change
            chosen_routes[r_del] = 1
            chosen_routes.pop(r_add)
        T *= 0.9995

    N =len(historique)
    X = np.arrange(N)
    plt.plot(X, historique, linewidth = 1, color='blue')
    plt.plot(X, np.ones(N)*max_utility, linewidth = 1, color='red')
    font1 = {'family':'serif','color':'blue','size':20}
    font2 = {'family':'serif','color':'red','size':20}
    font2 = {'family':'serif','color':'red','size':20}
    plt.xlabel("temps", fontdict = font1)
    plt.ylabel("utility", fontdict = font2)
    plt.title("Exploration of utility levels by simulated annealing")
    plt.show()

    return best_chosen_routes, max_utility

if __name__ == '___main___':
    main()


#print(truck_from_file(1))
route_out((1))
print(route_proccessing(1, truck_from_file(1)))