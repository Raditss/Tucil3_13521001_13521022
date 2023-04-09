# Tucil3_13521001_13521022
 This program reads a file of nodes and edges and calculates the shortest path between two input nodes using either A* or Uniform Cost Search (UCS). The nodes represent locations on Earth, and the edges represent the distance between them.

The program outputs the shortest path between the two nodes as well as the distance of the path in kilometers. Additionally, the program visualizes the nodes and the shortest path on a map using the Folium library.

## Requirements
 The program requires Python 3.6 or higher. The program also requires the following Python libraries:
 - heapq
 - folium
 - PyQt5

## Usage
The program can be run by executing the following command in the terminal(macOS/Linux) 
```
python3 main.py
``` 
command prompt (Windows):
```
python main.py
``` 
The program will prompt you to enter the input file name, the start node, the end node, and the search algorithm to use (A* or UCS).

The input file should be in the following format:
```
n
name_1 lat_1 long_1
name_2 lat_2 long_2
...
name_n lat_n long_n
a11 a12 ... a1n
a21 a22 ... a2n
...
an1 an2 ... ann
```
Where n is the number of nodes, name_i is the name of the i-th node, lat_i and long_i are the latitude and longitude of the i-th node, and a_ij is the adjacency between node i and node j.

## Output
The program outputs the shortest path between the start and end nodes in the following format:
```
Route: node_1 -> node_2 -> ... -> node_n
Distance: x KM
```
Where node_1 to node_n are the nodes in the shortest path and x is the distance of the path in kilometers.

## Visualization
The program visualizes the nodes and the shortest path on a map using the Folium library. The map is displayed in a PyQt5 window.

## Authors
| Name | NIM |
| --- | --- |
| Angger Ilham A. | 13521001 |
| Raditya Naufal A. | 13521022 |
