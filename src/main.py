from parse import create_graph
from Astar import aStar
from USC import usc
from extras import printRoute


graph = create_graph("src/text.txt")
came_from, cost_so_far = aStar('Bahasa', 'GKUT', graph)
printRoute('Bahasa', 'GKUT', came_from, cost_so_far)

x, y = usc('Bahasa', 'GKUT', graph)
printRoute('Bahasa', 'GKUT', x, y)