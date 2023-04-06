import sys 
sys.path.append("delivery_network")
sys.setrecursionlimit(1_000_000)

from time import perf_counter
import unittest 
from graph import Graph

class Test_ExecutionTime(unittest.TestCase):

    def test_temps_routes2(self):
        i = 2
        g = Graph.graph_from_file(f"input/network.{i}.in")
        g = g.kruskal()
        with open(f"input/routes.{i}.in", 'r') as route:
            N = int(route.readline())
            duration = 0
            k = 1
            for _ in range(k):
                ligne = route.readline().split(" ")
                node_a, node_b, utility = map(int, ligne)
                start = perf_counter()
                g.min_power_optimized(node_a, node_b)
                end = perf_counter()
                duration += (end-start)
            duration = duration/60
            print(f"It would take roughly {(N/k)*duration:.4f} mins to compute min_power for all paths from network.{i}, (N={N})")


if __name__ == '__main__':
    unittest.main()