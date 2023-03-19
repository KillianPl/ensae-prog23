# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network/")

import unittest 
from graph import Graph

class Test_GraphLoading(unittest.TestCase):
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 9)

    def test_network1(self):
        g = Graph.graph_from_file("input/network.01.in")
        self.assertEqual(g.nb_nodes, 7)
        self.assertEqual(g.nb_edges, 5)
    
    def test_network4(self):
        g = Graph.graph_from_file("input/network.04.in")
        self.assertEqual(g.nb_nodes, 10)
        self.assertEqual(g.nb_edges, 4)
        print(g.graph)
        self.assertEqual(g.graph[1][0][2], 6)

    def test_network10(self):
        g = Graph.graph_from_file("input/network.10.in")
        
if __name__ == '__main__':
    unittest.main()
