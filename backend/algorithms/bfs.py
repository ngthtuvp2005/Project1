from collections import deque

def solve_bfs(G, start_node, end_node):
    queue = deque([start_node])
    visited = {start_node}      
    parent = {start_node: None}   
    found = False
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
        path = []
        curr = end_node
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        return path[::-1] 
    else:
        return [] 