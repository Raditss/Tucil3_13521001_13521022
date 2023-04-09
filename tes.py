
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets


class MapApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the entry fields for the bounding box coordinates
        self.lat1_entry = QtWidgets.QLineEdit()
        self.lon1_entry = QtWidgets.QLineEdit()
        self.lat2_entry = QtWidgets.QLineEdit()
        self.lon2_entry = QtWidgets.QLineEdit()

        # Create the button to generate the map
        self.generate_button = QtWidgets.QPushButton("Generate Map")

        # Create the map canvas
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.setHtml(open('map.html').read())

        # Set up the layout
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.browser, 0, 2, 5, 1)

        self.setLayout(grid)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    map_app = MapApp()
    map_app.show()
    app.exec_()
