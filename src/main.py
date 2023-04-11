from parse import parsemap, parsegraph
from astar import astarmap, astargraph
from UCS import ucs
from extras import printRoute, returnRoute
import folium
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import os
from PyQt5.QtWebEngineWidgets import QWebEngineView
import matplotlib.pyplot as plt

class MapApp(QtWidgets.QMainWindow):
    def __init__(self, path, total_cost):
        super().__init__()

        # Create a QWebEngineView object to display the HTML file
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        # read-only property
        self.textbox = QTextEdit(self)
        self.textbox.setGeometry(10,430,200,60)
        self.textbox.setReadOnly(True)
        self.setWindowTitle('HTML Viewer')
        self.setGeometry(100,100,500,500)

        # Set the textbox to always appear in the bottom left corner
        self.set_textbox_position()
        self.textbox.show()

        a = f"Route: {' -> '.join(path)}"
        b = f"Distance: {total_cost} KM"
        text = f"{a}\n{b}"
        self.textbox.setPlainText(text)
        self.webview.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath("bin/map.html")))

    def resizeEvent(self, event):
        self.set_textbox_position()
        event.accept()

    def set_textbox_position(self):
        self.textbox.move(10, self.height() - self.textbox.height() - 10)



def mainmap():
    maps=input ("Insert input file name (without extension): ")
    mapsname = "test/"+maps+".txt"
    nodes = parsemap(mapsname)
    print('list of nodes: ')
    print(list(nodes.keys()))
    start = input('Insert start node: ')
    while start not in nodes:
        print('Node is not found, please insert a different value')
        start = input('Insert start node: ')

    goal = input('Insert goal node: ')
    while goal not in nodes:
        print('Node is not found, please insert a different value')
        goal = input('Insert goal node: ')

    temp = input('insert searching algorithm (A* atau UCS): ')
    while temp != 'A*' and temp != 'UCS':
        print('Algorithm not found, please insert a different value')
        temp = input('Insert searching algorithm (A* atau UCS): ')

    if temp == 'A*':
        came_from, cost_so_far = astarmap(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
        path, total_cost = returnRoute(start, goal, came_from, cost_so_far)
    else:
        came_from, cost_so_far = ucs(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
        path, total_cost = returnRoute(start, goal, came_from, cost_so_far)
    
    m = folium.Map(location=[nodes[start]['lat'], nodes[start]['lon']], zoom_start=16)

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
    
    m.save('bin/map.html')
    app = QtWidgets.QApplication([])
    map_app = MapApp(path, total_cost)
    map_app.show()
    app.exec_()

def maingraph():
    maps=input ("Insert input file name (without extension): ")
    mapsname = "test/"+maps+".txt"
    nodes = parsegraph(mapsname)
    print('list of nodes: ')
    print(list(nodes.keys()))
    start = input('Insert start node: ')
    while start not in nodes:
        print('Node is not found, please insert a different value')
        start = input('Insert start node: ')

    goal = input('Insert goal node: ')
    while goal not in nodes:
        print('Node is not found, please insert a different value')
        goal = input('Insert goal node: ')

    temp = input('insert searching algorithm (A* atau UCS): ')
    while temp != 'A*' and temp != 'UCS':
        print('Algorithm not found, please insert a different value')
        temp = input('Insert searching algorithm (A* atau UCS): ')
    if temp == 'A*':
        came_from, cost_so_far = astargraph(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
        path, total_cost = returnRoute(start, goal, came_from, cost_so_far)
    else:
        came_from, cost_so_far = ucs(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
        path, total_cost = returnRoute(start, goal, came_from, cost_so_far)
    # create the graph
    fig, ax = plt.subplots()
    for node in nodes:
        x = nodes[node]['x']
        y = nodes[node]['y']
        edges = nodes[node]['edges']
        for neighbor in edges:
            neighbor_x = nodes[neighbor]['x']
            neighbor_y = nodes[neighbor]['y']
            ax.plot([x, neighbor_x], [y, neighbor_y], color='black')
        ax.scatter(x, y, color='blue', s=100)
        ax.annotate(node, (x, y))
    if path:
        for i in range(len(path)-1):
            current_node = path[i]
            next_node = path[i+1]
            current_x = nodes[current_node]['x']
            current_y = nodes[current_node]['y']
            next_x = nodes[next_node]['x']
            next_y = nodes[next_node]['y']
            ax.plot([current_x, next_x], [current_y, next_y], color='red', linewidth=3)
    ax.set_aspect('equal')
    plt.show()


if __name__ == '__main__':
    temp = input("insert '1' to use a geographical coordinate or '2' to use a cartesian coordinate: ")
    while temp != '1' and temp != '2':
        print('Input not found, please try again')
        temp = input("insert '1' to use a geographical coordinate or '2' to use a cartesian coordinate: ")
    if temp == '1':
        mainmap()
    else:
        maingraph()