from flask import Flask, render_template, request, redirect, url_for
from geopy.geocoders import Nominatim  # Importing Nominatim geocoder class
from queue import PriorityQueue
import requests
import folium
import polyline
import networkx #To implement the find_shortest_path function, 
#use the networkx library to represent the graph and the networkx built-in shortest path algorithms 
#to calculate the shortest path. Here's an example implementation:
import random
import string
import os

app = Flask(__name__)

# making an instance of Nominatim class
geolocator = Nominatim(user_agent="shortest_path_app")

# Define the OpenStreetMap API endpoint for geocoding
GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_point = request.form['start']
        end_point = request.form['end']

        # use geocoding geocode function to convert addresses to coordinates
        start_coordinates = geocode(start_point)
        end_coordinates = geocode(end_point)

        # scenario where geocoding fails
        if not start_coordinates or not end_coordinates:
            return render_template('index.html', error="Unable to find coordinates for the given addresses.")

        # Perform the path finding algorithm with find_shortest_path function, the key operation for this program
        shortest_path = find_shortest_path(start_coordinates, end_coordinates)

        # scenario where shortest path cannot be found
        if shortest_path is None:
            return render_template('index.html', error="Unable to find a path.")

        # Plot the shortest path on the map and save it as an HTML file
        file_path = plot_shortest_path(start_coordinates, end_coordinates, shortest_path)

        # Pass the shortest path and coordinates to the template for visualization, 
        return redirect(url_for('show_shortest_path', file_path=file_path))

    return render_template('index.html')


# applying geocode method to get the location
def geocode(address):
    location = geolocator.geocode(address)
    if location is not None:
        return location.latitude, location.longitude
    return None


# Operates Dijkstra’s Algorithm 
def dijkstra(graph, start_coordinates, end_coordinates):
    # Initialize the distance dictionary with infinity for all nodes, except the start node
    distances = {}

    for node in graph: 
        distances[node] = float("inf")
    distances[start_coordinates] = 0
    
    # for visited nodes
    visited = {}

    # Create a priority queue to store nodes
    queue = PriorityQueue()  
    queue.put((0, start_coordinates))
    while not queue.empty():
        # Get the node with the smallest tentative distance from the priority queue
        current_distance, current_node = queue.get()
        # break when end node is reached
        if current_node == end_coordinates:
            break

        # Explore the neighbors of the current node
        for neighbor in graph[current_node]:
            # Calculate the distance from the start to the neighbor through the current node
            distance = current_distance + graph[current_node][neighbor]['weight']
            # If a shorter path is found, update the distance and visited node
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                visited[neighbor] = current_node

                # Add the neighbor code to the priority queue with the updated distance
                queue.put((distance, neighbor))

    # If no path from the start node to the end node, return None
    if end_coordinates not in visited:
        return None

    # Reconstruct the shortest path list from the visited nodes
    shortest_path = []
    current_node = end_coordinates
    while current_node != start_coordinates:
        shortest_path.append(current_node)
        current_node = visited[current_node]
    shortest_path.append(start_coordinates)

    shortest_path.reverse()

    return shortest_path


# Implement Dijkstra’s Algorithm, use the start_coordinates and end_coordinates to calculate the shortest path
# Return the shortest path as a list of coordinates
def find_shortest_path(start_coordinates, end_coordinates):
    # Create a weighted graph
    graph = networkx.Graph()

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

    # Use Dijkstra’s Algorithm to find the shortest path: 
    shortest_path = dijkstra(graph, start_coordinates, end_coordinates)

    # Retrieve the coordinates of the nodes in the shortest path
    path_coordinates = [graph.nodes[node]['pos'] for node in shortest_path]

    return path_coordinates


def plot_shortest_path(start_coordinates, end_coordinates, shortest_path):
    # Define the OSRM API endpoint
    url = f"http://router.project-osrm.org/route/v1/driving/{start_coordinates[1]},{start_coordinates[0]};{end_coordinates[1]},{end_coordinates[0]}"

    # Send a request to the OSRM API
    response = requests.get(url).json()

    # Retrieve the encoded polyline from the response
    encoded_polyline = response['routes'][0]['geometry']

    # Decode the polyline to obtain the coordinates
    coordinates = polyline.decode(encoded_polyline)

    # Create a map object using Folium
    m = folium.Map(location=start_coordinates, zoom_start=13)

    # Plot the start and destination markers
    folium.Marker(start_coordinates, popup="Start").add_to(m)
    folium.Marker(end_coordinates, popup="Destination").add_to(m)

    # Plot the polyline for the shortest path
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

    # Generate a random cache-busting parameter, ensure the URL is unique for each version of the HTML file
    cache_bust = ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))

    # Construct the file name with the cache-busting parameter
    file_name = f"shortest_path_{cache_bust}.html"
    file_path = os.path.join(r"C:\Users\xiong\lab1\Shortest_path\templates", file_name)

    file_url = file_path + '?_cache_bust=' + cache_bust

    # Save the map as an HTML file
    m.save(file_path)

    return file_path

# if user submits the form, will be redirected to below route.
@app.route('/shortest_path')
def show_shortest_path():
    file_path = request.args.get('file_path')
    cache_bust = file_path.split('_')[-1].split('.')[0]
    template_name = f'shortest_path_{cache_bust}.html'
    return render_template(template_name, file_path=file_path)

if __name__ == '__main__':
    app.run()
