const mysql = require('mysql2/promise');
const fs = require('fs');

// Cấu hình kết nối cơ sở dữ liệu
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: 'haohiep296',
    database: 'traffic_violations'
};

// Hàm xử lý từng dòng CSV
async function processRow(connection, line) {
    // In ra dữ liệu để kiểm tra
    console.log('Dữ liệu từ CSV:', line);

    // Lấy các giá trị từ dòng CSV
    const parts = line.split(',');
    if (parts.length !== 2) {
        console.log('Dòng không hợp lệ:', line);
        return;
    }

    const license_plate = parts[0].trim();
    const violation_time = parts[1].trim();

    try {
        // Kiểm tra xem vi phạm này đã tồn tại chưa
        const [existingViolation] = await connection.execute(
            'SELECT id FROM violations WHERE license_plate = ? AND violation_time = ?',
            [license_plate, violation_time]
        );

        if (existingViolation.length === 0) {
            // Nếu chưa có thì thêm vào bảng violations
            await connection.execute(
                'INSERT INTO violations (license_plate, violation_time) VALUES (?, ?)',
                [license_plate, violation_time]
            );
            console.log('Đã thêm vi phạm mới:', { license_plate, violation_time });
        } else {
            console.log('Bỏ qua - Vi phạm đã tồn tại:', { license_plate, violation_time });
        }
    } catch (error) {
        console.error('Lỗi khi xử lý dòng:', { license_plate, violation_time }, error);
    }
}

// Hàm nhập dữ liệu từ file CSV vào bảng violations
async function importViolations() {
    const connection = await mysql.createConnection(dbConfig);

    // Đọc toàn bộ nội dung file CSV
    const fileContent = fs.readFileSync('valid_plate.csv', 'utf-8');
    const lines = fileContent.split('\n');

    // Xử lý từng dòng trong file CSV
    for (const line of lines) {
        if (line.trim()) {  // Chỉ xử lý các dòng không rỗng
            await processRow(connection, line);
        }
    }

    console.log('Đã xử lý xong file CSV');
    await connection.end();
}

// Gọi hàm để bắt đầu nhập dữ liệu
importViolations();
