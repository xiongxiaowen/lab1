import unittest
from Dijkstra import dijkstra
import networkx

class DijkstraTestCase(unittest.TestCase):
    def test_Dijkstra(self):
        # Create a graph for testing
        graph = networkx.Graph()
        graph.add_edge('A', 'B', weight=1)
        graph.add_edge('B', 'C', weight=2)
        graph.add_edge('C', 'D', weight=3)

        # Define the start and end coordinates
        start_coordinates = 'A'
        end_coordinates = 'D'

        shortest_path = dijkstra(graph, start_coordinates, end_coordinates)

        #expected result
        expected_path = ['A', 'B', 'C', 'D']
        self.assertEqual(shortest_path, expected_path)

if __name__ == '__main__':
    unittest.main()