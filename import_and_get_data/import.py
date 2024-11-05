from pymongo import MongoClient
from datetime import datetime
import base64

# Kết nối với MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['traffic_violations']
violations_collection = db['violations']

# Hàm thêm vi phạm mới
def add_violation(license_plate, violation_time, image_path):
    try:
        # Kiểm tra xem vi phạm này đã tồn tại chưa
        existing_violation = violations_collection.find_one({
            "license_plate": license_plate,
            "violation_time": violation_time
        })

        if not existing_violation:
            # Đọc và mã hóa hình ảnh dưới dạng Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            # Tạo vi phạm mới
            violation = {
                "license_plate": license_plate,
                "violation_time": violation_time,
                "image_data": image_data,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

            # Lưu vào database
            violations_collection.insert_one(violation)
            print('Đã thêm vi phạm mới:', {"license_plate": license_plate, "violation_time": violation_time})
            return {"success": True, "message": "Đã thêm vi phạm mới"}
        else:
            print('Bỏ qua - Vi phạm đã tồn tại:', {"license_plate": license_plate, "violation_time": violation_time})
            return {"success": False, "message": "Vi phạm đã tồn tại"}
    except Exception as error:
        print('Lỗi khi thêm vi phạm:', error)
        return {"success": False, "message": "Lỗi khi thêm vi phạm", "error": str(error)}

# Ví dụ sử dụng:
result = add_violation('30A-33918', datetime.now(), 'C:/Users/PC/Desktop/Traffic-Violation-Detection-System/test_image/3.jpg')
print(result)
