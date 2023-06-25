import unittest
from Dijkstra import dijkstra, reconstruct_shortest_path
import networkx

class DijkstraTestCase(unittest.TestCase):
    def test_Dijkstra(self):
        # Create a graph for testing
        graph = networkx.Graph()
        graph.add_edge('A', 'B', weight=1)
        graph.add_edge('B', 'C', weight=3)
        graph.add_edge('C', 'D', weight=5)

        # Define the start and end coordinates
        start_coordinates = 'A'
        end_coordinates = 'D'

        shortest_path = dijkstra(graph, start_coordinates, end_coordinates)

        #expected result
        expected_path = ['A', 'B', 'C', 'D']
        self.assertEqual(shortest_path, expected_path)

class ReconstructShortestPathTestCase(unittest.TestCase):
    def test_ReconstructShortestPath(self):
        visited = {'A': None, 'B': 'A', 'C': 'B', 'D': 'C'}
        start_coordinates = 'A'
        end_coordinates = 'D'

        shortest_path = reconstruct_shortest_path(visited, start_coordinates, end_coordinates)

        expected_path = ['A', 'B', 'C', 'D']
        self.assertEqual(shortest_path, expected_path)

if __name__ == '__main__':
    unittest.main()