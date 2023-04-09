import math
import heapq
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets

class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        

        # Create the map canvas
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setHtml(open('map.html').read())

        # Set up the layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.browser, 0, 2, 5, 1)

        self.setLayout(grid)

def euclidianDist(x1, x2, y1, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def aStar(start, goal, graph):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while frontier:
        current = heapq.heappop(frontier)[1]
        if current == goal:
            break
        for next_node in graph[current]['edges']:
            new_cost = cost_so_far[current] + graph[current]['edges'][next_node]
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + euclidianDist(graph[next_node]['x'], graph[goal]['x'], graph[next_node]['y'], graph[goal]['y'])
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current
    return came_from, cost_so_far

# Step 1: Parse the input
with open("test/buahbatu.txt") as f:
    n = int(f.readline().strip())
    nodes = {}
    for i in range(n):
        name, lat, long = f.readline().strip().split()
        nodes[name] = {'x': float(lat), 'y': float(long), 'edges': {}}
    for i in range(n):
        adjacency_matrix_row = list(map(int, f.readline().strip().split()))
        for j in range(n):
            if adjacency_matrix_row[j] == 1:
                nodes[list(nodes.keys())[i]]['edges'][list(nodes.keys())[j]] = euclidianDist(
                    nodes[list(nodes.keys())[i]]['x'], nodes[list(nodes.keys())[j]]['x'],
                    nodes[list(nodes.keys())[i]]['y'], nodes[list(nodes.keys())[j]]['y'])

# Step 2: Find the shortest path using A* algorithm
start_node = input("Enter the start node: ")
end_node = input("Enter the end node: ")
came_from, cost_so_far = aStar(start_node, end_node, nodes)

# Step 3: Plot the shortest path on the map
m = folium.Map(location=[nodes[start_node]['x'], nodes[start_node]['y']], zoom_start=15)

# Add markers for the nodes
for node_name in nodes:
    folium.Marker(location=[nodes[node_name]['x'], nodes[node_name]['y']], tooltip=node_name).add_to(m)

# Plot the edges of the graph
for node_name in nodes:
    for neighbor_name in nodes[node_name]['edges']:
        folium.PolyLine(locations=[(nodes[node_name]['x'], nodes[node_name]['y']),
                                    (nodes[neighbor_name]['x'], nodes[neighbor_name]['y'])],
                        color='blue').add_to(m)

# Plot the shortest path on the map
path = [end_node]
current = end_node
while current != start_node:
    current = came_from[current]
    path.append(current)
path.reverse()
for i in range(len(path)-1):
    folium.PolyLine(locations=[(nodes[path[i]]['x'], nodes[path[i]]['y']),
                                (nodes[path[i+1]]['x'], nodes[path[i+1]]['y'])], color='red', weight=5, opacity=0.7).add_to(m)

# Step 4: Save the map as an HTML file
m.save('map.html')

# Step 5: Run the GUI
app = QtWidgets.QApplication([])
map_app = MapApp()
map_app.show()
app.exec_()

