from flask import Flask, render_template, request
from queue import PriorityQueue
import requests
import networkx
import folium
import polyline

app = Flask(__name__)

# use this to create a weighted graph
graph = networkx.Graph()

# use OpenStreetMap API endpoint for geocoding
GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

# below function for managing the web pages’ route, home function returns to the index.html. if make GET request, index.html is rendered.
@app.route('/', methods=['GET', 'POST'])
def home():
        #if make POST request,the POST block start to work, obtain data from the label start and end in the index.html form. Values are assigned to start_point and end-point.
    if request.method == 'POST':
        start_point = request.form['start']
        end_point = request.form['end']

        # use geocoding geocode function to convert start_point and end-point addresses to coordinates.
        start_coordinates = geocode(start_point)
        end_coordinates = geocode(end_point)

        if not start_coordinates or not end_coordinates:
            return render_template('index.html', error="Unable to find coordinates for the addresses.")

        # if geocoding address successful, perform the path finding algorithm with find_shortest_path function, the key operation for this program
        shortest_path = find_shortest_path(start_coordinates, end_coordinates)

        # if no path found, display error message
        if shortest_path is None:
            return render_template('index.html', error="Error: Unable to find a path.")

        # if path found, visualize the path on the map and save it as an HTML file to templates folder.
        plot_shortest_path(start_coordinates, end_coordinates, shortest_path)

        # Pass the shortest path and coordinates to the html file in the templates folder for visualization
        return render_template('shortest_path.html', shortest_path=shortest_path, start_coordinates=start_coordinates, end_coordinates=end_coordinates)

    return render_template('index.html')


#Below function use address as parameter to obtain longitude and latitude data
def geocode(address):
    params = {
        "q": address,
        "format": "json"
}
    #send GET request to the API
    response = requests.get(GEOCODE_API_URL, params=params)
    #if request successful,json method store the data as “data” variable. 
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return (float(data[0]['lon']), float(data[0]['lat']))
    return None


#Below is the key function for this program, using IDA* search to find path
def find_shortest_path(start_coordinates, end_coordinates):

    # Convert start and end coordinates to nodes, add ndoes to the graph
    start_point = geocode(start_coordinates)
    end_point = geocode(end_coordinates)
    if not start_point or not end_point:
        return None

    graph.add_node(start_coordinates, pos=start_point)
    graph.add_node(end_coordinates, pos=end_point)

    # Define the heuristic function (estimated distance from a node to the end node)
    def heuristic(node):
        start_pos = graph.nodes[start_coordinates]['pos']
        node_pos = graph.nodes[node]['pos']
        return distance(start_pos, node_pos)

    # Define the cost function (weight of an edge between two nodes)
    def cost(node1, node2):
        node1_pos = graph.nodes[node1]['pos']
        node2_pos = graph.nodes[node2]['pos']
        return distance(node1_pos, node2_pos)

    # Define the actions function (generate neighboring nodes from a given node)
    def actions(node):
        return list(graph.neighbors(node))

    # Define the distance function (Euclidean distance between two points)
    def distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # Define the IDA* search function
    def ida_star_search():
        start_node = (start_coordinates, 0, heuristic(start_coordinates), None)  # (node, g_score, f_score, parent)
        threshold = start_node[2]  # Initial threshold is the heuristic value of the start node

        while True:
            result, threshold = search(start_node, 0, threshold)
            if result is not None:
                return result


    # Define the recursive search function used in IDA*
    def search(node, g_score, threshold):
        node, _, f_score, _ = node
        f_score = g_score + heuristic(node)

        if f_score > threshold:
            return None, f_score

        if node == end_coordinates:
            return reconstruct_path(node), threshold

        min_cost = float('inf')
        neighbors = actions(node)

        for neighbor in neighbors:
            cost_to_neighbor = cost(node, neighbor)
            neighbor_node = (neighbor, g_score + cost_to_neighbor, 0, node)  # (node, g_score, f_score, parent)
            result, new_threshold = search(neighbor_node, g_score + cost_to_neighbor, threshold)

            if result is not None:
                return result, threshold

            min_cost = min(min_cost, new_threshold)

        return None, min_cost


    # Reconstruct the path from the goal node to the start node
    def reconstruct_path(node):
        path = []

        while node is not None:
            path.append(node)
            node = graph.nodes[node].get('parent')

        return list(reversed(path))


    # Run the IDA* search
    shortest_path = ida_star_search()

    return shortest_path



def plot_shortest_path(start_coordinates, end_coordinates, shortest_path):
    # Define the OSRM (Open Source Routing Machine) API endpoint
    url = "fhttp://router.project-osrm.org/route/v1/driving/{start_coordinates[1]},{start_coordinates[0]};{end_coordinates[1]},{end_coordinates[0]}"

    # Send a request to the OSRM API
    response = requests.get(url).json()

    # Retrieve coordinates from the response
    encoded_polyline = response['routes'][0]['geometry']['coordinates']

    # Create a map object using Folium
    m = folium.Map(location=start_coordinates, zoom_start=13)

    # Plot the start and destination markers
    folium.Marker(start_coordinates, popup="Start").add_to(m)
    folium.Marker(end_coordinates, popup="Destination").add_to(m)

    # Plot the polyline for the shortest path
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

    # Save the map as an HTML file to the templates folder
    file_path = r"C:\Users\xiong\lab1\Shortest_path\templates\shortest_path.html"
    m.save(file_path)

    return file_path


if __name__ == '__main__':
    app.run() #starts the flask running.
