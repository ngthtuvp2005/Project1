import os, time
import uvicorn
import osmnx as ox
import networkx as nx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager

from algorithms.dijkstra import solve_dijkstra
from algorithms.astar import solve_astar
from algorithms.bfs import solve_bfs

ox.settings.max_query_area_size = 125000000000
ox.settings.requests_timeout = 300 
PLACE_NAME = "Hanoi, Vietnam"
FILENAME = "hanoi_final_v2.graphml"
G = None
BOUNDARY_COORDS = [] 

def load_map():
    global G, BOUNDARY_COORDS
    print(f"Server đang khởi động... Đang xử lý: {PLACE_NAME}")

    try:
        gdf = ox.geocode_to_gdf(PLACE_NAME)
        geom = gdf.geometry.iloc[0]
        if geom.geom_type == 'MultiPolygon': geom = max(geom.geoms, key=lambda x: x.area)
        BOUNDARY_COORDS[:] = [{"lat": y, "lng": x} for x, y in geom.exterior.coords]
        print("Đã tải xong viền ranh giới.")
    except Exception: print("Cảnh báo: Không tải được viền.")

    if os.path.exists(FILENAME):
        G = ox.load_graphml(FILENAME)
        print("Đã đọc dữ liệu bản đồ.")
    else:
        print("Chưa có dữ liệu, đang tải dữ liệu bản đồ mới...")
        cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|unclassified|residential"]'
        G = ox.graph_from_place(PLACE_NAME, custom_filter=cf, simplify=True)
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        ox.save_graphml(G, FILENAME)
        print("Tải bản đồ thành công.")
    
    print(f"Server Sẵn sàng! Tổng số {len(G.nodes)} nút.")
    
    for u, v, k, data in G.edges(keys=True, data=True):
        length = data.get("length", 1)

        highway = data.get("highway", "")
        if isinstance(highway, list):
            highway = highway[0]

        penalty = 1.0

        if highway in ["residential", "service"]:
            penalty = 1.5
        elif highway in ["motorway", "trunk"]:
            penalty = 0.8

        if data.get("bridge"):
            penalty *= 1.2

        if data.get("tunnel"):
            penalty *= 1.1

        data["penalty"] = penalty
        data["weight"] = length * penalty


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_map()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class PathRequest(BaseModel):
    start: dict
    end: dict
    algorithm: str = "dijkstra"

@app.get("/api/boundary")
def get_boundary():
    return BOUNDARY_COORDS

@app.post("/api/find-path")
def find_path(req: PathRequest):
    if G is None: raise HTTPException(503, "Server đang khởi động...")
    try:
        orig = ox.nearest_nodes(G, req.start['lng'], req.start['lat'])
        dest = ox.nearest_nodes(G, req.end['lng'], req.end['lat'])

        algos = {"dijkstra": solve_dijkstra, "astar": solve_astar, "bfs": solve_bfs}
        solve_func = algos.get(req.algorithm.lower())
        if not solve_func: raise HTTPException(400, "Thuật toán không hỗ trợ")

        t_start = time.time()
        path_nodes = solve_func(G, orig, dest)
        exec_time = time.time() - t_start

        if not path_nodes: return {"status": "not_found"}

        segments = []
        for u, v in zip(path_nodes[:-1], path_nodes[1:]):
            data = G.get_edge_data(u, v)[0]
            stype = "road"
            if data.get('bridge') not in [None, 'no', 'false']: stype = "bridge"
            elif data.get('tunnel') not in [None, 'no', 'false']: stype = "tunnel"
            
            coords = []
            if 'geometry' in data:
                coords = [{"lat": y, "lng": x} for x, y in zip(*data['geometry'].xy)]
            else:
                coords = [{"lat": G.nodes[n]['y'], "lng": G.nodes[n]['x']} for n in (u, v)]
            segments.append({"type": stype, "coords": coords})

        dist = nx.path_weight(G, path_nodes, weight='length')
        return {
            "status": "found",
            "path_segments": segments,
            "distance": round(dist, 2),
            "node_count": len(path_nodes),
            "time": round(exec_time, 4)
        }
    except Exception as e:
        print(f"Lỗi: {e}")
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)