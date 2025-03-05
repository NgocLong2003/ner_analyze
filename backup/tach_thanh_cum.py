import re



def tach_thanh_cum(data, text):
  """Tách danh sách các thành phần thành các cụm từ dựa trên tag thực thể.

  Args:
    data: Từ điển chứa danh sách câu, mỗi câu là một danh sách các từ điển,
          mỗi từ điển chứa thông tin về một từ.

  Returns:
    Một danh sách các cụm từ (text, posTag), bao gồm cả cụm không được nối và loại bỏ posTag CH.
  """

  cac_cum = []
  cum_hien_tai = []
  pos_tag_hien_tai = [] # List to store posTags for the current phrase
  start_hien_tai = []
  end_hien_tai = []
  checkpoint = -1
  


  for sentence in data['sentences']:
    for word_info in sentence:
      tu = word_info['form'].replace("_", " ")
      tag = word_info['nerLabel']
      pos_tag = word_info['posTag']
      
      

      if pos_tag == 'CH':  # Loại bỏ trường hợp posTag là CH
        cac_cum.append({'text': tu, 'posTag': word_info['posTag'], 'nerLabel': word_info['nerLabel']})
        continue
      # Kiểm tra điều kiện cho nhóm B-, I-
      if tag.startswith("B-") or tag.startswith("I-"):
        cum_hien_tai.append(tu)
        pos_tag_hien_tai.append(pos_tag) # Append posTag to the list
        positions = [match.start() for match in re.finditer(tu, text)]
        # print(cum_hien_tai, positions)
        for i in positions:
          if i >= checkpoint:
            start_hien_tai.append(i)
            end_hien_tai.append(i + len(tu))
            checkpoint = i
            break
      else:
        # Nếu không phải B-, I-
        # thêm cum_hien_tai vào cac_cum nếu không rỗng
        cum_hien_tai.append(tu)
        pos_tag_hien_tai.append(pos_tag) # Append posTag to the list
        positions = [match.start() for match in re.finditer(tu, text)]
        # print(cum_hien_tai, positions)
        for i in positions:
          if i >= checkpoint:
            start_hien_tai.append(i)
            end_hien_tai.append(i + len(tu))
            checkpoint = i
            break
        cac_cum.append({'text': " ".join(cum_hien_tai).replace("_", " "), 'posTag': pos_tag_hien_tai[0], 'nerLabel': tag, 'start': start_hien_tai[0], 'end': end_hien_tai[-1]}) # Add tuple (text, posTag)
        # cac_cum.append((" ".join(cum_hien_tai).replace("_", " "), pos_tag_hien_tai[0])) # Add tuple (text, posTag)
        cum_hien_tai = []
        pos_tag_hien_tai = [] # Reset posTag list
        start_hien_tai = []
        end_hien_tai = []

      # Kiểm tra từ tiếp theo để quyết định thêm cum_hien_tai vào cac_cum
      try:
        next_word_info = sentence[word_info['index']]
        next_tag = next_word_info['nerLabel']
        if not (next_tag.startswith("I-") and tag.startswith(("B-", "I-"))) and cum_hien_tai:
          
          cac_cum.append({'text': " ".join(cum_hien_tai).replace("_", " "), 'posTag': pos_tag_hien_tai[0], 'nerLabel': tag, 'start': start_hien_tai[0], 'end': end_hien_tai[-1]}) # Add tuple (text, posTag)
          cum_hien_tai = []
          pos_tag_hien_tai = [] # Reset posTag list
          start_hien_tai = []
          end_hien_tai = []
      except IndexError:  # Xử lý trường hợp từ cuối cùng trong câu
        if cum_hien_tai:
          cac_cum.append({'text': " ".join(cum_hien_tai).replace("_", " "), 'posTag': pos_tag_hien_tai[0], 'nerLabel': tag, 'start': start_hien_tai[0], 'end': end_hien_tai[-1]}) # Add tuple (text, posTag)
          cum_hien_tai = []
          pos_tag_hien_tai = []# Reset posTag list
          start_hien_tai = []
          end_hien_tai = []

  return cac_cum

# text = """Năm nay, tại Hà Nội, Thủ tướng Chính phủ đã có cuộc họp khẩn với Bộ Tài chính và Ngân hàng Nhà nước về tình hình lạm phát gia tăng trong quý I năm nay. Cuộc họp diễn ra sau khi chỉ số giá tiêu dùng (CPI) tháng trước tăng 1,2% so với tháng liền kê, nâng mức lạm phát trung bình của ba tháng đầu năm lên 4,3%. Trong cuộc họp, ông Trân Văn A - Thống đốc Ngân hàng Nhà nước - đã đề xuất các biện pháp kiếm soát cung tiên, trong đó có điêu chính lãi suất cơ bản.
# Trong một diễn biến liên quan, sáng thứ Hai tuân trước, tập đoàn VinaTech đã công bố kế hoạch mở rộng nhà máy sản xuất chip tại khu công nghệ cao TP.HCM, dự kiến hoàn thành trong vòng hai năm. Dự án có tổng vốn đầu tư 600 triệu USD, với sự tham gia của đối tác Nhật Bản là Tập đoàn Nagaoka. Theo ông Yamamoto Kenji, Giám đốc điêu hành Nagaoka, đây là bước đi chiên lược để tận dụng chính sách ưu đãi thuế mới của Việt Nam, có hiệu lực từ quý II năm nay"""


# full_ner = vnp.annotate(text)
# ner_result = tach_thanh_cum(full_ner, text)
# for ner in ner_result:
#   print(ner)