import sys 
sys.path.append("delivery_network")
sys.setrecursionlimit(1_000_000)

from time import perf_counter
import unittest 
from graph import Graph

class Test_ExecutionTime(unittest.TestCase):
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        start = perf_counter()
        N = 100
        for _ in range(N):
            g.min_power(1, 4)
        end = perf_counter()
        print(f"Function min_power took {end-start:.4f} seconds to run {N} times on the graph from network.00 ")

    def test_network10(self):
        g = Graph.graph_from_file("input/network.10.in")
        start = perf_counter()
        g.min_power(1, 1800)
        end = perf_counter()
        print(f"Function min_power took {end-start:.4f} seconds to run on graph from network.10 ")

    def test_temps_routes1(self):
        #smaller graphs, less routes
        g = Graph.graph_from_file(f"input/network.1.in")
        with open(f"input/routes.1.in") as route:
            start = perf_counter()
            route.readline()
            for path in route.readlines(): # readlines works as a generator
                node_a, node_b, utility = map(int, path.rstrip().split(" "))
                g.min_power(node_a, node_b)
            end = perf_counter()
            print(f"It takes roughly {(end-start):.4f} seconds to compute min_power for all paths from routes.1.in ")

    def test_temps_routes2(self):
        for i in range(2, 11):
            g = Graph.graph_from_file(f"input/network.{i}.in")
            route = open(f"input/routes.{i}.in", 'r')
            N = int(route.readline().rstrip())
            start = perf_counter()
            for _ in range(5):
                node_a, node_b, utility = map(int, route.readline().split(" "))
                g.min_power(node_a, node_b)
            # probleme ici car pour i = 3 le code n'est pas interprété jusqu'ici
            # faire un autre test ne marche pas, il y a un pb avec la taille ?
            # erreur code=null
            end = perf_counter()
            duration = (end-start)/60/60
            print(f"It would take roughly {(N//5)*duration} hours to compute min_power for all paths from network.{i} (larger graph)") 
            route.close()
        
if __name__ == '__main__':
    unittest.main()