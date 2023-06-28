import unittest
from IDA_star import heuristic, search, ida_star, reconstruct_shortest_path
import networkx

class HeuristicTestCase(unittest.TestCase):
    def test_heuristic(self):
        start_coordinates = (0, 0)
        end_coordinates = (3, 4)
        expected_distance = 5.0
        distance = heuristic(start_coordinates, end_coordinates)
        self.assertEqual(distance, expected_distance)

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = networkx.Graph()
        self.graph.add_edge("A", "B", weight=1)
        self.graph.add_edge("A", "C", weight=2)
        self.graph.add_edge("B", "D", weight=3)
        self.graph.add_edge("C", "D", weight=1)
        self.graph.add_edge("C", "E", weight=1)
        self.graph.add_edge("E", "D", weight=2)

    def test_search_found(self):
        # Coordinates for Helsinki Railway Station
        current_coordinates = (60.1709, 24.941)
        g = 0
        bound = 5
        # Coordinates for Helsinki Cathedral
        end_coordinates = (60.1756, 24.9335)
        result = search(current_coordinates, g, bound, end_coordinates, self.graph)
        self.assertEqual(result, "FOUND")

    def test_search_not_found(self):
        # Coordinates for Helsinki Railway Station
        current_coordinates = (60.1709, 24.941)
        g = 0
        bound = 2
        # Coordinates for Kaisaniemi Park
        end_coordinates = (60.165, 24.9505)
        result = search(current_coordinates, g, bound, end_coordinates, self.graph)
        self.assertEqual(result, float("inf"))

    def test_search_sorting_neighbors(self):
        current_coordinates = "A"
        g = 0
        bound = float("inf")
        end_coordinates = "D"
        result = search(current_coordinates, g, bound, end_coordinates, self.graph)
        # Check if the neighbors are sorted based on the combined cost
        # of the path from the start node and the heuristic estimate
        expected_neighbors = ["C", "B"]
        self.assertEqual(result, expected_neighbors)

    def test_search_multiple_paths(self):
        current_coordinates = "A"
        g = 0
        bound = float("inf")
        end_coordinates = "D"
        distances = {"A": 0, "B": float("inf"), "C": float("inf"), "D": float("inf")}
        visited = {"A": None, "B": None, "C": None, "D": None}
        result = search(current_coordinates, g, bound, end_coordinates, self.graph, distances, visited)

        # Check if the shortest path is found among multiple possible paths
        expected_path = [
            ["A", "B", "D"],
            ["A", "C", "D"],
        ]
        self.assertEqual(result, expected_path)


    def test_search_explore_neighbors(self):
        # Create a graph with multiple neighbors
        graph = networkx.Graph()
        graph.add_edge("A", "B", weight=2)
        graph.add_edge("A", "C", weight=1)
        graph.add_edge("A", "D", weight=3)

        current_coordinates = "A"
        g = 0
        bound = float("inf")
        end_coordinates = "D"
        distances = {"A": 0, "B": float("inf"), "C": float("inf"), "D": float("inf")}
        visited = {"A": None, "B": None, "C": None, "D": None}
        result = search(current_coordinates, g, bound, end_coordinates, graph, distances, visited)

        # Check if the distances and visited nodes are updated correctly
        expected_distances = {"A": 0, "B": 2, "C": 1, "D": 3}
        expected_visited = {"A": None, "B": "A", "C": "A", "D": "A"}
        self.assertEqual(distances, expected_distances)
        self.assertEqual(visited, expected_visited)

        # Check if the minimum cost is updated correctly
        expected_min_cost = float("inf")
        self.assertEqual(result, expected_min_cost)

    def test_search_cost_found(self):
        graph = networkx.Graph()
        current_coordinates = "A"
        g = 0
        bound = float("inf")
        end_coordinates = "D"
        distances = {"A": 0, "B": float("inf"), "C": float("inf"), "D": float("inf")}
        visited = {"A": None, "B": None, "C": None, "D": None}
        result = search(current_coordinates, g, bound, end_coordinates, graph, distances, visited)
        # Check if "FOUND" is returned when the goal is reached
        expected_result = "FOUND"
        self.assertEqual(result, expected_result)

    def test_search_min_cost(self):
        graph = networkx.Graph()
        graph.add_edge("A", "B", weight=1)
        graph.add_edge("B", "C", weight=2)
        graph.add_edge("C", "D", weight=3)

        current_coordinates = "A"
        g = 0
        bound = float("inf")
        end_coordinates = "D"
        distances = {"A": 0, "B": float("inf"), "C": float("inf"), "D": float("inf")}
        visited = {"A": None, "B": None, "C": None, "D": None}
        result = search(current_coordinates, g, bound, end_coordinates, graph, distances, visited)

        # Check if the minimum cost is calculated correctly
        expected_min_cost = 6
        self.assertEqual(result, expected_min_cost)


class IDAStarTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = networkx.Graph()
        self.graph.add_edge((0, 0), (1, 1), weight=1)
        self.graph.add_edge((1, 1), (2, 2), weight=2)
        self.graph.add_edge((2, 2), (3, 3), weight=3)

    def test_ida_star(self):
        # Test case1: Basic test case with a simple graph
        graph = networkx.Graph()
        graph.add_edge('A', 'B', weight=2)
        graph.add_edge('B', 'C', weight=3)
        graph.add_edge('C', 'D', weight=4)

        start_coordinates = 'A'
        end_coordinates = 'D'

        shortest_path = ida_star(graph, start_coordinates, end_coordinates)
        expected_path = ['A', 'B', 'C', 'D']
        self.assertEqual(shortest_path, expected_path, f"Test case 1 failed. Expected: {expected_path}, Got: {shortest_path}")

        # Test case2: No path exists between start and end coordinates
        graph = networkx.Graph()
        graph.add_edge('A', 'B', weight=2)
        graph.add_edge('C', 'D', weight=4)

        start_coordinates = 'A'
        end_coordinates = 'D'

        shortest_path = ida_star(graph, start_coordinates, end_coordinates)
        expected_path = []
        self.assertEqual(shortest_path, expected_path, f"Test case 2 failed. Expected: {expected_path}, Got: {shortest_path}")

        # Test case3: Graph with negative edge weights
        graph = networkx.Graph()
        graph.add_edge('A', 'B', weight=2)
        graph.add_edge('B', 'C', weight=-3)
        graph.add_edge('C', 'D', weight=4)

        start_coordinates = 'A'
        end_coordinates = 'D'

        shortest_path = ida_star(graph, start_coordinates, end_coordinates)
        expected_path = ['A', 'B', 'C', 'D']
        self.assertEqual(shortest_path, expected_path, f"Test case 3 failed. Expected: {expected_path}, Got: {shortest_path}")

        # Test case4: Graph with disconnected components
        graph = networkx.Graph()
        graph.add_edge('A', 'B', weight=2)
        graph.add_edge('C', 'D', weight=4)

        start_coordinates = 'A'
        end_coordinates = 'C'
        shortest_path = ida_star(graph, start_coordinates, end_coordinates)
        expected_path = []
        self.assertEqual(shortest_path, expected_path, f"Test case 4 failed. Expected: {expected_path}, Got: {shortest_path}")


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