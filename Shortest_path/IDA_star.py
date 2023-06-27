#implementing IDA*

def ida_star(graph, start_coordinates, end_coordinates):
    # heuristic function (Euclidean distance between two points)
    # estimates the distance between a given node and the goal node
    def heuristic(start_coordinates, end_coordinates):
        x1, y1 = start_coordinates
        x2, y2 = end_coordinates
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    distances = {}
    for node in graph.nodes:
        distances[node] = float("inf")
    distances[start_coordinates] = 0

    # for visited nodes
    visited = {}

    # Define the IDA* search function
    def search(current_coordinates, g, bound):
        f = g + heuristic(current_coordinates, end_coordinates)
        if f > bound:
            return f

        if current_coordinates == end_coordinates:
            return "FOUND"

        min_cost = float("inf")

      # neighbors sorted by the combined cost of the path from the start node and the heuristic estimate
        neighbors = sorted(graph.neighbors(current_coordinates), key=lambda neighbor: g + graph[current_coordinates][neighbor]['weight'] + heuristic(neighbor, end_coordinates))


        # Explore the neighbors of the current node
        for neighbor in neighbors:
            # Calculate the distance from the start to the neighbor through the current node
            distance = g + graph[current_coordinates][neighbor]['weight']
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                visited[neighbor] = current_coordinates

                cost = search(neighbor, distance, bound)
                if cost == "FOUND":
                    return "FOUND"
                if cost < min_cost:
                    min_cost = cost

        return min_cost

    # Perform the IDA* search
    bound = heuristic(start_coordinates, end_coordinates)
    while True:
        cost = search(start_coordinates, 0, bound)
        if cost == "FOUND":
            break
        if cost == float("inf"):
            return []

        bound = cost

    # Reconstruct the shortest path
    shortest_path = reconstruct_shortest_path(visited, start_coordinates, end_coordinates)
    return shortest_path


# Reconstruct the shortest path list from the visited nodes
def reconstruct_shortest_path(visited, start_coordinates, end_coordinates):
    shortest_path = []
    current_coordinates = end_coordinates
    while current_coordinates != start_coordinates:
        shortest_path.append(current_coordinates)
        current_coordinates = visited[current_coordinates]
    shortest_path.append(start_coordinates)
    shortest_path.reverse()
    return shortest_path
