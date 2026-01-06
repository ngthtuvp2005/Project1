# Hệ thống tìm đường đi đơn giản

## Mô tả
Web đơn giản cho phép tìm đường đi ngắn nhất giữa 2 điểm trên bản đồ thành phố Hà Nội

## Hướng dẫn cài đặt

### 1. Yêu cầu:
* Node.js 20+
* Python 3.10+

### 2. Cài đặt và chạy
1) Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
* Do cần tải dữ liệu bản đồ nên việc hoàn thành khởi động backend có thể mất tới 5-7 phút trước khi đi vào hoạt động.
2) Frontend
```bash
# Vào thư mục frontendpy
cd frontend
npm install
npm run dev
```
Mở trình duyệt tại: http://localhost:5173
