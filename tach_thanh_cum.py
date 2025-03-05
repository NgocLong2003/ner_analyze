import re
from custom_date_parser import custom_date_parser
from get_meaning import get_meaning


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
  start_ao = 0



  for sentence in data['sentences']:
    for word_info in sentence:
      tu = word_info['form'].replace("_", " ")
      tag = word_info['nerLabel']
      pos_tag = word_info['posTag']



      if pos_tag == 'CH':  # Loại bỏ trường hợp posTag là CH
        cac_cum.append({'text': tu, 'posTag': word_info['posTag'], 'start': -1, 'end': -1, 'nerLabel': word_info['nerLabel'], 'check': 0, 'meaning':''})
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
        if start_hien_tai == []:
          start_hien_tai.append(start_ao)
          end_hien_tai.append(start_ao + len(tu))
          start_ao += len(tu) + 1
        else:
          start_ao += len(tu) + 1
        cac_cum.append({'text': " ".join(cum_hien_tai).replace("_", " "), 'posTag': pos_tag_hien_tai[0], 'nerLabel': tag, 'start': start_hien_tai[0], 'end': end_hien_tai[-1], 'check': 0, 'meaning':''}) # Add tuple (text, posTag)
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
          if start_hien_tai == []:
            start_hien_tai.append(start_ao)
            end_hien_tai.append(start_ao + len(tu))
            start_ao += len(tu) + 1
          else:
            start_ao += len(tu) + 1             
          cac_cum.append({'text': " ".join(cum_hien_tai).replace("_", " "), 'posTag': pos_tag_hien_tai[0], 'nerLabel': tag[-3:], 'start': start_hien_tai[0], 'end': end_hien_tai[-1], 'check': 0, 'meaning':''}) # Add tuple (text, posTag)
          cum_hien_tai = []
          pos_tag_hien_tai = [] # Reset posTag list
          start_hien_tai = []
          end_hien_tai = []
      except IndexError:  # Xử lý trường hợp từ cuối cùng trong câu
        if cum_hien_tai:
          if start_hien_tai == []:
            start_hien_tai.append(start_ao)
            end_hien_tai.append(start_ao + len(tu))
            start_ao += len(tu) + 1
          else:
            start_ao += len(tu) + 1
          cac_cum.append({'text': " ".join(cum_hien_tai).replace("_", " "), 'posTag': pos_tag_hien_tai[0], 'nerLabel': tag[-3:], 'start': start_hien_tai[0], 'end': end_hien_tai[-1], 'check': 0, 'meaning':''}) # Add tuple (text, posTag)
          cum_hien_tai = []
          pos_tag_hien_tai = []# Reset posTag list
          start_hien_tai = []
          end_hien_tai = []
      merged_time = merge_time(cac_cum)
      

  return get_meaning(merged_time, text)

time_combinations = {
    'hôm': ['qua', 'nay', 'sau'],
    'năm': ['nay', 'trước','qua', 'sau','tới'],
    'quý': ['i', 'ii', 'iii', 'iv', 'trước', 'sau', 'tới', 'này', 'nay'],
    'tháng': ['trước', 'sau', 'nay', 'này', 'qua'],
    'tuần': ['trước', 'sau', 'này', 'nay', 'tới'],
    'ngày': ['hôm qua', 'hôm nay', 'mai', 'chủ nhật'],
    'thứ': ['hai', 'ba', 'tư', 'năm', 'sáu', 'bảy',  '2', '3', '4', '5', '6', '7'],
    'chủ nhật': [],
    'hôm nay': [],
    # Thêm các cặp từ khác nếu cần
}

