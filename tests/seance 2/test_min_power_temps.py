import sys 
sys.path.append("delivery_network")
sys.setrecursionlimit(1_000_000)

from time import perf_counter
import unittest 
from graph import Graph

class Test_ExecutionTime(unittest.TestCase):

    def test_temps_routes2(self):
            g = Graph.graph_from_file(f"input/network.{2}.in")
            g = g.kruskal()
            with open(f"input/routes.{2}.in", 'r') as route:
                route.readline()
                duration = 0
                for _ in range(5):
                    ligne = route.readline()
                    ligne.split(" ")
                    print(ligne)
                    node_a, node_b, utility = map(int, ligne)
                    start = perf_counter()
                    g.min_power_tree(node_a, node_b)
                    end = perf_counter()
                    duration += (end-start)
                duration = duration/60
                print(f"It would take roughly {N/5*duration:.4f} mins to compute min_power for all paths from network.{2}, (N={N})")


if __name__ == '__main__':
    unittest.main()