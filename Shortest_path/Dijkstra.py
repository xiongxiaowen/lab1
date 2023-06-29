"""
This module contains all fuctions to implment Dijkstra.
"""

class binaryheap:
    """
    use heap, in seprate class.
    for each node (not root), the value of the parent node is <= the values of the children,
    smallest key always at the front(min heap)
    """
    def __init__(self):
        # create a list to store the elements of the heap
        self.heap=[]
        # create a dictionary to store the nodes and their corresponding entries in the heap
        self.node_index={}
        self.current_index = 0

    def push(self, node, distance):
        """
        push new elements to heap
        """
        #needs distance and node stored in the list
        entry =[distance, self.current_index, node]
        #add to the dictionary
        self.node_index[node] = entry
        self.heap.append(entry)
        #increment index
        self.current_index += 1
        #calls belwo method to maintain the heap property
        #by moving the new added element to its correct position
        self._sift_up(len(self.heap) - 1)

    def pop (self):
        """
        removes and returns the element with the smallest distance from the heap
        """
        if not self.heap:
            return None

        node = self.heap[0][2]
        del self.node_index[node]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop()
            #calls below method to maintain the heap property
            #by moving the new root element to the correct position.
            self._sift_down(0)
        else:
            self.heap.pop()

        if self.heap:
            return self.heap[0][0], node
        else:
            return None, None

    def update(self, node, new_distance):
        """
        update the distance of a node in the heap.
        """
        entry = self.node_index[node]
        entry[0] = new_distance
        index = entry[1]
        if index > 0 and entry[0] < self.heap[self._parent(index)][0]:
            self._sift_up(index)
        else:
            self._sift_down(index)

    def is_empty(self):
        """
        Check if the heap is empty
        """
        return len(self.heap) == 0

    #restore the heap property by moving an element up the heap.
    #use an index as input and compares the element at that index with the parent.
    #If the element is smaller, swaps the element with the parent and updates the index.
    def _sift_up(self, index):
        while index > 0 and self.heap[index][0] < self.heap[self._parent(index)][0]:
            self._swap(index, self._parent(index))  # Swap the current entry with its parent
            index = self._parent(index)  # Move up to the parent index

    #restore the heap property by moving an element down the heap.
    #It takes an index as input and compares the element at that index with its children.
    #If any child is smaller, it swaps the element with the smallest child and updates the index.
    def _sift_down(self, index):
        while True:
            smallest = index
            left_child = self._left_child(index)
            right_child = self._right_child(index)
            heap_size = len(self.heap)

            if left_child < heap_size and self.heap[left_child][0] < self.heap[smallest][0]:
                smallest = left_child  # Find the smallest child among the left and right children

            if right_child < heap_size and self.heap[right_child][0] < self.heap[smallest][0]:
                smallest = right_child  # Update the smallest child if the right child is smaller

            if smallest != index:
                self._swap(index, smallest)  # Swap the current entry with the smallest child
                index = smallest  # Move down to the smallest child index
            else:
                # If the current entry´smaller than both children, the heap property is maintained
                break

    def _parent(self, index):
        # Calculate the parent index of a given index, returns the parent index of a given index
        return (index - 1) // 2

    def _left_child(self, index):
        # Calculate the index of the left child of a given index,
        # returns the index of the left child of a given index
        return 2 * index + 1

    def _right_child(self, index):
        # Calculate the index of the right child of a given index,
        # returns the index of the right child of a given index in the heap.
        return 2 * index + 2

    #swaps the entries in the heap list and updates the corresponding indices in the entries.
    #to exchange elements during the process of maintaining the heap property.
    def _swap(self, i, j):
        # Swap the entries in the heap list
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        # Swap the indices in the entries
        self.heap[i][1], self.heap[j][1] = self.heap[j][1], self.heap[i][1]
        # Update the mapping for the swapped entries
        self.node_index[self.heap[i][2]] = self.heap[i]
        # Update the mapping for the swapped entries
        self.node_index[self.heap[j][2]] = self.heap[j]


def dijkstra(graph, start_coordinates, end_coordinates):
    """
    Operates Dijkstra’s Algorithm
    """
    # Initialize the distance dictionary with infinity for all nodes, except the start node
    distances = {}
    for node in graph.nodes:
        distances[node] = float("inf")
    distances[start_coordinates] = 0

    # for visited nodes
    visited = {}

    # create queue
    queue = binaryheap()
    queue.push (start_coordinates, 0)

    while not queue.is_empty():
        # Get the node with the smallest tentative distance from the priority queue
        current_distance, current_node = queue.pop()
        if current_distance is None or current_node is None:
            break

        # break when end node is reached
        if current_node == end_coordinates:
            break

        # Explore the neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            # Calculate the distance from the start to the neighbor through the current node
            distance = current_distance + graph[current_node][neighbor]['weight']
            # If a shorter path is found, update the distance and visited node
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                visited[neighbor] = current_node

                # Add the neighbor code to the priority queue with the updated distance
                queue.push((distance, neighbor))

    # If no path from the start node to the end node, return None
    if end_coordinates not in visited:
        return []

    if end_coordinates not in distances:
        return []

    # Call the reconstruct_shortest_path function
    shortest_path = reconstruct_shortest_path(visited, start_coordinates, end_coordinates)
    return shortest_path, visited



def reconstruct_shortest_path(visited, start_coordinates, end_coordinates):
    """
    Reconstruct the shortest path list from the visited nodes
    """
    shortest_path = []
    current_node = end_coordinates
    while current_node != start_coordinates:
        shortest_path.append(current_node)
        current_node = visited[current_node]
    shortest_path.append(start_coordinates)
    shortest_path.reverse()
    return shortest_path
