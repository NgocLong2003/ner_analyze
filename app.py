from flask import Flask, render_template, request
app = Flask(__name__)
from vncorenlp import VnCoreNLP
from tach_thanh_cum import tach_thanh_cum
from pos_tag_dict import pos_tag_dict
from search_gpt import ask_question
from get_meaning import load_word_dict, save_word_dict
vnp = VnCoreNLP("VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg,pos,ner,parse")


@app.route('/', methods=['GET', 'POST'])
def index():
    text = ''
    entities = []
    if request.method == 'POST':
        text = request.form.get('input_text', '')
        full_ner = vnp.annotate(text)
        entities = tach_thanh_cum(full_ner, text)

    return render_template('index.html', text=text, entities=entities, pos_tag_dict=pos_tag_dict)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    ner_label = request.args.get('nerLabel')  # Lấy 'nerLabel' từ query string
    # Tên file JSON để lưu từ điển
    word_dict = load_word_dict()
    # Kiểm tra xem 'query' và 'nerLabel' có tồn tại không
    if query and ner_label:
        # Gọi hàm ask_question để lấy kết quả từ GPT hoặc Wikipedia
        result = ask_question(query, ner_label)
        word_dict.append({'text': query.lower(), 'meaning': result, 'posTag': '', 'nerLabel': ner_label})
            # Lưu lại từ điển vào file JSON
        save_word_dict(word_dict)
        return result  # Trả về kết quả dưới dạng text
    else:
        return 'Thiếu tham số query hoặc nerLabel', 400


if __name__ == '__main__':
    app.run(debug=True)