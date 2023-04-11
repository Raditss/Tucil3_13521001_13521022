from extras import calculate_distance

def parsemap(filename):

    with open(filename) as f:
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

def parsegraph(filename):
    graph = {}
    with open(filename) as file:
        lines = file.readlines()
        num_nodes = int(lines[0])
        for i in range(1, num_nodes+1):
            node_info = lines[i].strip().split()
            node_name = node_info[0]
            x = float(node_info[1])
            y = float(node_info[2])
            edges = {}
            graph[node_name] = {'x': x, 'y': y, 'edges': edges}
        adj_matrix = lines[num_nodes+1:]
        for i in range(num_nodes):
            row = adj_matrix[i].strip().split()
            node1_name = lines[i+1].strip().split()[0]
            edges = graph[node1_name]['edges']
            for j in range(num_nodes):
                if row[j] != '0':
                    node2_name = lines[j+1].strip().split()[0]
                    edges[node2_name] = float(row[j])
    return graph