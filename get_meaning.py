import re
import requests
import json

# Tên file JSON để lưu từ điển
word_dict_file = 'word_dict.json'

# Hàm để đọc từ điển từ file
def load_word_dict():
    try:
        with open(word_dict_file, 'r', encoding='utf-8') as file:
            print("thấy json")
            return json.load(file)
    except FileNotFoundError:
        print("đ thấy json đâu")
        return []  # Nếu file không tồn tại, trả về danh sách trống

# Hàm để lưu từ điển vào file JSON
def save_word_dict(word_dict):
    with open(word_dict_file, 'w', encoding='utf-8') as file:
        json.dump(word_dict, file, ensure_ascii=False, indent=4)





# wiki_wiki = wikipediaapi.Wikipedia(
#     user_agent='my_bot/1.0 (my_email@example.com)',
#     language='vi',  # Ngôn ngữ: 'vi' cho tiếng Việt
#     extract_format=wikipediaapi.ExtractFormat.WIKI
# )

def custom_wiki(text):


    url = f"https://vi.wikipedia.org/api/rest_v1/page/summary/{text}"
    headers = {'User-Agent': 'my_bot/1.0 (my_email@example.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            summary = data.get('extract', '')[:300]
            return summary if summary else None
        return None
    except requests.RequestException:
        return None

def get_meaning(merge_entities, text):
    # Đọc dữ liệu khi server khởi động
    word_dict = load_word_dict()    
    # Duyệt qua từng từ trong word_dict
    for word_entry in word_dict:
        word = word_entry['text']  # Lấy từ cần tìm
        # Dùng re.finditer để lấy tất cả các vị trí của từ trong văn bản
        positions = [match.span() for match in re.finditer(re.escape(word), text.lower())]

        if positions:
            print(f"Found positions for '{word}': {positions}")

        # Duyệt qua các vị trí tìm được
        for start_word, end_word in positions:
            potential_merges = []  # Dùng để lưu các thực thể cần gộp
            indices_to_remove = []  # Dùng để lưu các chỉ số của thực thể cũ sẽ bị xóa

            # Kiểm tra các thực thể trong merge_entities
            for i, entity in enumerate(merge_entities):
                # Nếu thực thể nằm trong phạm vi của từ này (start và end của entity nằm trong start_word và end_word)
                if entity['start'] >= start_word and entity['end'] <= end_word:
                    potential_merges.append(entity)
                    indices_to_remove.append(i)

            if potential_merges:
                # Gộp tất cả các thực thể trong potential_merges thành một thực thể duy nhất
                merged_text = " ".join([ent['text'] for ent in potential_merges])
                posTag = potential_merges[0]['posTag']
                nerLabel = potential_merges[0]['nerLabel'][-3:]
                merged_start = potential_merges[0]['start']  # start của thực thể đầu tiên
                merged_end = potential_merges[-1]['end']    # end của thực thể cuối cùng

                # Cập nhật thực thể đã gộp với thông tin từ từ điển
                merged_entity = {
                    'text': merged_text,
                    'posTag': word_entry['posTag'] if word_entry['posTag'] != '' else posTag,
                    'nerLabel':word_entry['nerLabel'] if word_entry['nerLabel'] != 'null' else nerLabel,
                    'start': merged_start,
                    'end': merged_end,
                    'meaning': word_entry['meaning']  # Thêm nghĩa vào trường 'meaning'
                }

                # Loại bỏ các thực thể cũ và thay thế bằng thực thể mới
                for index in reversed(indices_to_remove):  # Duyệt ngược để không bị lỗi khi xóa
                    merge_entities.pop(index)

                # Thêm thực thể đã gộp vào vị trí của thực thể cũ
                merge_entities.insert(indices_to_remove[0], merged_entity)
        # #Lấy định nghĩa trên wikipedia
        # for i in merge_entities:
        #   if (i['nerLabel'] not in ['O', 'DATE']) and (i['meaning'] == ''):
        #     i['meaning'] = custom_wiki(i['text'])
    return merge_entities



# # Gọi hàm get_meaning
# merged_entities_with_meaning = get_meaning(ner_result, word_dict, text)

# # Kiểm tra kết quả
# for entity in merged_entities_with_meaning:
#     print(entity)