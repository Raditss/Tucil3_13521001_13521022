import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Fungsi untuk membaca file graf
def read_graph(filename):
    with open(filename, 'r') as file:
        graph = [[int(num) for num in line.split()] for line in file]
    return graph

# Fungsi untuk menampilkan peta/graf
def draw_graph(graph, shortest_path=[]):
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    scene = QGraphicsScene()
    view = QGraphicsView(scene)
    layout.addWidget(view)
    window.setLayout(layout)

    # Menggambar simpul pada peta
    node_size = 20
    node_brush = QBrush(Qt.white)
    node_pen = QPen(Qt.black)
    node_font = QFont('Arial', 10)
    node_text_offset = QPointF(node_size/2, node_size/2)
    for i in range(len(graph)):
        node = QGraphicsEllipseItem(i*node_size, 0, node_size, node_size)
        node.setBrush(node_brush)
        node.setPen(node_pen)
        node.setPos(i*node_size, 0)
        scene.addItem(node)
        node_label = QGraphicsTextItem(str(i))
        node_label.setFont(node_font)
        node_label.setDefaultTextColor(Qt.black)
        node_label.setPos(i*node_size + node_text_offset.x(), node_text_offset.y())
        scene.addItem(node_label)

    # Menggambar sisi pada peta
    edge_pen = QPen(Qt.black)
    edge_pen.setWidth(2)
    for i in range(len(graph)):
        for j in range(i+1, len(graph)):
            if graph[i][j] > 0:
                edge = QGraphicsLineItem(i*node_size + node_size/2, node_size/2,
                                         j*node_size + node_size/2, node_size/2)
                edge.setPen(edge_pen)
                scene.addItem(edge)

    # Menandai simpul pada lintasan terpendek dengan warna merah
    if shortest_path:
        path_pen = QPen(Qt.red)
        path_pen.setWidth(4)
        for i in range(len(shortest_path)-1):
            path = QGraphicsLineItem(shortest_path[i]*node_size + node_size/2, node_size/2,
                                      shortest_path[i+1]*node_size + node_size/2, node_size/2)
            path.setPen(path_pen)
            scene.addItem(path)

    window.show()
    sys.exit(app.exec_())

# Fungsi untuk menghitung jarak antara dua simpul
def get_distance(coord1, coord2):
    return ((coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2)**0.5

# Fungsi untuk mencari lintasan terpendek menggunakan algoritma UCS
def ucs(graph, start, end):
    # Inisialisasi variabel
    n = len(graph)
    visited = [False]*n
    distance = [float('inf')]*n
    distance[start] = 0
    path = [-1]*n
    heap = [(0, start)]

    # Loop utama algoritma UCS
    while heap:
        (cost, curr) = heappop(heap)
        if visited[curr]:
            continue
        visited[curr] = True
        if curr == end:
            break
        for neighbor in range(n):
           
