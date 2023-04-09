from parse import parse
from astar import aStar
from UCS import ucs
from extras import printRoute
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the map canvas
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setHtml(open('bin/map.html').read())

        # Set up the layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.browser, 0, 2, 5, 1)

        self.setLayout(grid)

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
        came_from, cost_so_far = aStar(start, goal, nodes)
        printRoute(start, goal, came_from, cost_so_far)
    else:
        came_from, cost_so_far = ucs(start, goal, nodes)
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
    
    m.save('bin/map.html')
    app = QtWidgets.QApplication([])
    map_app = MapApp()
    map_app.show()
    app.exec_()


if __name__ == '__main__':
    main()