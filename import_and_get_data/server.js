const express = require('express'); // Import thư viện Express để tạo ứng dụng web
const mongoose = require('mongoose'); // Import Mongoose để kết nối với MongoDB
const cors = require('cors'); // Import CORS để cho phép truy cập từ các nguồn khác nhau
const app = express(); // Khởi tạo một ứng dụng Express

app.use(cors()); // Sử dụng middleware CORS để cho phép mọi nguồn truy cập vào API
app.use(express.json()); // Sử dụng middleware để phân tích dữ liệu JSON từ yêu cầu

// Kết nối đến MongoDB
mongoose.connect('mongodb://localhost:27017/traffic_violations', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// Định nghĩa Schema cho vi phạm
const violationSchema = new mongoose.Schema({
    license_plate: String,
    violation_time: Date,
    image_data: String // Lưu ảnh dưới dạng Base64
});

// Tạo model
const Violation = mongoose.model('Violation', violationSchema);

// API endpoint: Kiểm tra vi phạm theo biển số xe
app.get('/api/violations/:licensePlate', async (req, res) => {
    try {
        const licensePlate = req.params.licensePlate; // Lấy biển số xe từ URL parameters

        // Tìm kiếm thông tin vi phạm theo biển số xe
        const violations = await Violation.find({ license_plate: licensePlate });

        if (violations.length === 0) { // Kiểm tra nếu không có kết quả nào cho biển số xe
            return res.status(404).json({
                message: 'Không tìm thấy thông tin vi phạm cho biển số xe' // Trả về mã lỗi 404 nếu không có vi phạm nào
            });
        }

        // Chuyển đổi dữ liệu vi phạm thành định dạng cần thiết
        const response = violations.map(v => ({
            license_plate: v.license_plate,
            violation_time: new Date(v.violation_time).toLocaleString('en-GB'), // Định dạng thời gian
            image_data: v.image_data // Dữ liệu hình ảnh
        }));

        res.json(response); // Trả về response dưới dạng JSON

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
