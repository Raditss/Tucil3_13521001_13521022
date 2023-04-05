def create_graph(filename):
    graph = {}
    with open(filename) as file:
        lines = file.readlines()
        num_nodes = int(lines[0])
        for i in range(1, num_nodes+1):
            node_info = lines[i].strip().split()
            node_name = node_info[0]
            x = int(node_info[1])
            y = int(node_info[2])
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
                    edges[node2_name] = int(row[j])
    return graph

# graph = create_graph("src/text.txt")
# print(graph)