import heapq

def ucs(start, goal, graph):
    # Initialize the frontier priority queue and dictionaries to store path and cost information
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    # Loop until the goal node is found or the frontier is empty
    while frontier:
        # Pop the node with the lowest cost so far from the priority queue
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
                priority = new_cost
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
    if goal not in came_from:
        raise Exception("No path found from start to goal")
    # Return the path and cost information dictionaries
    return came_from, cost_so_far
