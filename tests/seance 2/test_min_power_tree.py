import sys 
sys.path.append("delivery_network")
sys.setrecursionlimit(1_000_000)

from time import perf_counter
import unittest 
from graph import Graph

class Test_ExecutionTime(unittest.TestCase):

    def test_network10(self):
        g = Graph.graph_from_file("input/network.1.in").kruskal()
        start = perf_counter()
        g.min_power_tree(1, 20)
        end = perf_counter()
        print(f"Function min_power took {end-start:.4f} seconds to run on graph from network.1 ")

    def test_temps_routes1(self):
        g = Graph.graph_from_file(f"input/network.1.in").kruskal()
        with open(f"input/routes.1.in") as route:
            temps = 0
            route.readline()
            for path in route.readlines(): # readlines works as a generator
                node_a, node_b, utility = map(int, path.rstrip().split(" "))
                start = perf_counter()
                g.min_power_tree(node_a, node_b)
                end = perf_counter()
                temps += (end - start)
            print(f"It takes roughly {temps:.4f} seconds to compute min_power for all paths from routes.1.in (smaller graph) ")
            route.close()

    def test_temps_routes2(self):
        i=3
        g = Graph.graph_from_file(f"input/network.{i}.in").kruskal()
        route = open(f"input/routes.{i}.in", 'r')
        N = int(route.readline().rstrip())
        temps = 0
        for _ in range(5):
            node_a, node_b, utility = map(int, route.readline().split(" "))
            start = perf_counter()
            g.min_power_tree(node_a, node_b)
            end = perf_counter()
        duration = (end-start)/60
        print(f"It would take roughly {N/5*duration:.4f} mins to compute min_power for all paths from network.{i}, (N={N})") 
        route.close()


if __name__ == '__main__':
    unittest.main()