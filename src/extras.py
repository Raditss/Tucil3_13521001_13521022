from math import radians, sin, cos, sqrt, atan2

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    distance = R*c

    return distance

def printRoute(start, goal, came_from, cost_so_far):
    current = goal
    path = [current]
    total_cost = cost_so_far[current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    total_cost = round(total_cost, 3)
    print(f"Route: {' -> '.join(path)}")
    print(f"Distance: {total_cost} KM")