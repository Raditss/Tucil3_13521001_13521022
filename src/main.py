from parse import parse
from astar import astar
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

        a = f"Route: {' -> '.join(path)}"
        b = f"Distance: {total_cost} KM"
        text = f"{a}\n{b}"
        self.textbox.setPlainText(text)
        self.webview.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath
        ("bin/map.html")))

def main():
    maps=input ("Masukkan nama file input (tanpa extension): ")
    mapsname = "test/"+maps+".txt"
    nodes = parse(mapsname)
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
        came_from, cost_so_far = astar(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
        path, total_cost = returnRoute(start, goal, came_from, cost_so_far)
    else:
        came_from, cost_so_far = ucs(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
        path, total_cost = returnRoute(start, goal, came_from, cost_so_far)
    
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
    
    m.save('bin/map.html')
    app = QtWidgets.QApplication([])
    map_app = MapApp(path, total_cost)
    map_app.show()
    app.exec_()


if __name__ == '__main__':
    main()