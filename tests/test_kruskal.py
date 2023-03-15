import sys 
sys.path.append("delivery_network")
sys.setrecursionlimit(1_000_000)

from time import perf_counter
import unittest 
from graph import Graph


class Test_Kruskal(unittest.TestCase):
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        K = g.kruskal()
        for n in K.nodes: 
            if K.graph[n] != g.graph[n]:
                self.assertFalse
        self.assertTrue

    def test_network1(self):
        g = Graph.graph_from_file("input/network.01.in")
        K = g.kruskal()
        for n in K.nodes:
            if K.graph[n] != g.graph[n]:
                self.assertFalse
        self.assertTrue
    
    def test_efficiency(self):
        start = perf_counter()
        g = Graph.graph_from_file("input/network.10.in")
        end = perf_counter()
        print(f"L'implémentation de l'algorithme de Kruskal prend {end - start:4f} sur le graph de network.10.in.")



if __name__ == '__main__':
    unittest.main()
