import math

# license plate type classification helper function
def linear_equation(x1, y1, x2, y2):
    b = y1 - (y2 - y1) * x1 / (x2 - x1)
    a = (y1 - b) / x1
    return a, b

def check_point_linear(x, y, x1, y1, x2, y2):
    a, b = linear_equation(x1, y1, x2, y2)
    y_pred = a*x+b
    return(math.isclose(y_pred, y, abs_tol = 3))

def check_valid_plate(plate: str) -> bool:
    parts = plate.split('-')
    if len(parts) != 2 or (len(parts[0])!=3 and len(parts[0])!=4) or (len(parts[1])!=4 and len(parts[1])!=5):
        return False
    unknown_plate = ["13", "42", "44", "45", "46", "87", "91", "96"]
    if (parts[0][0].isalpha() or parts[0][1].isalpha() or parts[0][2].isnumeric()): return False
    for char in parts[1]:
        if (char.isalpha()): return False

    if parts[0] in unknown_plate: return False
    return True
    
# detect character and number in license plate
# def read_plate(yolo_license_plate, im):
#     LP_type = "1"
#     results = yolo_license_plate(im)
#     bb_list = results.pandas().xyxy[0].values.tolist()
#     if len(bb_list) == 0 or len(bb_list) < 7 or len(bb_list) > 10:
#         return "unknown"
#     center_list = []
#     y_mean = 0
#     y_sum = 0
#     for bb in bb_list:
#         x_c = (bb[0]+bb[2])/2
#         y_c = (bb[1]+bb[3])/2
#         y_sum += y_c
#         center_list.append([x_c,y_c,bb[-1]])

#     # find 2 point to draw line
#     l_point = center_list[0]
#     r_point = center_list[0]
#     for cp in center_list:
#         if cp[0] < l_point[0]:
#             l_point = cp
#         if cp[0] > r_point[0]:
#             r_point = cp
#     for ct in center_list:
#         if l_point[0] != r_point[0]:
#             if (check_point_linear(ct[0], ct[1], l_point[0], l_point[1], r_point[0], r_point[1]) == False):
#                 LP_type = "2"

#     y_mean = int(int(y_sum) / len(bb_list))
#     size = results.pandas().s

#     # 1 line plates and 2 line plates
#     line_1 = []
#     line_2 = []
#     license_plate = ""
#     if LP_type == "2":
#         for c in center_list:
#             if int(c[1]) > y_mean:
#                 line_2.append(c)
#             else:
#                 line_1.append(c)
#         for l1 in sorted(line_1, key = lambda x: x[0]):
#             license_plate += str(l1[2])
#         license_plate += "-"
#         for l2 in sorted(line_2, key = lambda x: x[0]):
#             license_plate += str(l2[2])
#     else:
#         for l in sorted(center_list, key = lambda x: x[0]):
#             license_plate += str(l[2])
#     return license_plate

def read_plate(yolo_license_plate, im):
    results = yolo_license_plate(im)
    bb_list = results.pandas().xyxy[0].values.tolist()
    
    if not (7 <= len(bb_list) <= 10):
        return "unknown"
    
    center_list = [[(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2, bb[-1]] for bb in bb_list]
    y_mean = sum(c[1] for c in center_list) / len(center_list)
    
    l_point = min(center_list, key=lambda c: c[0])
    r_point = max(center_list, key=lambda c: c[0])
    
    LP_type = "1"
    if l_point[0] != r_point[0]:
        for c in center_list:
            if not check_point_linear(c[0], c[1], l_point[0], l_point[1], r_point[0], r_point[1]):
                LP_type = "2"
                break
    
    line_1 = [c for c in center_list if c[1] <= y_mean]
    line_2 = [c for c in center_list if c[1] > y_mean]
    
    license_plate = ""
    if LP_type == "2":
        license_plate = "".join(str(c[2]) for c in sorted(line_1, key=lambda x: x[0]))
        license_plate += "-"
        license_plate += "".join(str(c[2]) for c in sorted(line_2, key=lambda x: x[0]))
    else:
        license_plate = "".join(str(c[2]) for c in sorted(center_list, key=lambda x: x[0]))
        license_plate = license_plate[:3]+'-'+license_plate[3:]
        
    
    return license_plate