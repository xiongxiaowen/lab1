from flask import Flask, render_template, request
from queue import PriorityQueue
import requests
import matplotlib.pyplot as plt

app = Flask(__name__)


# Below function for managing the web pages’ route, home function returns to the index.html. 
# if make GET request, index.html is rendered.
@app.route('/', methods=['GET', 'POST'])
def home():
        #if make POST request,the POST block start to work, obtain data from the label start and end in the index.html form. 
        #Values are assigned to start_point and end-point.
    if request.method == 'POST':
        start_point = request.form['start']
        end_point = request.form['end']

        # use geocoding geocode function to convert start_point and end-point addresses to coordinates.
        start_coordinates = geocode(start_point)
        end_coordinates = geocode(end_point)

        if not start_coordinates or not end_coordinates:
            return render_template('index.html', error="Unable to find coordinates for the addresses.")

        # if geocoding address successful, perform the path finding algorithm with find_shortest_path function, 
        # the key operation for this program
        shortest_path = find_shortest_path(start_coordinates, end_coordinates)

        # if no path found, display error message
        if shortest_path is None:
            return render_template('index.html', error="Error: Unable to find a path.")

        # if path found, visualize the path on the map and save it as an HTML file to templates folder.
        plot_shortest_path(start_coordinates, end_coordinates, shortest_path)

        # Pass the shortest path and coordinates to the html file in the templates folder for visualization
        return render_template('shortest_path.html', shortest_path=shortest_path, start_coordinates=start_coordinates, end_coordinates=end_coordinates)

    return render_template('index.html')

# use OpenStreetMap API for geocoding
GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

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
        return (float(data[0]['lon']), float(data[0]['lat']))
    return None


#Below is the key function for this program, using Dijkstra's algorithm to find path
def find_shortest_path(start_coordinates, end_coordinates):   
    
    # below dictionary to store the tentative distances from the start node to each node
    distances = {}

    # below dictionary to store the previous node in the optimal path, 
    # as Dijkstra's algorithm keeps track of the currently known shortest distance from each node to the source node and it updates these values if it finds a shorter path.
    previous = {}

    # Create a priority queue to store nodes and their tentative distances, 
    # ensures the node with the smallest distance is always at the front of the queue. 
    queue = PriorityQueue()

    # Initialize all distances to infinity except for the start node (distance = 0)
    for node in graph:
        distances[node] = float('inf')
    distances[start_coordinates] = 0

    # Add the start node to the priority queue
    queue.put((0, start_coordinates))

    while not queue.empty():
        # Get the node with the smallest tentative distance from the priority queue
        current_distance, current_node = queue.get()

        # Stop when the end node is reached
        if current_node == end_coordinates:
            break

        # Explore the neighbors of the current node
        for neighbor in graph[current_node]:
            # Calculate the distance from the start node to the neighbor through the current node
            distance = current_distance + graph[current_node][neighbor]

            # If a shorter path is found, update the distance and previous node
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node

                # put neighbor code to the priority queue with the updated distance
                queue.put((distance, neighbor))

    # Reconstruct the shortest path from the previous nodes
    shortest_path = []
    current_node = end_coordinates
    while current_node != start_coordinates:
        shortest_path.append(current_node)
        current_node = previous[current_node]
    shortest_path.append(start_coordinates)

    return shortest_path


def plot_shortest_path(start_coordinates, end_coordinates, shortest_path):
    # need a graph structure to represent the map, to be fixed next week
    graph = []

    # Extract coordinates from the shortest path
    x = [coord[0] for coord in shortest_path]
    y = [coord[1] for coord in shortest_path]

    # Create a scatter plot of the coordinates
    plt.scatter(x, y, color='blue')

    # Add labels for start and end points
    plt.text(start_coordinates[0], start_coordinates[1], 'Start', fontsize=9)
    plt.text(end_coordinates[0], end_coordinates[1], 'End', fontsize=9)

    # Connect the points with a visible line
    plt.plot(x, y, color='blue', linewidth=2)

    # Set plot title and labels
    plt.title('Shortest Path')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Set plot limits
    plt.xlim(min(x) - 0.1, max(x) + 0.1)
    plt.ylim(min(y) - 0.1, max(y) + 0.1)

    # Save the plot as an image file to the templates folder.
    plt.savefig(r"C:\Users\xiong\lab1\Shortest_path\templates\shortest_path.html")

    # Close plot
    plt.close()

    print("Shorted path found here")

if __name__ == '__main__':
    app.run() #starts the flask running.
