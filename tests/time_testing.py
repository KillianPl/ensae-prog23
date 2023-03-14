import sys 
sys.path.append("delivery_network")

from time import perf_counter
import unittest 
from graph import Graph

class Test_ExecutionTime(unittest.TestCase):
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        s = perf_counter()
        for _ in range(1_000_000):
            g.get_path_with_power(1, 4, 11)
        e = perf_counter()
        print(f"Function or method get_path_with_power took {e-s:.4f} seconds to run a million times on the graph from network.00 ")

if __name__ == '__main__':
    unittest.main()