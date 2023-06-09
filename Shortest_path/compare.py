"""
This module is not part of the program, but for checking performance.
Use this verion to compare the execution times of geocoding, IDA* algorithm and Dijkstra's algorithm.
it tells the fastest algorithm.
"""

import time
from geopy.geocoders import Nominatim
import networkx
from dijkstra import dijkstra
from ida_star import ida_star


# making an instance of Nominatim class
geolocator = Nominatim(user_agent="shortest_path_app")

# Create a weighted graph
graph = networkx.Graph()


# Implement Dijkstra’s Algorithm (priority queue implemented on heap) or IDA* Algorithm, 
# use the start_coordinates and end_coordinates to calculate the shortest path
# Return the shortest path as a list of coordinates
def find_shortest_path(start_coordinates, end_coordinates):

    start_coordinates = geocode(start_point)
    end_coordinates = geocode(end_point)

    # Add the start and end nodes with their coordinates to the graph
    graph.add_node('start', pos=start_coordinates)
    graph.add_node('node1', pos=(0, 0))  # Add 'node1' with placeholder coordinates
    graph.add_node('node2', pos=(0, 0))  # Add 'node2' with placeholder coordinates
    graph.add_node('end', pos=end_coordinates)

    # Define the distance function (Euclidean distance between two points)
    def distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # Calculate the distance between two nodes based on their coordinates
    def calculate_distance(node1, node2):
        return distance(graph.nodes[node1]['pos'], graph.nodes[node2]['pos'])


    # Add edges to the graph connecting neighboring nodes
    graph.add_edge('start', 'node1', weight=calculate_distance('start', 'node1'))
    graph.add_edge('node1', 'node2', weight=calculate_distance('node1', 'node2'))
    graph.add_edge('node2', 'end', weight=calculate_distance('node2', 'end'))

    print("Graph Edges:", graph.edges)
    print("Graph Nodes:", graph.nodes)

    # Define a tolerance for coordinate matching
    tolerance = 0.00001

    # Use Algorithm:
    if not any(distance(start_coordinates, node['pos']) < tolerance for node in graph.nodes.values()) or \
            not any(distance(end_coordinates, node['pos']) < tolerance for node in graph.nodes.values()):
        # Handle the case when the coordinates are not present in the graph
        print('Invalid start or end coordinates. Please provide valid coordinates.')
        return None, None

    # if use ida_star function (IDA* Algorithm) to find the shortest path, run below line: 
    ida_star_path = ida_star(graph, start_coordinates, end_coordinates)
    # if use Dijkstra’s Algorithm to find the shortest path, run below line: 
    dijkstra_path = dijkstra(graph, 'start', 'end')

    if not dijkstra_path:
        print("dijkstra_path no found")

    if not ida_star_path:
        print("ida_star_path no found")

    # Retrieve the coordinates of the nodes in the path
    path_coordinatesida_star = [graph.nodes[node]['pos'] for node in ida_star_path]
    path_coordinatesdijkstra = [graph.nodes[node]['pos'] for node in dijkstra_path]

    #print the found path
    print('IDA* Path:', path_coordinatesida_star)
    print('Dijkstra Path:', path_coordinatesdijkstra)


def compare_shortest_paths(start_coordinates, end_coordinates):
    ida_star_path, dijkstra_path = find_shortest_path(start_coordinates, end_coordinates)

    if start_coordinates is None or end_coordinates is None:
        print('Invalid start or end address. Please provide address.')
        return

    if ida_star_path and dijkstra_path:
        # execution time of IDA* algorithm
        ida_star_start_time = time.time()
        ida_star_path = ida_star(graph, start_coordinates, end_coordinates)
        ida_star_end_time = time.time()
        ida_star_execution_time = ida_star_end_time - ida_star_start_time
        
        # execution time of Dijkstra's algorithm
        dijkstra_start_time = time.time()
        dijkstra_path = dijkstra(graph, 'start', 'end')
        dijkstra_end_time = time.time()
        dijkstra_execution_time = dijkstra_end_time - dijkstra_start_time
        
      # Print out the execution times
        print("Execution time of IDA* algorithm:", ida_star_execution_time)
        print("Execution time of Dijkstra's algorithm:", dijkstra_execution_time)
    else:
        print("Unable to find the shortest path using one or both algorithms.")


# applying geocode method to get the location
def geocode(address):
    try: 
        start_time = time.time()
        location = geolocator.geocode(address)
        end_time = time.time()
        execution_time = end_time - start_time

        if location is not None and hasattr(location, 'latitude') and hasattr(location, 'longitude'):
            return (location.latitude, location.longitude), execution_time
    except Exception as ex:
        print(f"Geocoding failed for address '{address}': {ex}")
    return None, execution_time


          
if __name__ == '__main__':
    start_point = input("Enter the start address: ")
    end_point = input("Enter the end address: ")

    start_coordinates, start_execution_time = geocode(start_point)
    end_coordinates, end_execution_time = geocode(end_point)

    #print geocoding coordinates & execution time
    print("Start Coordinates after geocoding:", start_coordinates)
    print("End Coordinates after geocoding:", end_coordinates)
    print("Geocoding Execution Time (Start Address):", start_execution_time)
    print("Geocoding Execution Time (End Address):", end_execution_time)

