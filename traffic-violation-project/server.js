const express = require('express'); // Import thư viện Express để tạo ứng dụng web
const mysql = require('mysql2/promise'); // Import mysql2 với hỗ trợ Promise để kết nối cơ sở dữ liệu MySQL
const cors = require('cors'); // Import CORS để cho phép truy cập từ các nguồn khác nhau
const app = express(); // Khởi tạo một ứng dụng Express

app.use(cors()); // Sử dụng middleware CORS để cho phép mọi nguồn truy cập vào API
app.use(express.json()); // Sử dụng middleware để phân tích dữ liệu JSON từ yêu cầu

// Cấu hình kết nối cơ sở dữ liệu
const dbConfig = {
    host: 'localhost', // Địa chỉ máy chủ MySQL
    user: 'root', // Tên người dùng MySQL
    password: 'haohiep296', // Mật khẩu của người dùng MySQL
    database: 'traffic_violations' // Tên cơ sở dữ liệu sử dụng trong ứng dụng
};

// API endpoint: Kiểm tra vi phạm theo biển số xe
app.get('/api/violations/:licensePlate', async (req, res) => {
    try {
        const connection = await mysql.createConnection(dbConfig); // Kết nối đến cơ sở dữ liệu với cấu hình đã định nghĩa
        const licensePlate = req.params.licensePlate; // Lấy biển số xe từ URL parameters

        // Query violations
        const [results] = await connection.execute(`
            SELECT 
                violation_time
            FROM violations
            WHERE license_plate = ?
        `, [licensePlate]); // Thực hiện truy vấn để lấy thời gian vi phạm từ bảng 'violations' theo biển số xe (license_plate)

        if (results.length === 0) { // Kiểm tra nếu không có kết quả nào cho biển số xe
            return res.status(404).json({
                message: 'Không tìm thấy thông tin vi phạm cho biển số xe' // Trả về mã lỗi 404 nếu không có vi phạm nào
            });
        }

        // Format thời gian vi phạm
        const violations = results.map(r => ({
            time: new Date(r.violation_time).toLocaleString('en-GB') // Định dạng thời gian vi phạm thành dd/mm/yyyy, hh:mm:ss
        }));

        const response = {
            licensePlate: licensePlate, // Gán biển số xe vào response
            violations: violations // Gán danh sách vi phạm đã định dạng vào response
        };

        res.json(response); // Trả về response dưới dạng JSON
        await connection.end(); // Đóng kết nối cơ sở dữ liệu

    } catch (error) {
        console.error(error); // Log lỗi ra console nếu có lỗi xảy ra
        res.status(500).json({
            message: 'Lỗi server' // Trả về mã lỗi 500 nếu có lỗi server
        });
    }
});

const PORT = 3000; // Đặt cổng cho server là 3000
app.listen(PORT, () => {
    console.log(`Server đang chạy tại http://localhost:${PORT}`); // In thông báo server đang chạy lên console
});
