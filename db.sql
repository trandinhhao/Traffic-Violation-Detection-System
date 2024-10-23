CREATE DATABASE traffic_violations;
USE traffic_violations;

-- Tạo bảng vi phạm
CREATE TABLE violations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20),
    violation_time DATETIME NOT NULL
);

-- Data test
INSERT INTO violations (license_plate, violation_time) VALUES
('29AA-77509', '2024-10-16 17:21:18'),
('29A-77509', '2024-10-16 17:21:20'),
('295-14262', '2024-10-16 17:21:21');
