import heapq

def euclidean_distance(start, goal):
    return ((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2) ** 0.5

def a_star(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start)) # (f_score, node)
    g_score = {start: 0}
    explored = set()

    while frontier:
        f_score, node = heapq.heappop(frontier)

        if node == goal:
            return g_score[node]

        explored.add(node)

        for neighbor, neighbor_cost in graph[node].items():
            tentative_g_score = g_score[node] + neighbor_cost

            if neighbor in explored and tentative_g_score >= g_score.get(neighbor, float("inf")):
                continue

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + euclidean_distance(neighbor, goal)
                heapq.heappush(frontier, (f_score, neighbor))

    return float("inf")
