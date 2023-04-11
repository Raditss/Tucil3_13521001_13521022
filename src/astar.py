import heapq
from extras import calculate_distance, euclidianDist

def astarmap(start, goal, graph):
    # Initialize the frontier priority queue and dictionaries to store path and cost information
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    # Loop until the goal node is found or the frontier is empty
    while frontier:
        # Pop the node with the lowest estimated total cost from the priority queue
        current = heapq.heappop(frontier)[1]
        
        # Check if the goal node has been reached
        if current == goal:
            break
        
        # Loop through the neighbors of the current node
        for next in graph[current]['edges']:
            # Calculate the new cost to reach the neighbor
            new_cost = cost_so_far[current] + graph[current]['edges'][next]
            
            # If the neighbor hasn't been visited or the new cost is lower than the previous cost, update the dictionaries
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                # Calculate the estimated total cost of the path through the neighbor to the goal
                priority = new_cost + calculate_distance(graph[next]['lat'],graph[goal]['lat'],graph[next]['lon'],graph[goal]['lon'])
                # Add the neighbor to the frontier with its estimated total cost
                heapq.heappush(frontier, (priority, next))
                # Store the parent node of the neighbor in the search tree
                came_from[next] = current
    if goal not in came_from:
        raise Exception("No path found from start to goal")
    # Return the path and cost information dictionaries
    return came_from, cost_so_far

def astargraph(start, goal, graph):
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
    if goal not in came_from:
        raise Exception("No path found from start to goal")
    return came_from, cost_so_far
