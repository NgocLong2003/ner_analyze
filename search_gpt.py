from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"
# Thay "YOUR_API_KEY" bằng API key của bạn

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)
def ask_question(text, nerLabel):
    # Thêm đoạn văn mới vào context
    ner = "là gì hoặc là ai hoặc ở đâu?"
    if nerLabel[-3:] == "LOC":
        ner = "là ai hoặc ở đâu?"
    elif nerLabel[-3:] == "PER":
        ner = "là ai?"
    elif nerLabel[-3:] == "ORG":
        ner = "là gì?"
    
    question = f"{text} {ner}"

    # Gọi API với context hiện tại
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Hoặc gpt-4
        messages=[
            {"role":"system", "content":"Bạn hãy trả lời ngắn gọn câu hỏi trong 3 câu và tối đa 300 ký tự. Nếu đó là 1 chức danh, trả lời cả người đương nhiệm"},
            {"role": "user", "content": question}
        ],
    )

    # Lấy kết quả từ phản hồi
    output = response.choices[0].message.content

    # # Lưu lại phản hồi vào context
    # messages.append({"role": "assistant", "content": output})
    return output#, messages


# answer = ask_question("Bộ Tài chính", "B-ORG")
# print(answer)
