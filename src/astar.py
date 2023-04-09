import heapq
from extras import calculate_distance

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