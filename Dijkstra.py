def dijkstra(graph, start):
    #Initialization
    unvisited_nodes = list(graph.keys())  # All nodes are initially unvisited
    distances = {node: float('inf') for node in graph}  # Set all distances to infinity
    distances[start] = 0  # Distance to the start node is 0
    previous_nodes = {node: None for node in graph}  # Tracks the path
    
    # While there are unvisited nodes
    while unvisited_nodes:
        #Select the unvisited node with the smallest distance
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        
        # If the smallest distance is infinity, the remaining nodes are not connected
        if distances[current_node] == float('inf'):
            break
        
        #Check all unvisited neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            if neighbor in unvisited_nodes:  # Only consider unvisited neighbors
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance  # Update distance
                    previous_nodes[neighbor] = current_node  # Update the path
        
        #Mark the current node as visited
        unvisited_nodes.remove(current_node)

    return distances, previous_nodes

#graph
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Starting node
start_node = 'A'
distances, previous_nodes = dijkstra(graph, start_node)

# Printing the results
print("Shortest distances from node A:")
for node, distance in distances.items():
    print(f"Distance to {node}: {distance}")

print("\nPaths:")
for node in graph:
    path = []
    current = node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    print(f"Path to {node}: {' -> '.join(path)}")