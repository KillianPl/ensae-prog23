# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph

import unittest   # The test framework

class Test_Kruskal(unittest.TestCase):
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        K = g.kruskal()

if __name__ == '__main__':
    unittest.main()
