# import heapq

# def dijkstra(graph, start):
#     distances = {node: float('inf') for node in graph}
#     distances[start] = 0
#     queue = [(0, start)]

#     while queue:
#         distance, current_node = heapq.heappop(queue)

#         if distance > distances[current_node]:
#             continue

#         for neighbor in graph[current_node]:
#             new_distance = distance + 1
#             if new_distance < distances[neighbor]:
#                 distances[neighbor] = new_distance
#                 heapq.heappush(queue, (new_distance, neighbor))

#     return distances

def bellman_ford(graph, source):
    # Initialize distances to each node from source to infinity
    distances = [float('inf')] * (len(graph)+1)
    distances[source] = 0
    next_hop = [None] * (len(graph) + 1)

    # Relax edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for u, neighbors in graph.items():
            for neighbor in neighbors:
                if distances[u] + 1 < distances[neighbor]:
                    distances[neighbor] = distances[u] + 1
                    next_hop[neighbor] = u

    # Check for negative cycles
    for u, neighbors in graph.items():
        for neighbor in neighbors:
            if distances[u] + 1 < distances[neighbor]:
                print("Graph contains negative cycles")
                return -1
            
    return distances, next_hop

network = {
    1: [2, 3, 5, 6],
    2: [1, 3],
    3: [1, 2, 4],
    4: [3, 7],
    5: [1],
    6: [1, 7],
    7: [6, 4],
}

n = len(network)

for i in range(n) :
    distances, next_hop = bellman_ford(network, i+1)
    # print(next)
    print(f"\nRouting table for {i+1}:")
    print("Dest Cost NHop")
    for node, distance in enumerate(distances):
        if node not in (i + 1, 0):
            next_hop_node = next_hop[node]
            if next_hop_node is None:
                next_hop_node = "N/A"  # Indicate that there's no valid next hop
            print(f"{node}     {distance}     {next_hop_node}")

# Destination   Cost    NextHop
# Dest Cost NHop
   