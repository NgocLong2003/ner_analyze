import dateparser
from datetime import datetime

def custom_date_parser(date_str):
    # Phân tích biểu thức ngày bằng dateparser, hỗ trợ tiếng Việt
    parsed_date = dateparser.parse(date_str, languages=['vi'])

    if not parsed_date:
        if ("quý" in date_str.lower()) or ("quí" in date_str.lower()):
          if "i" in date_str.lower():
            return "Từ 1/1 tới 31/3"
          elif "ii" in date_str.lower():
            return "Từ 1/4 tới 30/6"
          elif "iii" in date_str.lower():
            return "Từ 1/7 tới 30/9"
          elif "iv" in date_str.lower():
            return "Từ 1/10 tới 31/12"

          quarter = (datetime.now().month - 1) // 3 + 1
          if "này" in date_str.lower():
            return f"Quý {quarter} năm {datetime.now().year}"  # Ví dụ: Quý 1 (nếu hôm nay là tháng 2)

          if "sau" in date_str.lower():
            return f"Quý {quarter +1 if quarter < 4 else '1'} năm {datetime.now().year + 1}"  # Ví dụ: Quý 1 (nếu hôm nay là tháng 2)

          if "trước" in date_str.lower():
            return f"Quý {quarter -1 if quarter > 1 else '4'} năm {datetime.now().year - 1}"  # Ví dụ: Quý 1 (nếu hôm nay là tháng 2)

        return "Không rõ mốc thời gian"

    # Chuyển biểu thức về chữ thường để kiểm tra từ khóa
    date_str_lower = date_str.lower()

    # Nếu có từ "năm", chỉ trả về năm
    if "năm" in date_str_lower:
        return parsed_date.year

    # Nếu có từ "tháng", trả về tháng và năm
    elif "tháng" in date_str_lower:
        return parsed_date.strftime('%m/%Y')

    # Các trường hợp còn lại, trả về ngày đầy đủ
    else:
        return parsed_date.strftime('%d/%m/%Y %H:%M:%S')

# # Danh sách biểu thức để kiểm tra
# test_expressions = [
#     "hôm nay",
#     "ngày mai",
#     "quý này",
#     "Quý I",
#     "quý trước",
#     "cùng quý",
#     "chủ nhật"
# ]

# # Kiểm tra từng biểu thức
# for expr in test_expressions:
#     result = custom_date_parser(expr)
#     print(f"Biểu thức: {expr}")
#     print(f"Kết quả: {result}")
#     print("---")