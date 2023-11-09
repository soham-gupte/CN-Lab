class Router:
    def __init__(self, name):
        self.name = name
        self.routing_table = {}
        
    def update_routing_table(self, destination, distance, next_hop):
        self.routing_table[destination] = (distance, next_hop)
        
    def display_routing_table(self):
        print(f"\nRouting Table for Router {self.name}:")
        print("Destn\t\tCost\t\tNext Hop")
        for destination, (distance, next_hop) in self.routing_table.items():
            print(f"{destination}\t\t{distance}\t\t{next_hop}")

# Define the network topology and distances
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


routers = {}
for router_name in network_topology:
    routers[router_name] = Router(router_name)

for router_name in routers:
    router = routers[router_name]
    for destination in network_topology:
        if destination == router_name:
            router.update_routing_table(destination, 0, destination)  # Set distance to 0 for the router itself
        elif destination in network_topology[router_name]:
            neighbor = destination
            neighbor_distance = distances[(router_name, neighbor)]
            router.update_routing_table(neighbor, neighbor_distance, neighbor)
        else:
            router.update_routing_table(destination, float("inf"), None)  # Set distance to infinity for unreachable destinations

# Display initial routing tables
print("Initial Routing Tables:")
for router_name in routers:
    routers[router_name].display_routing_table()

# Simulate RIP updates
for i in range(3):  # Simulate updates 3 times
    for router_name in routers:
        router = routers[router_name]
        for destination in network_topology:
            if destination != router_name:
                min_distance = float("inf")
                next_hop = None
                for neighbor in network_topology[router_name]:
                    neighbor_router = routers[neighbor]
                    if destination in neighbor_router.routing_table:
                        distance = distances[(router_name, neighbor)] + neighbor_router.routing_table[destination][0]
                        if distance < min_distance:
                            min_distance = distance
                            next_hop = neighbor
                router.update_routing_table(destination, min_distance, next_hop)
    print(f"\nAfter {i}th iteration: \n")
    for router_name in routers:
        routers[router_name].display_routing_table()
    print("______________________________________________________\n")
