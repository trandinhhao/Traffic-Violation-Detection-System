const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// Cấu hình kết nối cơ sở dữ liệu
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'traffic_violations'
};

// API endpoint: Kiểm tra vi phạm theo biển số xe
app.get('/api/violations/:licensePlate', async (req, res) => {
    try {
        const connection = await mysql.createConnection(dbConfig);
        const licensePlate = req.params.licensePlate;

        // Query violations
        const [results] = await connection.execute(`
            SELECT 
                violation_time
            FROM violations
            WHERE license_plate = ?
        `, [licensePlate]);

        if (results.length === 0) {
            return res.status(404).json({
                message: 'Không tìm thấy thông tin vi phạm cho biển số xe'
            });
        }

        // Format thời gian vi phạm
        const violations = results.map(r => ({
            time: new Date(r.violation_time).toLocaleString('en-GB') // Định dạng dd/mm/yyyy, hh:mm:ss
        }));

        const response = {
            licensePlate: licensePlate,
            violations: violations
        };

        res.json(response);
        await connection.end();

    } catch (error) {
        console.error(error);
        res.status(500).json({
            message: 'Lỗi server'
        });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server đang chạy tại http://localhost:${PORT}`);
});
