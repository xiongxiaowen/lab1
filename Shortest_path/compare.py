import time
from flask import flash, redirect, render_template, url_for
from Shortest_path import graph
from IDA_star import ida_star
from Dijkstra import dijkstra

def compare_shortest_paths(start_coordinates, end_coordinates):

    if start_coordinates not in graph.nodes or end_coordinates not in graph.nodes:
        flash('Invalid start or end coordinates. Please provide valid coordinates.', 'error')
        return redirect(url_for('home'))
    else:
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
        
        # Check which faster
        if ida_star_path and dijkstra_path:
            fastest_algorithm = 'IDA*' if ida_star_execution_time < dijkstra_execution_time else 'Dijkstra'
            fastest_path = ida_star_path if fastest_algorithm == 'IDA*' else dijkstra_path
            
            # Display the template with the fastest algorithm and path
            return render_template('result.html', fastest_algorithm=fastest_algorithm, fastest_path=fastest_path)
        else:
            # Handle the case when one or both paths were not found
            flash('Unable to find the shortest path using one or both algorithms.', 'error')
            return redirect(url_for('home'))