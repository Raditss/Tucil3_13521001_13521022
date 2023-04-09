from math import radians, sin, cos, sqrt, atan2
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
        for next in graph[current]['edges']:
            new_cost = cost_so_far[current] + graph[current]['edges'][next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + calculate_distance(graph[next]['lat'],graph[goal]['lat'],graph[next]['lon'],graph[goal]['lon'])
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    return came_from, cost_so_far

def usc(start, goal, graph):
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
        for next in graph[current]['edges']:
            new_cost = cost_so_far[current] + graph[current]['edges'][next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    return came_from, cost_so_far

def printRoute(start, goal, came_from, cost_so_far):
    current = goal
    path = [current]
    total_cost = cost_so_far[current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    total_cost = round(total_cost, 3)
    print(f"Route: {' -> '.join(path)}")
    print(f"Distance: {total_cost} KM")

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    distance = R*c

    return distance

def parse(input):
    with open(input) as f:
        n = int(f.readline().strip())
        nodes = {}
        for i in range(n):
            name, lat, long = f.readline().strip().split()
            nodes[name] = {'lat': float(lat), 'lon': float(long), 'edges': {}}
        for i in range(n):
            adjacency_matrix_row = list(map(int, f.readline().strip().split()))
            for j in range(n):
                if adjacency_matrix_row[j] == 1:
                    node1 = nodes[list(nodes.keys())[i]]
                    node2 = nodes[list(nodes.keys())[j]]
                    distance = calculate_distance(node1['lat'], node1['lon'], node2['lat'], node2['lon'])
                    nodes[list(nodes.keys())[i]]['edges'][list(nodes.keys())[j]] = distance
    return nodes

def main():
    nodes = parse('test/buahbatu.txt')
    print('Daftar node: ')
    print(list(nodes.keys()))
    start = input('Masukkan node awal: ')
    while start not in nodes:
        print('Node tidak ditemukan, silakan coba lagi')
        start = input('Masukkan node awal: ')

    goal = input('Masukkan node tujuan: ')
    while goal not in nodes:
        print('Node tidak ditemukan, silakan coba lagi')
        goal = input('Masukkan node tujuan: ')

    temp = input('Masukkan metode pencarian (A* atau UCS): ')
    while temp != 'A*' and temp != 'UCS':
        print('Metode pencarian tidak ditemukan, silakan coba lagi')
        temp = input('Masukkan metode pencarian (A* atau UCS): ')

    if temp == 'A*':
        came_from, cost_so_far = aStar(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
    else:
        came_from, cost_so_far = usc(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
    
    m = folium.Map(location=[nodes[start]['lat'], nodes[start]['lon']], zoom_start=15)

    # Add markers for the nodes
    for node_name in nodes:
        folium.Marker(location=[nodes[node_name]['lat'], nodes[node_name]['lon']], tooltip=node_name).add_to(m)

    # Plot the edges of the graph
    for node_name in nodes:
        for neighbor_name in nodes[node_name]['edges']:
            folium.PolyLine(locations=[(nodes[node_name]['lat'], nodes[node_name]['lon']),
                                        (nodes[neighbor_name]['lat'], nodes[neighbor_name]['lon'])],
                                        color='blue').add_to(m)
    path = [goal]
    current = goal
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    for i in range(len(path)-1):
        folium.PolyLine(locations=[(nodes[path[i]]['lat'], nodes[path[i]]['lon']),
                                    (nodes[path[i+1]]['lat'], nodes[path[i+1]]['lon'])], color='red', weight=5, opacity=0.7).add_to(m)
    
    m.save('map.html')
    app = QtWidgets.QApplication([])
    map_app = MapApp()
    map_app.show()
    app.exec_()


if __name__ == '__main__':
    main()


