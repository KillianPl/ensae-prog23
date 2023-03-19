# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph

import unittest   # The test framework

class Test_min_distance(unittest.TestCase): # TEST DE LA QUESTION 5
    def test_network0(self):
        g = Graph.graph_from_file("input/network.00.in")
        self.assertEqual(g.get_optimal_path_with_power(1, 4, 11), [1, 2, 3, 4])
        self.assertEqual(g.get_optimal_path_with_power(1, 4, 10), None)

if __name__ == '__main__':
    unittest.main()
