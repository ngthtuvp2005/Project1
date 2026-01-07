import heapq

def solve_dijkstra(G, start_node, end_node, avg_speed_kmh = 40):
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
            edge_data_dict = G.get_edge_data(current_node, neighbor)
            edge_data = next(iter(edge_data_dict.values()))
            weight = edge_data.get('weight', edge_data.get('length', 1))
            new_dist = current_dist + weight
            if new_dist < min_dist[neighbor]:
                min_dist[neighbor] = new_dist
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (new_dist, neighbor))      
    if min_dist[end_node] == float('inf'):
        return [], 0
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr)
    path = path[::-1]

    total_seconds = 0
    if len(path) > 1:
        speed_ms = avg_speed_kmh / 3.6 # Đổi km/h -> m/s
        
        for u, v in zip(path[:-1], path[1:]):
            # Lấy lại thông tin cạnh để tính giờ
            if G.has_edge(u, v):
                # OSMnx là MultiDiGraph, lấy cạnh đầu tiên (key=0)
                edge_data = G[u][v][0] 
                
                length = edge_data.get('length', 0)
                penalty = edge_data.get('penalty', 1.0)
                
                # Công thức: t = (d * p) / v
                total_seconds += (length * penalty) / speed_ms

    return path, total_seconds