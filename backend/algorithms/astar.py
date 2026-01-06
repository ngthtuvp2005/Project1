import heapq
import math

def euclidean_distance(G, node1_id, node2_id):
    x1 = G.nodes[node1_id]['x']
    y1 = G.nodes[node1_id]['y']
    x2 = G.nodes[node2_id]['x']
    y2 = G.nodes[node2_id]['y']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def solve_astar(G, start_node, end_node):
    priority_queue = [(0, start_node)]
    g_score = {node: float('inf') for node in G.nodes}
    g_score[start_node] = 0
    parent = {start_node: None}
    
    while priority_queue:
        current_f, current_node = heapq.heappop(priority_queue)
        if current_node == end_node:
            break
        for neighbor in G.neighbors(current_node):
            edge_data = G.get_edge_data(current_node, neighbor)[0]
            weight = edge_data.get('length', 0)
            tentative_g = g_score[current_node] + weight
            if tentative_g < g_score[neighbor]:
                parent[neighbor] = current_node
                g_score[neighbor] = tentative_g
                h_score = euclidean_distance(G, neighbor, end_node)
                f_score = tentative_g + h_score
                heapq.heappush(priority_queue, (f_score, neighbor))
    if g_score[end_node] == float('inf'):
        return []
    path = []
    curr = end_node
    while curr is not None:
        path.append(curr)
        curr = parent.get(curr) 
    return path[::-1]