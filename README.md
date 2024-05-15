

---
-
# Thông Tin Cá Nhân

- **Họ tên:** Vũ Công Anh
- **MSSV:** K205480106003
- **Lớp:** K56kmt
- **Tên môn học:** Lập Trình Python

# Thông Tin Dự Án

- **Tên dự án:** Hệ Thống Giám Sát Chất Lượng Không Khí

## Yêu Cầu/Chức Năng Của Project
1. Thu thập dữ liệu chất lượng không khí (PM2.5, CO2) từ api.
2. Lưu trữ dữ liệu vào cơ sở dữ liệu MySQL.
3. Tạo API để truy xuất dữ liệu qua FastAPI.
4. Tự động thu thập và xử lý dữ liệu với Node-RED.
5. Xây dựng giao diện web để hiển thị dữ liệu dưới dạng biểu đồ và bảng.

# Công Nghệ Sử Dụng

1. **Cơ sở dữ liệu: MySQL**
   - Tạo các bảng `Sensors` và `Readings`.
   - Sử dụng stored procedure `SP_AddReading` để thêm dữ liệu vào bảng `Readings`.
   - **Bảng `Sensors`**:
     - `id` (Primary Key)
     - `name`
     - `location`
   - **Bảng `Readings`**:
     - `id` (Primary Key)
     - `sensor_id` (Foreign Key)
     - `pm25`
     - `co2`
     - `timestamp`
   - **Stored Procedure `SP_AddReading`**:
     ```sql
     CREATE PROCEDURE SP_AddReading(
         IN p_sensor_id INT,
         IN p_pm25 FLOAT,
         IN p_co2 FLOAT,
         IN p_timestamp DATETIME
     )
     BEGIN
         INSERT INTO Readings (sensor_id, pm25, co2, timestamp)
         VALUES (p_sensor_id, p_pm25, p_co2, p_timestamp);
     END;
     ```

2. **Module đọc dữ liệu: Python + FastAPI**
   - **Python**: Viết mã để thu thập dữ liệu từ web API (ví dụ: OpenWeatherMap API).
   - **FastAPI**: Tạo API để nhận và xử lý dữ liệu từ web API và lưu dữ liệu vào MySQL.
   - **requests**: Thư viện Python để gửi yêu cầu HTTP và lấy dữ liệu từ web API.
   - **mysql-connector-python**: Thư viện để kết nối và tương tác với MySQL từ Python.
   - **NSSM (Non-Sucking Service Manager)**: Công cụ để đóng gói và quản lý FastAPI dưới dạng một dịch vụ trên Windows.

3. **Node-RED**
   - Thiết lập luồng để tự động gọi API FastAPI mỗi 10 giây.
   - Sử dụng **HTTP Request Node** để gửi yêu cầu HTTP đến API FastAPI và nhận dữ liệu.
   - Sử dụng **Function Node** để xử lý dữ liệu trước khi lưu vào MySQL.
   - Sử dụng **MySQL Node** để gọi stored procedure `SP_AddReading` và lưu dữ liệu vào MySQL.

4. **Web Application**
   - **HTML**: Tạo cấu trúc trang web.
   - **CSS**: Tạo kiểu cho trang web.
   - **JavaScript**: Tạo các tương tác động trên trang web.
   - **Chart.js**: Thư viện để vẽ biểu đồ hiển thị dữ liệu chất lượng không khí.
   - **Fetch API**: Giao diện để thực hiện các yêu cầu HTTP từ trình duyệt và lấy dữ liệu từ server.

---


![Sơ đồ tổng quát hệ thống](C:/Users/chinh/Downloads/1.png)

