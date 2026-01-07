import { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, Polyline, Polygon, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './App.css';
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import shadow from 'leaflet/dist/images/marker-shadow.png';

L.Marker.prototype.options.icon = L.icon({
    iconUrl: icon, shadowUrl: shadow,
    iconSize: [25, 41], iconAnchor: [12, 41]
});

function App() {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [boundary, setBoundary] = useState([]);
  const [algo, setAlgo] = useState("dijkstra");

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/boundary')
      .then(r => r.data.length && setBoundary(r.data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (!start || !end) return;
    setLoading(true); setRes(null);
    axios.post('http://127.0.0.1:8000/api/find-path', { start, end, algorithm: algo })
      .then(r => setRes(r.data))
      .catch(e => console.error(e))
      .finally(() => setLoading(false));
  }, [start, end, algo]);

  const ClickHandler = () => {
    useMapEvents({
      click(e) {
        if (!start) { setStart(e.latlng); setRes(null); }
        else if (!end) { setEnd(e.latlng); }
        else { setStart(e.latlng); setEnd(null); setRes(null); }
      }
    });
    return null;
  };

  return (
    <div className="app-container">
      {/* --- SIDEBAR --- */}
      <div className="sidebar">
        <h1 className="app-title">Bản Đồ Hà Nội</h1>
        
        <div className="control-group">
          <label className="label">Thuật toán</label>
          <select className="select-box" value={algo} onChange={e => setAlgo(e.target.value)}>
            <option value="dijkstra">Dijkstra</option>
            <option value="astar">A*</option>
            <option value="bfs">BFS</option>
          </select>
        </div>

        <div className="status-card">
          <label className="label">Trạng thái</label>
          <div className="status-text">
            {loading ? <span className="status-loading">Đang tính toán...</span> :
             !start ? "Chọn điểm ĐI" :
             !end ? "Chọn điểm ĐẾN" : "Đã tìm thấy đường!"}
          </div>
        </div>
round
        {res && res.status === 'found' && (
          <div className="result-card">phút
             <label className="label">Kết quả</label>
             <div className="result-item"><span>Quãng đường:</span> <span className="result-value">{(res.distance/1000).toFixed(2)} km</span></div>
             <div className="result-item"><span>Thời gian:</span> <span className="result-value">{Math.round(res.time / 60)} phút</span></div>
             <div className="result-item"><span>Số nút:</span> <span className="result-value">{res.node_count}</span></div>
             
             <div className="legend">
                <div className="legend-item"><div className="color-box" style={{background: '#0984e3'}}></div> Đường đi</div>
                <div className="legend-item"><div className="color-box" style={{background: '#c0392b'}}></div> Ranh giới Hà Nội</div>
             </div>
          </div>
        )}
      </div>

      <div className="map-wrapper">
        <MapContainer center={[21.0285, 105.8542]} zoom={12} scrollWheelZoom={true}>
            <TileLayer url="http://mt0.google.com/vt/lyrs=m&x={x}&y={y}&z={z}" attribution='Google Maps' />
            <ClickHandler />

            {boundary.length > 0 && (
                <Polygon 
                    positions={boundary.map(p => [p.lat, p.lng])} 
                    pathOptions={{ 
                        color: '#c0392b', 
                        weight: 4,       
                        fillOpacity: 0.05 
                    }} 
                />
            )}
            
            {start && <Marker position={start}><Popup>Điểm Đi</Popup></Marker>}
            {end && <Marker position={end}><Popup>Điểm Đến</Popup></Marker>}

            {res?.path_segments?.map((seg, i) => (
                <Polyline 
                  key={i} 
                  positions={seg.coords.map(p => [p.lat, p.lng])} 
                  pathOptions={{ 
                    color: seg.type === 'tunnel' ? '#636e72' : '#0984e3', 
                    weight: seg.type === 'bridge' ? 10 : 7, 
                    opacity: 1.0,
                    dashArray: seg.type === 'tunnel' ? '10, 10' : null 
                  }} 
                />
            ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default App;