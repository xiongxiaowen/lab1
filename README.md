﻿# Shortest_path
This is the repository for "Tietorakenteet ja algoritmit harjoitustyö alkukesä".


This project is to implement an efficient solution to find the shortest driving distance path between two street addresses. IDA* vs Dijkstra two algorithms will be compared for this project work. 


Weekly reports & other documents:
+ stored in the folder "documentation".


How to startup the program: 
+ "shortest_path.py": the main module to startup the program.
+ "dijkstra.py": Dijkstra algorithm implementation, priority queue implemented on heap.
+ "ida_star.py": the file of implementing IDA* (Iterative Deepening A*) algorithm.
    + please refer to the document "Käyttöohje _ Instructions.pdf". 


"compare.py" file: 
+ not a part of the program. It checks the execution time of each algorithm, compare the execution time.


Run tests: 
+ Ensure the "shortest_path.py" module file is located in the same directory as the tests folder. 
+ Run command "python -m unittest discover tests" to cover all tests. 


Generate the coverage report: 
+ run command "coverage run -m unittest discover", which tells the coverage tool to run the tests and collect coverage data, then unittest will automatically discover and run all test cases it finds in the project.
+ Run "coverage html", which generates a HTML report in the current directory (Wrote HTML report to htmlcov\index.html). 


Code style checking with pylint:
+ run "pylint filename.py", replace filename with the actual file name.

 
