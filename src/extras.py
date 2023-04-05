
def printRoute(start, goal, came_from, cost_so_far):
    current = goal
    path = [current]
    total_cost = cost_so_far[current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    print(f"Route: {' -> '.join(path)}")
    print(f"Total Cost: {total_cost}")