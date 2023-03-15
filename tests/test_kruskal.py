# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph
from time import perf_counter
import unittest   # The test framework

#kruskal works but is too slow
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
        

if __name__ == '__main__':
    unittest.main()