def merge_time(doc):
    i = 0
    merged_entities = []

    while i < len(doc):
        current_ent = doc[i]
        potential_merges = []  # List to hold pairs of entities that can be merged
        next = 0  # Track if we need to skip a next entity

        current_ent_lower = current_ent['text'].lower()

        if current_ent_lower in time_combinations:
            # Check if there's a valid entity before the current one
            if time_combinations[current_ent_lower] == []:
              potential_merges.append(current_ent)
              next = 1
            if i - 1 >= 0:  # Check for previous entity
                prev_ent = doc[i - 1]
                if (prev_ent['posTag'] == 'M') and (prev_ent.get('check') == 0):  # Check if previous entity is a number
                    merged_entities.pop()  # Remove previous entity from merged_entities list
                    potential_merges.append(prev_ent)
                    potential_merges.append(current_ent)  # Add current entity as well
                    next = 1  # Set to skip the next entity in the next iteration

            # Check if there's a valid entity after the current one
            if i + 1 < len(doc):  # Check for next entity
                next_ent = doc[i + 1]
                next_ent_lower = next_ent['text'].lower()
                if next_ent_lower in time_combinations[current_ent_lower]:  # Check if the next entity matches the time_combinations
                    potential_merges.append(current_ent)
                    potential_merges.append(next_ent)
                    doc[i + 1]['check'] = 1  # Mark the next entity as used
                    next = 2  # Skip next entity in the next iteration

        # If no potential merges, simply add current entity
        if next == 0:
            merged_entities.append(current_ent)
            i += 1  # Move to the next entity
        else:
            # If there are potential merges, merge them
            if potential_merges != []:
              # Remove duplicates based on 'start' and 'end' values
              seen = set()
              unique_potential_merges = []
              for d in potential_merges:
                key = (d['start'], d['end'])
                if key not in seen:
                  seen.add(key)
                  unique_potential_merges.append(d)

            potential_merges = unique_potential_merges
            merged_text = " ".join([ent['text'] for ent in potential_merges])
            merged_start = potential_merges[0]['start']
            merged_end = potential_merges[-1]['end']

            merged_entities.append({
                'text': merged_text,
                'posTag': 'N',  # Assume merged entity has 'N' POS tag
                'nerLabel': 'DATE',  # Assuming the merged label is 'DATE'
                'start': merged_start,
                'end': merged_end,
                'meaning': custom_date_parser(merged_text)
            })

            # Update the index to skip over the merged entities
            i += next
            potential_merges.clear()  # Reset potential merges list

    return merged_entities

# Kiểm tra hệ thống

# # Gọi hàm merge_time để gộp các thực thể
# merged_entities = merge_time(ner_result)

# for ent in merged_entities:
#     print(f"Text: {ent['text']}, Label: {ent['nerLabel']}, Start: {ent['start']}, End: {ent['end']}")

# text = """Năm nay, tại Hà Nội, Thủ tướng Chính phủ đã có cuộc họp khẩn với Bộ Tài chính và Ngân hàng Nhà nước về tình hình lạm phát gia tăng trong quý I năm nay. Cuộc họp diễn ra sau khi chỉ số giá tiêu dùng (CPI) tháng trước tăng 1,2% so với tháng liền kê, nâng mức lạm phát trung bình của ba tháng đầu năm lên 4,3%. Trong cuộc họp, ông Trân Văn A - Thống đốc Ngân hàng Nhà nước - đã đề xuất các biện pháp kiếm soát cung tiên, trong đó có điêu chính lãi suất cơ bản.
# Trong một diễn biến liên quan, sáng thứ Hai tuân trước, tập đoàn VinaTech đã công bố kế hoạch mở rộng nhà máy sản xuất chip tại khu công nghệ cao TP.HCM, dự kiến hoàn thành trong vòng hai năm. Dự án có tổng vốn đầu tư 600 triệu USD, với sự tham gia của đối tác Nhật Bản là Tập đoàn Nagaoka. Theo ông Yamamoto Kenji, Giám đốc điêu hành Nagaoka, đây là bước đi chiên lược để tận dụng chính sách ưu đãi thuế mới của Việt Nam, có hiệu lực từ quý II năm nay"""


# full_ner = vnp.annotate(text)
# ner_result = tach_thanh_cum(full_ner, text)
# for ner in ner_result:
#   print(ner)




