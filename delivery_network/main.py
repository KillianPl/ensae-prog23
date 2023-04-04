
from graph import Graph, graph_render, time_measure

data_path = "input/"
file_name = "network.01.in"

#g = Graph.graph_from_file(data_path + file_name)
g1 = Graph.graph_from_file("input/network.00.in")
#print(g)

#graph_render(g1,path=[9,8,1,2,3,4,10])
time_measure(graph_render(g1,path=[9,8,1,2,3,4,10]))

def calcul_utilite(graphe, route):
    return None


def recuit_simule():
    #choix initial random
    return None 






if __name__ == """main""":
    main()