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
        N = 100_000
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

    def test_temps(self):
        for i in range(4):
            g = Graph.graph_from_file(f"input/network.0{i}.in")
            V = g.nb_nodes
            start = perf_counter()
            g.min_power(1, g.nodes[-1])
            end = perf_counter()
            print(f"It would take roughly {(V*(V-1)//2)*(end-start):.4f} seconds to compute min_power for all paths from network.0{i} ") # number of choices of 2 nodes among V is V*(V-1)//2

        for i in range(4, 11):
            g = Graph.graph_from_file(f"input/network.{i}.in")
            V = g.nb_nodes
            start = perf_counter()
            g.min_power(1, g.nodes[-1])
            end = perf_counter()
            duration = (end-start)/60/60/24/365
            print(f"It would take roughly {int((V*(V-1)//2)*duration)} years to compute min_power for all paths from network.{i} (larger graph)") 
        
if __name__ == '__main__':
    unittest.main()