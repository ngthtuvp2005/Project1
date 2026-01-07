from collections import deque

def solve_bfs(G, start_node, end_node, avg_speed_kmh=40):
    queue = deque([start_node])
    visited = {start_node}      
    parent = {start_node: None}   
    found = False
    
    # 1. Chạy BFS (Tìm đường ít cạnh nhất)
    while queue:
        current_node = queue.popleft() 
        if current_node == end_node:
            found = True
            break
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)
                
    if found:
        # Truy vết đường đi
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path = path[::-1] 
        
        # 2. Tính toán thời gian (Để đồng bộ format return)
        # BFS không dùng penalty để tìm đường, nhưng ta vẫn tính thời gian thực tế của đường đó
        total_seconds = 0
        if len(path) > 1:
            speed_ms = avg_speed_kmh / 3.6
            
            for u, v in zip(path[:-1], path[1:]):
                if G.has_edge(u, v):
                    edge_data = G[u][v][0]
                    length = edge_data.get('length', 0)
                    penalty = edge_data.get('penalty', 1.0)
                    
                    total_seconds += (length * penalty) / speed_ms
        
        return path, total_seconds

    else:
        # Trả về format đồng nhất khi không tìm thấy đường
        return [], 0