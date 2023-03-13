import sys 
sys.path.append("delivery_network")

from graph import Graph

if __name__ == '__main__':
    g1 = Graph.graph_from_file("input/network.00.in")
    g2 = Graph.graph_from_file("input/network.02.in")
    print(g1.min_power(1, 4))
