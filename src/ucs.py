import heapq

def ucs(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start)) # (cost, node)
    explored = set()

    while frontier:
        cost, node = heapq.heappop(frontier)

        if node == goal:
            return cost

        explored.add(node)

        for neighbor, neighbor_cost in graph[node].items():
            if neighbor not in explored:
                heapq.heappush(frontier, (cost + neighbor_cost, neighbor))

    return float("inf")
