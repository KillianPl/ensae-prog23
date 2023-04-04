
from graph import Graph, graph_render, time_measure

data_path = "input/"
file_name = "network.01.in"

#g = Graph.graph_from_file(data_path + file_name)
g1 = Graph.graph_from_file("input/network.00.in")
#print(g)

#graph_render(g1,path=[9,8,1,2,3,4,10])
time_measure(graph_render(g1,path=[9,8,1,2,3,4,10]))


def import_camion(nom_fichier):
  fichier = open(nom_fichier,'r')
  fligne = fichier.readline.split(" ")
  Cam = (int(fligne[0]),[])

  E = fichier.readlines():
  for ligne in E:
    ligne = ''.join(ligne.splitlines())
    Cam[1].append([ligne[0],ligne[1]])
  
  return Cam


def import_route(nom_fichier): # let us have a useable format for roads
  list_route = []

  with open(f"input/routes.1.in") as route:
    temps = 0
    route.readline()
    for path in route.readlines(): # readlines works as a generator
      node_a, node_b, utility = map(int, path.rstrip().split(" "))
      list_route.append([node_a,node_b,utility])

    return list_route

def route_synth(nom_fichier,graph): # synthetise roads as a minimal power and a cost
  route_init = import_route(nom_fichier)
  synth = []
  for route in route_init:
    min_pow = graph.min_optimised(route[0],route[1])[1]
    synth.append([min_pow, route[2],((route[0],route[1])])
  
  return synth

def order(ilist, composante=0, type = "asc"): # default is 0 ie power
  if not ilist[:,composante]: 
    return ilist[:,composante] # empty sequence case

  pivot = ilist[:,composante][random.choice(range(0, len(truck_list[:,component])))]

  head = order([x for x in ilist if x[composante] < pivot])
  tail = order([x for x in ilist if x[composante] > pivot])

  
  return head + [x for x in ilist if x[composante] == pivot] + tail

def camion_opti(truck_list, pow, utility):
  p = utility - truck_list[0][1] ; m = 0
  for i in range( len(truck_list)):
    if truck_list[i][0] >= pow:
      np = utility - truck_list[i][1]
      if (np) > p:
        m = i
        p = np
    
    return [m , truck_list[m], p]


def profit(routes, truck_list, graph):  #routes au format route_synth
  truck_list = order(truck_list)
  profits = []
  for route in routes:  # format : "avec camion i, on fait profit p entre a et b"
    i, data, p = camion_opti(truck_list, route[0])
    profits.append([i, p , route[2]])
  
  return profits


def sac_glouton(fichier_route,fichier_graph,fichier_camions):
  budget = 25*10**9

  graph = graph_from_file(fichier_graph)

  truck_list = import_camion(fichier_camions)
  truck_list = order(truck_list,0)

  routes = route_synth(fichier_route, graph)
  routes = order(routes, 0)

  profits = profit(routes,truck_list,graph)
  profits = order(profits,1)

  commande_camions = {i : [0,[]] for i in range(len(truck_list))}

  for camion in profit: 
    """on parcours la liste des profits triée par ordre décroissant et on ajoute 
    le parcours tant qu'on a le budget pour le camion"""

    if budget == 0:
      return commande_camions

    if budget - camion[1]>=0:
      commande_camions[i][0] += 1
      commande_camions[i][1].append(camion[2])
