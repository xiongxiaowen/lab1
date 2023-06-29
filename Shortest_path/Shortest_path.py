"""
This module contains all main functions, like routes, geocoding, path finding, plotting etc. 
This version can work either with dijkstra’s algorithm or IDA* algorithm.
"""
import secrets
import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from geopy.geocoders import Nominatim
import requests
import folium
import polyline
import networkx
from dijkstra import dijkstra
from ida_star import ida_star

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# making an instance of Nominatim class
geolocator = Nominatim(user_agent="shortest_path_app")

# Define the OpenStreetMap API endpoint for geocoding
GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

# Create a weighted graph
graph = networkx.Graph()

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    build the home page.
    """
    if request.method == 'POST':
        start_point = request.form['start']
        end_point = request.form['end']

        if not start_point or not end_point:
            flash('Please provide both a start and end address.', 'error')
            return redirect(url_for('home'))

        # use geocoding geocode function to convert addresses to coordinates
        start_coordinates = geocode(start_point)
        end_coordinates = geocode(end_point)

        # Perform find_shortest_path function, the key operation for this program
        shortest_path = find_shortest_path(start_coordinates, end_coordinates)

        if start_coordinates and end_coordinates:
            # Plot the shortest path on the map and save it as an HTML file
            file_path = plot_shortest_path(start_coordinates, end_coordinates, shortest_path)
            if file_path:
                # Pass the shortest path and coordinates to the template for visualization
                redirect_url = url_for('show_shortest_path', file_path=file_path)
                return redirect(redirect_url)

        # scenario where geocoding fails
        if not start_coordinates or not end_coordinates:
            return render_template('index.html', error="Unable to find coordinates for addresses.")

        # scenario where shortest path cannot be found
        if shortest_path is None:
            return render_template('index.html', error="Unable to find a path.")

    return render_template('index.html')


def geocode(address):
    """
    applying geocode method to get the location
    """
    try:
        location = geolocator.geocode(address)
        print(location)  # Print loocation variable
        if (
            location is not None and
            hasattr(location, 'latitude') and
            hasattr(location, 'longitude')
            ):
            return location.latitude, location.longitude
    except Exception as ex:
        print(f"Geocoding failed for address '{address}': {ex}")
    return None


def find_shortest_path(start_coordinates, end_coordinates):
    """
    Implement Dijkstra’s Algorithm (priority queue implemented on heap) or IDA* Algorithm
    use the start_coordinates and end_coordinates to calculate the shortest path
    Return the shortest path as a list of coordinate
    """
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

    # Use Algorithm:
    if start_coordinates not in graph.nodes or end_coordinates not in graph.nodes:
        # Handle the case when the coordinates are not present in the graph
        flash('Invalid start or end coordinates. Please provide valid coordinates.', 'error')
        return redirect(url_for('home'))

    # if use ida_star function (IDA* Algorithm) to find the shortest path, run below line:
    shortest_path = ida_star(graph, start_coordinates, end_coordinates)
    # if use Dijkstra’s Algorithm to find the shortest path, run below line:
    #shortest_path = dijkstra(graph, 'start', 'end')

    if not shortest_path:
        return "No path found"

    # Retrieve the coordinates of the nodes in the shortest path
    path_coordinates = [graph.nodes[node]['pos'] for node in shortest_path]

    return path_coordinates


def plot_shortest_path(start_coordinates, end_coordinates, shortest_path):
    """
    this function plots the found path.
    """
    # Define the OSRM API endpoint
    url = (f"http://router.project-osrm.org/route/v1/driving/"
            f"{start_coordinates[1]},{start_coordinates[0]};"
            f"{end_coordinates[1]},{end_coordinates[0]}")

    # Send a request to the OSRM API
    response = requests.get(url, timeout=5).json()

    # Check if the 'routes' key exists in the response
    if 'routes' not in response or not response['routes']:
        raise ValueError("Missing 'routes' key in API response")

    # Get the encoded polyline from the first route
    route = response['routes'][0]

    # Check if the 'geometry' key exists in the route
    if 'geometry' not in route:
        raise ValueError("Missing 'geometry' key in route")

    # Retrieve the encoded polyline from the response
    encoded_polyline = route['geometry']

    # Decode the polyline to obtain the coordinates
    coordinates = polyline.decode(encoded_polyline)

    # Create a map object using Folium
    m_map = folium.Map(location=start_coordinates, zoom_start=13)

    # Plot the start and destination markers
    folium.Marker(start_coordinates, popup="Start").add_to(m_map)
    folium.Marker(end_coordinates, popup="Destination").add_to(m_map)

    # Plot the polyline for the shortest path
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m_map)

    # Generate a random cache-busting parameter
    # ensure the URL is unique for each version of the HTML file
    cache_bust = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Construct the file name with the cache-busting parameter
    file_name = f"shortest_path_{cache_bust}.html"
    file_path = os.path.join("templates", file_name)

    # Save the map as an HTML file to templates folder
    m_map.save(file_path)

    return file_path, shortest_path


@app.route('/shortest_path')
def show_shortest_path():
    """
    retrieves the value of the file_path parameter from the query string
    if user submits the form, will be redirected to below route.
    """
    file_path = request.args.get('file_path')
    return render_template('results.html', file_path=file_path)


@app.route('/display_map/<file_path>')
def display_map(file_path):
    """
    send the map to the frame
    """
    return send_file(file_path)

if __name__ == '__main__':
    app.run()
