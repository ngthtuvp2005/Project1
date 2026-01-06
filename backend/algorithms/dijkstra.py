import heapq

def solve_dijkstra(G, start_node, end_node):
    priority_queue = [(0, start_node)]
    min_dist = {node: float('inf') for node in G.nodes}
    min_dist[start_node] = 0
    parent = {start_node: None}  
    while priority_queue:
        current_dist, current_node = heapq.heappop(priority_queue)
        if current_node == end_node:
            break
        if current_dist > min_dist[current_node]:
            continue
        for neighbor in G.neighbors(current_node):
            edge_data = G.get_edge_data(current_node, neighbor)[0]
            weight = edge_data.get('length', 0) 
            new_dist = current_dist + weight
            if new_dist < min_dist[neighbor]:
                min_dist[neighbor] = new_dist
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (new_dist, neighbor))      
    if min_dist[end_node] == float('inf'):
        return [] 
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    return path[::-1]