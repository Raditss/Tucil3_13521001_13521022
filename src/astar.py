import networkx as nx
import matplotlib.pyplot as plt
import math
import heapq

def euclidianDist(x1,x2,y1,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def heuristicarr(graph,goal):
    arrHeuristic=[]
    for i in graph:
        arrHeuristic.append((i,euclidianDist(graph[i]['x'],graph[goal]['x'],graph[i]['y'],graph[goal]['y'])))
    return arrHeuristic


def aStar(start, goal, graph):
    arrHeuristic=heuristicarr(graph,goal)
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
                priority = new_cost + euclidianDist(graph[next]['x'],graph[goal]['x'],graph[next]['y'],graph[goal]['y'])
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    return came_from, cost_so_far
