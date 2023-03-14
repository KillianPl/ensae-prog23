import sys 
sys.path.append("delivery_network")

from time import perf_counter
import unittest 
from graph import Graph

class Test_ExecutionTime(unittest.TestCase):
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        s = perf_counter()
        for _ in range(100_000):
            g.min_power(1, 4)
        e = perf_counter()
        print(f"Function or method min_power took {e-s:.4f} seconds to run a 100 000 times on the graph from network.00 ")

    def test_network0(self):
        g = Graph.graph_from_file("input/network.10.in")
        s = perf_counter()
        g.min_power(1, 1800)
        e = perf_counter()
        print(f"Function or method min_power took {e-s:.4f} seconds to run on graph from network.00 ")

if __name__ == '__main__':
    unittest.main()