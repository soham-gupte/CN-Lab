import heapq

class Routing:
    def __init__(self, router_id, ip_address):
        self.router_id = router_id
        self.ip_address = ip_address
        self.adjacent_routers = {}

    def add_adjacent_router(self, router, cost):
        self.adjacent_routers[router] = cost

    def dijkstra(self, graph, start, main_distances):
        # Initialize distances with infinity for all nodes except the start node
        distances = {node: float('inf') for node in graph}
        distances[start] = 0

        # Priority queue to select the node with the smallest distance
        priority_queue = [(0, start)]

        while priority_queue:
            # Get the node with the smallest distance
            current_distance, current_node = heapq.heappop(priority_queue)

            # If the current distance is larger than the known distance, skip
            if current_distance > distances[current_node]:
                continue

            # Check neighbors and update distances
            for neighbor in graph[current_node]:
                distance = distances[current_node] + main_distances[(current_node, neighbor)]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

if __name__ == '__main__':
    routers = {}

    network_topology = {
        "1": ["2"],
        "2": ["1", "3", "5"],
        "3": ["2", "4"],
        "4": ["3", "5","6"],
        "5": ["2", "4","6"],
        "6": ["4", "5"],
    }

    distances = {
        ("1", "2"): 1,
        ("2", "1"): 1,
        ("2", "3"): 1,
        ("3", "2"): 1,
        ("2", "5"): 1,
        ("5", "2"): 1,
        ("3", "4"): 1,
        ("4", "3"): 1,
        ("4", "5"): 1,
        ("5", "4"): 1,
        ("4", "6"): 1,
        ("6", "4"): 1,
        ("5", "6"): 1,
        ("6", "5"): 1,
    }

    router_id = [None, "172.10.1.1", "172.10.2.2", "172.10.3.3", "172.10.4.4", "172.10.5.5", "172.10.6.6"] 

    for k in network_topology.keys() :
        routers[k] = Routing(k, router_id[int(k)])

    for router in routers.values() :
        for neighbor in network_topology[router.router_id] :
            router.add_adjacent_router(neighbor, distances[(router.router_id, neighbor)])

    # for router in routers.values():
    #     shortest_paths = router.dijkstra(network_topology, router.router_id, distances)
    #     print("Shortest paths from {}: {}".format(router.router_id,shortest_paths))

    for router in routers.values() :
        shortest_paths = router.dijkstra(network_topology, router.router_id, distances)
        print(f"\nPaths from router {router.router_id}:")
        print("Dest.  Router_IP    Cost")
        for k, v in shortest_paths.items() :
            print(f"{k}     {router_id[int(k)]}      {v}")
