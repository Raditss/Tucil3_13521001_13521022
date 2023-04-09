from extras import calculate_distance

def parse(input):
    with open(input) as f:
        n = int(f.readline().strip())
        nodes = {}
        for i in range(n):
            name, lat, long = f.readline().strip().split()
            nodes[name] = {'lat': float(lat), 'lon': float(long), 'edges': {}}
        for i in range(n):
            adjacency_matrix_row = list(map(int, f.readline().strip().split()))
            for j in range(n):
                if adjacency_matrix_row[j] == 1:
                    node1 = nodes[list(nodes.keys())[i]]
                    node2 = nodes[list(nodes.keys())[j]]
                    distance = calculate_distance(node1['lat'], node1['lon'], node2['lat'], node2['lon'])
                    nodes[list(nodes.keys())[i]]['edges'][list(nodes.keys())[j]] = distance
    return nodes