import heapq

 # reading our graph from a file
def read_file_graph(file):
    graph = []
    with open(file,"r") as f:
        for line in f:
            row = [ tuple(map(float, triplet.split())) for triplet in line.strip().split('|') ]
            graph.append(row)

    return graph

def update_graph(graph, u, v, distance, delay_time, fuel_consumption):
     #Update the graph with new edge information.
    while len(graph) <= u:
        graph.append([])

    while len(graph[u]) <= v:
        graph[u].append((0,0,0))

    graph[u][v] = (distance, delay_time, fuel_consumption)
    return graph

def write_txt_graph(graph, file):
    with open(file, 'w') as f:
        for row in graph:
            line = ' | '.join(' '.join(map(str, triplet)) for triplet in row)
            f.write(line + '\n')

 # total cost for a given path
def calculate_cost(distance, delay_time, fuel_consumption=0.05, fuel_price=1.8):
       #calculating the total cost for a path
    fuel_cost = distance * fuel_consumption * fuel_price
    traffic_cost = (0.0082 * delay_time) + (0.052 * delay_time) + (0.0174 * delay_time)

    return traffic_cost + fuel_cost


 # Dijkstra's algorithm
def Dijkstras(graph, start, end):
    n = len(graph)
    min_heap = [(0,start)]
    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    parent = {i: None for i in range(n)}

    while min_heap: #while min_heap is non-empty (true)
        current_cost, current_node = heapq.heappop(min_heap)  #we get the node with the smallest cost

         #if we meet the destination, we stop (break)
        if current_node == end:
            break

         #let's check the neighbours of the current node
        for neighbour, (distance, delay_time, fuel_consumption) in enumerate(graph[current_node]):
            if distance == 0:
                continue

             #lets calculate the total cost taken to reach the neighbour
            cost = calculate_cost(distance, delay_time, fuel_consumption)
            new_cost = current_cost + cost

               #we want the shortest path
            if new_cost < distances[neighbour]:
                distances[neighbour] = new_cost
                parent[neighbour] = current_node
                heapq.heappush(min_heap,(new_cost,neighbour)) #we update the heap

    if distances[end] == float('inf'):
        print(f"No path exist from node {start} to node {end}.")
        return [], float('inf')

     #reconstruct the path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]

    if path[-1] != start:
        print(f"No path exists between node {start} and node {end}.")
        return[], float('inf')


    return path[::-1], distances[end]


   #the case of multiple destinations
# def MultiDestination(graph, start, list):

#     path1 = [start]

#     while len(list) > 0:
#         _, min = Dijkstras(graph, start, list[0])
#         for x in list:
#             _, cost = Dijkstras(graph, start, x)
#             if cost <= min:
#                 minNode = x

#         start = minNode
#         path1.append(minNode)
#         list.remove(minNode)

#     return path1


def dijkstra(graph, start):
    n = len(graph)
    distances = [float('inf')] * n
    distances[start] = 0
    min_heap = [(0, start)]

    while min_heap:
        current_cost, current_node = heapq.heappop(min_heap)

        if current_cost > distances[current_node]:
            continue

        for neighbour, (distance, delay_time, fuel_consumption) in enumerate(graph[current_node]):
            if distance is None:
                continue
            cost = calculate_cost(distance, delay_time, fuel_consumption)
            new_cost = current_cost + cost
            if new_cost < distances[neighbour]:
                distances[neighbour] = new_cost
                heapq.heappush(min_heap, (new_cost, neighbour))

    return distances


def multiple_destinations(graph, start, destinations):
    total_cost = 0
    path = [start]

    while destinations:
        # Run Dijkstra's algorithm from the current start node
        distances = dijkstra(graph, start)

        # Find the nearest destination
        nearest = None
        nearest_distance = float('inf')
        for destination in destinations:
            if distances[destination] < nearest_distance:
                nearest_distance = distances[destination]
                nearest = destination

        # Update the total cost and path
        total_cost += nearest_distance
        path.append(nearest)

        # Remove the nearest destination from the list
        destinations.remove(nearest)

        # Update the start node for the next iteration
        start = nearest

    return total_cost, path